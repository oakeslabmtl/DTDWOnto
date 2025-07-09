import csv
from datetime import datetime
import logging
import logging.config
import sys
from utils import log_assert
from rabbitmq import Rabbitmq

class CSVRecorder:
    def __init__(self, csv_file_path, 
                 topics_to_subscribe, rabbit_config):    
        self._l = logging.getLogger("CSVRecorder")
        self.rabbitmq = Rabbitmq(**rabbit_config)
        self.csv_file_path = csv_file_path

        log_assert(self._l, len(set(topics_to_subscribe)) == len(topics_to_subscribe), "Topics to subscribe must be unique.")

        self.topics_to_subscribe = topics_to_subscribe
        
        self.number_records = 0
        self.header_written = False
        self.current_file = None
        self.csv_writer = None
        self.data_per_topic_before_writting_to_file = {}

    def read_state(self, ch, method, properties, body_json):
        self._l.debug("New msg:")
        self._l.debug(body_json)

        log_assert(self._l, method.routing_key in self.topics_to_subscribe, f"Received unexpected topic {method.routing_key}.")
        
        if method.routing_key not in self.data_per_topic_before_writting_to_file:
            # Record message into the data.
            self.data_per_topic_before_writting_to_file[method.routing_key] = body_json
        else:
            # This is not expected, given the ordering of the messages.
            log_assert(self._l, False, f"Received unexpected message from {method.routing_key}. Current state of the data is {self.data_per_topic_before_writting_to_file}.")

        if len(self.data_per_topic_before_writting_to_file) == len(self.topics_to_subscribe):
            
            if len(self.data_per_topic_before_writting_to_file) == len(self.topics_to_subscribe) and not self.header_written:
                self._l.debug("Writing header.")
                header = ["time"]
                for k in self.data_per_topic_before_writting_to_file.keys():
                    for field in self.data_per_topic_before_writting_to_file[k]["fields"]:
                        header.append(field)
                self.csv_writer.writerow(header)
                self.header_written = True


            timestamp = self.data_per_topic_before_writting_to_file[self.topics_to_subscribe[0]]["time"]
            for k in self.data_per_topic_before_writting_to_file.keys():
                other_timestamp = self.data_per_topic_before_writting_to_file[k]["time"]
                log_assert(self._l, timestamp == other_timestamp, f"Timestamps do not match: {timestamp} != {other_timestamp}. Current state of the data is {self.data_per_topic_before_writting_to_file}." )
            # Write to file
            self._l.debug(f"Writting to file.")
            values = [timestamp]
            for k in self.data_per_topic_before_writting_to_file.keys():
                for field in self.data_per_topic_before_writting_to_file[k]["fields"]:
                    values.append(self.data_per_topic_before_writting_to_file[k]["fields"][field])
            self.csv_writer.writerow(values)
            self.current_file.flush()
            self.number_records += 1

            self.data_per_topic_before_writting_to_file = {}

            self._l.debug(f"number_records={self.number_records}")

    def setup(self):
        self._l.debug(f"New file in {self.csv_file_path}.")
        self.current_file = open(self.csv_file_path, 'w', newline='')
        self.csv_writer = csv.writer(self.current_file)
        self.number_records = 0
        self.header_written = False

        self.rabbitmq.connect_to_server()

        for t in self.topics_to_subscribe:
            self.rabbitmq.subscribe(routing_key=t,
                                    on_message_callback=self.read_state,
                                    queue_name="csv_recorder")

    def start(self):
        self.rabbitmq.start_consuming()

    def stop(self):
        log_assert(self._l, len(self.data_per_topic_before_writting_to_file) == 0, f"Data not written to file: {self.data_per_topic_before_writting_to_file}.")
        log_assert(self._l, self.current_file is not None, "No file to close.")
        self.current_file.flush()
        self.current_file.close()
    
        self.rabbitmq.close()

if __name__ == "__main__":
    from pyhocon import ConfigFactory
    import os
    
    # Clear log file for monitor
    with open("csv_recorder.log", "w"):
        pass

    # Set logging
    logging.basicConfig(level=logging.INFO, filename="csv_recorder.log")
    
    # Start CSVRecorder
    config = ConfigFactory.parse_file("service.conf")

    service = CSVRecorder(csv_file_path=sys.argv[1], 
                 topics_to_subscribe=["dut_monitor.output"], rabbit_config=config["rabbitmq"])

    service.setup()

    service.start()