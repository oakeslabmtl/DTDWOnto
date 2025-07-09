import logging
import logging.config
from utils import log_assert
from rabbitmq import Rabbitmq

class DUTMonitorService:
    def __init__(self, rabbit_config):
        self._l = logging.getLogger("DUTMonitor")
        self.rabbitmq = Rabbitmq(**rabbit_config)

        self.dut_output_data = None
        self.testbench_output_data = None


    def setup(self):
        self.rabbitmq.connect_to_server()

        self.rabbitmq.subscribe(routing_key="dut.output",
                                on_message_callback=self.data_in, queue_name="dut_monitor")
        self.rabbitmq.subscribe(routing_key="testbench.output",
                                on_message_callback=self.data_in, queue_name="dut_monitor")
        

    def start(self):
        self.rabbitmq.start_consuming()

    def data_in(self, ch, method, properties, body_json):
        if method.routing_key == "dut.output":
            self._l.debug(f"Received DUT output: {body_json}.")
            log_assert(self._l, self.dut_output_data is None, f"DUT output already received: {self.dut_output_data}.")
            self.dut_output_data = body_json
        elif method.routing_key == "testbench.output":
            self._l.debug(f"Received TB output: {body_json}.")
            log_assert(self._l, self.testbench_output_data is None, f"TB output already received: {self.testbench_output_data}.")
            self.testbench_output_data = body_json
            if self.testbench_output_data is not None and self.dut_output_data is not None:
                self.do_computation()
                self.testbench_output_data = None
                self.dut_output_data = None
        else:
            log_assert(self._l, False, f"Unknown routing key: {method.routing_key}.")

    def do_computation(self):
        # Check timestamps are aligned
        log_assert(self._l, self.dut_output_data["time"] == self.testbench_output_data["time"], f"Timestamps not aligned: {self.dut_output_data['time']} != {self.testbench_output_data['time']}.")

        self.timestamp = self.dut_output_data["time"]

        # Compute stuff
        self.out_conformance = 0.0

        self.publish_state()
        
    def publish_state(self):
        message = {
            "measurement": "DUTMonitor",
            "time": self.timestamp,
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
    with open("monitor.log", "w"):
        pass

    # Set logging
    logging.basicConfig(level=logging.DEBUG, filename="dut_monitor.log")
    
    # Start DUTMonitorService
    
    config = ConfigFactory.parse_file("service.conf")

    monitor = DUTMonitorService(rabbit_config=config["rabbitmq"])

    monitor.setup()

    monitor.start()
