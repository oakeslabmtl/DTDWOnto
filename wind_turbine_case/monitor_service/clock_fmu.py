import logging
import logging.config
import sys
import time

import pandas as pd
from rabbitmq import Rabbitmq
import os

class ClockCSV:
    def __init__(self, csv_file, rabbit_config):
        self._l = logging.getLogger("ClockCSV")
        self.csv_file = csv_file
        self.rabbitmq = Rabbitmq(**rabbit_config)

    def setup(self):
        # Check if CSV file is available and throw error if not.
        if not os.path.exists(self.csv_file):
            self._l.error("CSV file not found: %s" % self.csv_file)
            raise FileNotFoundError("CSV file not found: %s" % self.csv_file)

        self.rabbitmq.connect_to_server()

    def start(self):
        # Read CSV file using pandas and publish the data to RabbitMQ
        data = pd.read_csv(self.csv_file)
        self._l.info("Publishing data from CSV file: %s" % self.csv_file)
        total_rows = len(data)
        self._l.info(f"Data contains {total_rows} rows.")
        for index, row in data.iterrows():
            
            message = {
                "measurement": "ClockCSV",
                "time": row["time"],
                "tags": {
                    "source": "ClockCSV"
                }
            }
            
            self.rabbitmq.send_message("clock.output", message)

            self._l.info(f"Message for row {index}/{total_rows} sent.")

    def stop(self):
        self.rabbitmq.close()

if __name__ == "__main__":
    from pyhocon import ConfigFactory
    
    # Clear log file for monitor
    log_file = "clock_csv.log"

    with open(log_file, "w"):
        pass

    # Start service
    config = ConfigFactory.parse_file("service.conf")

    service = ClockCSV(csv_file=sys.argv[1], rabbit_config=config["rabbitmq"])

    # Set logging config for this logger so that only its log messages are seen.
    service._l.setLevel(logging.DEBUG)
    service._l.addHandler(logging.FileHandler(log_file))

    service.setup()

    try: 
        service.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        service.stop()
        sys.exit(0)
