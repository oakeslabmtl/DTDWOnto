from collections import OrderedDict
import logging
import logging.config
from utils import log_assert
from rabbitmq import Rabbitmq
from fmpy import read_model_description
import pprint as pp
from fmu_utils import build_logging_function, getVars, load


class DUTMonitorFMUService:
    def __init__(self, fmu_path, rabbit_config):
        self._l = logging.getLogger("DUTMonitorFMU")
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
                                on_message_callback=self.data_in, queue_name="dut_monitor")
        self.rabbitmq.subscribe(routing_key="testbench.output",
                                on_message_callback=self.data_in, queue_name="dut_monitor")
        self.rabbitmq.subscribe(routing_key="in_dut.output",
                                on_message_callback=self.data_in, queue_name="dut_monitor")
        
        # Try to load the fmu
        self.fmu_model_description = read_model_description(self.fmu_path)
        self.fmu_vars = getVars(self.fmu_model_description)
        self._l.debug(f"FMU variables: {pp.pformat(self.fmu_vars)}")
        self.fmu,_ = load(self.fmu_path, self.fmu_model_description, "monitor", build_logging_function(self._l))
        self._l.debug(f"Loaded fmu successfully: {self.fmu.modelIdentifier}.")


    def start(self):
        self.rabbitmq.start_consuming()

    def data_in(self, ch, method, properties, body_json):

        if method.routing_key == "dut.output":
            self._l.debug(f"Received dut.output: {body_json}.")
        elif method.routing_key == "testbench.output":
            self._l.debug(f"Received testbench.output: {body_json}.")
        elif method.routing_key == "in_dut.output":
            self._l.debug(f"Received in_dut.output: {body_json}.")
        else:
            log_assert(self._l, False, f"Unknown routing key: {method.routing_key}.")
        
        # Store message in buffer
        if body_json["time"] not in self.input_buffer:
            self.input_buffer[body_json["time"]] = {method.routing_key: body_json}
        else:
            self.input_buffer[body_json["time"]][method.routing_key] = body_json

        self.do_computation()


    def do_computation(self):
        # Check timestamps are aligned
        
        # Get the smallest timestamp in the buffer
        timestamp = next(iter(self.input_buffer.keys()))

        # Check if we have all the data we need
        if "dut.output" not in self.input_buffer[timestamp] or "testbench.output" not in self.input_buffer[timestamp] or "in_dut.output" not in self.input_buffer[timestamp]:
            return

        dut_output_data = self.input_buffer[timestamp]["dut.output"]
        testbench_output_data = self.input_buffer[timestamp]["testbench.output"]
        set_input_output_data = self.input_buffer[timestamp]["in_dut.output"]

        self._l.info(f"Computing conformance at time {timestamp}.")

        if not self.fmu_initialized:
            self._l.debug(f"Initializing FMU at time {timestamp}.")
            self.fmu.instantiate(loggingOn=False)
            self.fmu.setupExperiment(startTime=timestamp)
            self.fmu.enterInitializationMode()
            self.fmu.exitInitializationMode()
            self.fmu_initialized = True

        # Set inputs to FMU. See the scenario file to understand this.
        self._l.debug(f"Setting inputs to FMU.")
        
        self.fmu.setReal([self.fmu_vars["in_angle"].valueReference], [testbench_output_data["fields"]["out_angle"]])
        self.fmu.setReal([self.fmu_vars["in_speed"].valueReference], [testbench_output_data["fields"]["out_speed"]])
        self.fmu.setReal([self.fmu_vars["in_acceleration"].valueReference], [testbench_output_data["fields"]["out_acceleration"]])

        # self.fmu.setReal([self.fmu_vars["dut_out_torque"].valueReference], [dut_output_data["fields"]["out_torque"]])
        # self.fmu.setReal([self.fmu_vars["dut_out_acceleration"].valueReference], [dut_output_data["fields"]["out_acceleration"]])
        self.fmu.setReal([self.fmu_vars["dut_out_speed"].valueReference], [dut_output_data["fields"]["out_speed"]])
        # self.fmu.setReal([self.fmu_vars["dut_out_angle"].valueReference], [dut_output_data["fields"]["out_angle"]])

        self.fmu.setReal([self.fmu_vars["in_set_torque"].valueReference], [set_input_output_data["fields"]["y"]])
        
        # Step the fmu, to trigger conformance computation
        self._l.debug(f"Stepping FMU.")
        self.fmu.doStep(currentCommunicationPoint=timestamp, communicationStepSize=0.001)

        # Get the conformance out of the FMU and publish it
        self.out_conformance = self.fmu.getReal([self.fmu_vars["out_conformance"].valueReference])[0]
        self._l.debug(f"Conformance: {self.out_conformance}")

        # Remove the timestamp from the buffer
        del self.input_buffer[timestamp]

        self.publish_state(timestamp)
        
    def publish_state(self, timestamp):
        message = {
            "measurement": "DUTMonitor",
            "time": timestamp,
            "tags": {
                "source": "DUTMonitor"
            },
            "fields": {
                "conformance": self.out_conformance
            }
        }

        self.rabbitmq.send_message("dut_monitor.output", message)

if __name__ == "__main__":
    from pyhocon import ConfigFactory
    import os
    import sys
    
    # Clear log file for monitor
    log_file = "dut_monitor_fmu.log"
    with open(log_file, "w"):
        pass

    # Start DUTMonitorFMUService
    config = ConfigFactory.parse_file("service.conf")

    monitor = DUTMonitorFMUService(fmu_path = os.path.abspath(sys.argv[1]),
                                rabbit_config=config["rabbitmq"])

    # Set logging config for DUTMonitorFMU logger so that only its log messages are seen.
    monitor._l.setLevel(logging.DEBUG)
    monitor._l.addHandler(logging.FileHandler(log_file))

    monitor.setup()

    monitor.start()