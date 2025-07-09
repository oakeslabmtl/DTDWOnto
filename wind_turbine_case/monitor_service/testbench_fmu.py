from collections import OrderedDict
import logging
import logging.config
from utils import log_assert
from rabbitmq import Rabbitmq
from fmpy import read_model_description
import pprint as pp

from fmu_utils import build_logging_function, getVars, load

class TestBenchFMUService:
    def __init__(self, fmu_path, rabbit_config):
        self._l = logging.getLogger("TestBenchFMU")
        self.rabbitmq = Rabbitmq(**rabbit_config)
        self.fmu_path = fmu_path

        self.fmu_model_description = None
        self.fmu_vars = None
        self.fmu = None
        self.fmu_initialized = False

        self.input_buffer = OrderedDict()

        
    def setup(self):
        self.rabbitmq.connect_to_server()

        self.rabbitmq.subscribe(routing_key="dut.output",
                                on_message_callback=self.data_in, queue_name="testbench")
        self.rabbitmq.subscribe(routing_key="in_tb.output",
                                on_message_callback=self.data_in, queue_name="testbench")
        
        # Try to load the fmu
        self.fmu_model_description = read_model_description(self.fmu_path)
        self.fmu_vars = getVars(self.fmu_model_description)
        self._l.debug(f"FMU variables: {pp.pformat(self.fmu_vars)}")
        self.fmu,_ = load(self.fmu_path, self.fmu_model_description, "monitor", build_logging_function(self._l))
        self._l.debug(f"Loaded fmu successfully: {self.fmu.modelIdentifier}.")


    def start(self):
        self.rabbitmq.start_consuming()

    def data_in(self, ch, method, properties, body_json):
        
        if method.routing_key == "in_tb.output":
            self._l.debug(f"Received in_tb.output: {body_json}.")
        elif method.routing_key == "dut.output":
            self._l.debug(f"Received dut.output: {body_json}.")
        else:
            log_assert(self._l, False, f"Unknown routing key: {method.routing_key}.")

        # Store message in buffer
        if body_json["time"] not in self.input_buffer:
            self.input_buffer[body_json["time"]] = {method.routing_key: body_json}
        else:
            self.input_buffer[body_json["time"]][method.routing_key] = body_json

        self.do_computation()

    def do_computation(self):
        
        it = iter(self.input_buffer.keys())
        timestamp = next(it)

        if not self.fmu_initialized:
            self._l.debug(f"Initializing FMU at time {timestamp}.")
            self.fmu.instantiate(loggingOn=False)
            self.fmu.setupExperiment(startTime=timestamp)
            self.fmu.enterInitializationMode()
            
            self.out_angle = 0.0
            self.out_speed = 1.0
            self.out_acceleration = 1.0
            self.out_angle_inertia = self.fmu.getReal([self.fmu_vars["out_angle_inertia"].valueReference])[0]

            self.fmu.exitInitializationMode()
            self.fmu_initialized = True

            self.publish_state(timestamp)
            return
        
        if len(self.input_buffer.keys()) < 2:
            return
        
        # This FMU always steps ahead of time, so we get the next timestamp
        next_timestamp = next(it)

        # Check if we have all the data we need. 
        if "in_tb.output" not in self.input_buffer[timestamp] or "dut.output" not in self.input_buffer[timestamp]:
            return 

        dut_output_data = self.input_buffer[timestamp]["dut.output"]
        in_tb_output_data = self.input_buffer[timestamp]["in_tb.output"]

        self._l.info(f"Stepping FMU at time {timestamp}.")
        
        # Set inputs to FMU. See the scenario file to understand this.
        self._l.debug(f"Setting inputs to FMU.")
        self.fmu.setReal([self.fmu_vars["in_torque"].valueReference], [dut_output_data["fields"]["out_torque"]])
        self.fmu.setReal([self.fmu_vars["in_set_speed"].valueReference], [in_tb_output_data["fields"]["y"]])
        
        # Step the fmu, to trigger conformance computation
        self._l.debug(f"Stepping FMU.")
        self.fmu.doStep(currentCommunicationPoint=timestamp, communicationStepSize=0.001)

        # Get the conformance out of the FMU and publish it
        self.out_acceleration = self.fmu.getReal([self.fmu_vars["out_acceleration"].valueReference])[0]
        self.out_speed = self.fmu.getReal([self.fmu_vars["out_speed"].valueReference])[0]
        self.out_angle = self.fmu.getReal([self.fmu_vars["out_angle"].valueReference])[0]
        self.out_angle_inertia = self.fmu.getReal([self.fmu_vars["out_angle_inertia"].valueReference])[0]

        # Remove the timestamp from the buffer
        del self.input_buffer[timestamp]

        self.publish_state(next_timestamp)
        
    def publish_state(self, timestamp):
        message = {
            "measurement": "DUTFMU",
            "time": timestamp,
            "tags": {
                "source": "DUTFMU"
            },
            "fields": {
                "out_acceleration" : self.out_acceleration,
                "out_speed" : self.out_speed,
                "out_angle" : self.out_angle,
                "out_angle_inertia" : self.out_angle_inertia
            }
        }

        self.rabbitmq.send_message("testbench.output", message)

if __name__ == "__main__":
    from pyhocon import ConfigFactory
    import os
    import sys
    
    # Clear log file for monitor
    log_file = "testbench_fmu.log"

    with open(log_file, "w"):
        pass

    # Start TestBenchFMUService
    config = ConfigFactory.parse_file("service.conf")

    service = TestBenchFMUService(fmu_path = os.path.abspath(sys.argv[1]),
                                rabbit_config=config["rabbitmq"])

    # Set logging config for TestBenchFMU logger so that only its log messages are seen.
    service._l.setLevel(logging.DEBUG)
    service._l.addHandler(logging.FileHandler(log_file))

    service.setup()

    service.start()