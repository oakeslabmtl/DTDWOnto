import logging
import logging.config
from utils import log_assert
from rabbitmq import Rabbitmq
from fmpy import read_model_description
import pprint as pp

from fmu_utils import build_logging_function, getVars, load

class SetInputFMUService:
    def __init__(self, fmu_path, k, instance, rabbit_config):
        self._l = logging.getLogger("SetInputFMU")
        self.rabbitmq = Rabbitmq(**rabbit_config)
        self.fmu_path = fmu_path

        self.fmu_model_description = None
        self.fmu_vars = None
        self.fmu = None
        self.fmu_initialized = False

        self.k = k
        self.instance = instance
        self.clock_output_data = None
        
    def setup(self):
        self.rabbitmq.connect_to_server()

        self.rabbitmq.subscribe(routing_key="clock.output",
                                on_message_callback=self.data_in, queue_name=f"{self.instance}")
        
        # Try to load the fmu
        self.fmu_model_description = read_model_description(self.fmu_path)
        self.fmu_vars = getVars(self.fmu_model_description)
        self._l.debug(f"FMU variables: {pp.pformat(self.fmu_vars)}")
        self.fmu,_ = load(self.fmu_path, self.fmu_model_description, "monitor", build_logging_function(self._l))
        self._l.debug(f"Loaded fmu successfully: {self.fmu.modelIdentifier}.")


    def start(self):
        self.rabbitmq.start_consuming()

    def data_in(self, ch, method, properties, body_json):
        self._l.debug(f"Received message: {body_json}.")

        log_assert(self._l, method.routing_key == "clock.output", f"Received unexpected topic {method.routing_key}.")

        self.clock_output_data = body_json

        self.do_computation()

    def do_computation(self):
        self.timestamp = self.clock_output_data["time"]

        if not self.fmu_initialized:
            self._l.debug(f"Initializing FMU at time {self.timestamp}.")
            self.fmu.instantiate(loggingOn=False)
            self.fmu.setupExperiment(startTime=self.timestamp)
            self.fmu.enterInitializationMode()

            # set parameter k 
            self.fmu.setReal([self.fmu_vars["k"].valueReference], [self.k])

            self.fmu.exitInitializationMode()
            self.fmu_initialized = True

        # Step the fmu, to trigger conformance computation
        self._l.debug(f"Stepping FMU.")
        self.fmu.doStep(currentCommunicationPoint=self.timestamp, communicationStepSize=0.001)

        # Get the conformance out of the FMU and publish it
        self.out_y = self.fmu.getReal([self.fmu_vars["y"].valueReference])[0]

        self.publish_state()
        
    def publish_state(self):
        message = {
            "measurement": "SetInputFMU",
            "time": self.timestamp,
            "tags": {
                "source": "SetInputFMU"
            },
            "fields": {
                "y" : self.out_y,
            }
        }

        self.rabbitmq.send_message(f"{self.instance}.output", message)

if __name__ == "__main__":
    from pyhocon import ConfigFactory
    import os
    import sys
    
    instance = sys.argv[3]

    # Clear log file for monitor
    log_file = f"{instance}_fmu.log"

    with open(log_file, "w"):
        pass

    # Start SetInputFMUService
    config = ConfigFactory.parse_file("service.conf")

    monitor = SetInputFMUService(fmu_path = os.path.abspath(sys.argv[1]),
                                    k = float(sys.argv[2]),
                                    instance = sys.argv[3],
                                    rabbit_config=config["rabbitmq"])

    # Set logging config for this logger so that only its log messages are seen.
    monitor._l.setLevel(logging.DEBUG)
    monitor._l.addHandler(logging.FileHandler(log_file))

    monitor.setup()

    monitor.start()