import logging
import logging.config
from utils import log_assert
from rabbitmq import Rabbitmq
from fmpy import read_model_description
import pprint as pp
from collections import OrderedDict

from fmu_utils import build_logging_function, getVars, load

class DUTFMUService:
    def __init__(self, fmu_path, rabbit_config):
        self._l = logging.getLogger("DUTFMU")
        self.rabbitmq = Rabbitmq(**rabbit_config)
        self.fmu_path = fmu_path

        self.fmu_model_description = None
        self.fmu_vars = None
        self.fmu = None
        self.fmu_initialized = False

        self.input_buffer = OrderedDict()
        
    def setup(self):
        self.rabbitmq.connect_to_server()

        self.rabbitmq.subscribe(routing_key="testbench.output",
                                on_message_callback=self.data_in, queue_name="dut")
        self.rabbitmq.subscribe(routing_key="in_dut.output",
                                on_message_callback=self.data_in, queue_name="dut")
        
        # Try to load the fmu
        self.fmu_model_description = read_model_description(self.fmu_path)
        self.fmu_vars = getVars(self.fmu_model_description)
        self._l.debug(f"FMU variables: {pp.pformat(self.fmu_vars)}")
        self.fmu,_ = load(self.fmu_path, self.fmu_model_description, "monitor", build_logging_function(self._l))
        self._l.debug(f"Loaded fmu successfully: {self.fmu.modelIdentifier}.")


    def start(self):
        self.rabbitmq.start_consuming()

    def data_in(self, ch, method, properties, body_json):
        if method.routing_key == "in_dut.output":
            self._l.debug(f"Received in_dut.output: {body_json}.")
        elif method.routing_key == "testbench.output":
            self._l.debug(f"Received TB output: {body_json}.")
        else:
            log_assert(self._l, False, f"Unknown routing key: {method.routing_key}.")

        # Store message in buffer
        if body_json["time"] not in self.input_buffer:
            self.input_buffer[body_json["time"]] = {method.routing_key: body_json}
        else:
            self.input_buffer[body_json["time"]][method.routing_key] = body_json

        self.do_computation()
        

    def do_computation(self):
        
        # Get the smallest timestamp in the buffer
        timestamp = next(iter(self.input_buffer.keys()))

        # Check if we have all the data we need
        if "in_dut.output" not in self.input_buffer[timestamp] or "testbench.output" not in self.input_buffer[timestamp]:
            return

        in_dut_output_data = self.input_buffer[timestamp]["in_dut.output"]
        testbench_output_data = self.input_buffer[timestamp]["testbench.output"]

        self._l.info(f"Stepping FMU at time {timestamp}.")

        if not self.fmu_initialized:
            self._l.debug(f"Initializing FMU at time {timestamp}.")
            self.fmu.instantiate(loggingOn=False)
            self.fmu.setupExperiment(startTime=timestamp)
            self.fmu.enterInitializationMode()
            # Set dut_turbine.J parameter to 1.6 to simulate an anomaly
            self.fmu.setReal([self.fmu_vars["dut_turbine.J"].valueReference], [1.6])
            self.fmu.exitInitializationMode()
            self.fmu_initialized = True

        # Get the stuff out of the FMU and publish it
        self.out_torque = self.fmu.getReal([self.fmu_vars["out_torque"].valueReference])[0]
        self.out_acceleration = self.fmu.getReal([self.fmu_vars["out_acceleration"].valueReference])[0]
        self.out_speed = self.fmu.getReal([self.fmu_vars["out_speed"].valueReference])[0]
        self.out_angle = self.fmu.getReal([self.fmu_vars["out_angle"].valueReference])[0]

        # Set inputs to FMU. See the scenario file to understand this.
        self._l.debug(f"Setting inputs to FMU.")
        self.fmu.setReal([self.fmu_vars["in_angle"].valueReference], [testbench_output_data["fields"]["out_angle"]])
        self.fmu.setReal([self.fmu_vars["in_speed"].valueReference], [testbench_output_data["fields"]["out_speed"]])
        self.fmu.setReal([self.fmu_vars["in_acceleration"].valueReference], [testbench_output_data["fields"]["out_acceleration"]])
        self.fmu.setReal([self.fmu_vars["in_set_torque"].valueReference], [in_dut_output_data["fields"]["y"]])
        
        # Step the fmu
        self._l.debug(f"Stepping FMU.")
        self.fmu.doStep(currentCommunicationPoint=timestamp, communicationStepSize=0.001)

        # Remove the timestamp from the buffer
        del self.input_buffer[timestamp]

        self.publish_state(timestamp)
        
    def publish_state(self, timestamp):
        message = {
            "measurement": "DUTFMU",
            "time": timestamp,
            "tags": {
                "source": "DUTFMU"
            },
            "fields": {
                "out_torque" : self.out_torque,
                "out_acceleration" : self.out_acceleration,
                "out_speed" : self.out_speed,
                "out_angle" : self.out_angle,
            }
        }

        self.rabbitmq.send_message("dut.output", message)

if __name__ == "__main__":
    from pyhocon import ConfigFactory
    import os
    import sys
    
    # Clear log file for monitor
    log_file = "dut_fmu.log"
    with open(log_file, "w"):
        pass

    # Start DUTFMUService
    config = ConfigFactory.parse_file("service.conf")

    monitor = DUTFMUService(fmu_path = os.path.abspath(sys.argv[1]),
                                rabbit_config=config["rabbitmq"])

    # Set logging config for this logger so that only its log messages are seen.
    monitor._l.setLevel(logging.DEBUG)
    monitor._l.addHandler(logging.FileHandler(log_file))

    monitor.setup()

    monitor.start()