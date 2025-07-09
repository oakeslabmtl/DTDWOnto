import logging
import logging.config
import sys
import time

import pandas as pd
from rabbitmq import Rabbitmq
import os

class CSVStreamer:
    def __init__(self, csv_file, rabbit_config):
        self._l = logging.getLogger("CSVStreamer")
        self.csv_file = csv_file
        self.rabbitmq = Rabbitmq(**rabbit_config)

    def setup(self):
        # Check if CSV file is available and throw error if not.
        if not os.path.exists(self.csv_file):
            self._l.error("CSV file not found: %s" % self.csv_file)
            raise FileNotFoundError("CSV file not found: %s" % self.csv_file)

        self.rabbitmq.connect_to_server()

    def start(self):
        # start_time = time.time()
        # Read CSV file using pandas and publish the data to RabbitMQ
        data = pd.read_csv(self.csv_file)
        self._l.info("Publishing data from CSV file: %s" % self.csv_file)
        total_rows = len(data)
        self._l.info(f"Data contains {total_rows} rows.")
        for index, row in data.iterrows():
            
            tb_message = {
                "measurement": "CSVStreamer",
                "time": row["time"],
                "tags": {
                    "source": "CSVStreamer"
                },
                "fields": {
                    "out_angle": row["{TestBench}.tb.out_angle"],
                    "out_speed": row["{TestBench}.tb.out_speed"],
                    "out_acceleration": row["{TestBench}.tb.out_acceleration"],
                }
            }
            
            dut_message = {
                "measurement": "CSVStreamer",
                "time": row["time"],
                "tags": {
                    "source": "CSVStreamer"
                },
                "fields": {
                    "out_torque": row["{Dut}.dut.out_torque"],
                    "out_acceleration": row["{Dut}.dut.out_acceleration"],
                    "out_speed": row["{Dut}.dut.out_speed"],
                    "out_angle": row["{Dut}.dut.out_angle"],
                }
            }

            set_input_message = {
                "measurement": "CSVStreamer",
                "time": row["time"],
                "tags": {
                    "source": "CSVStreamer"
                },
                "fields": {
                    "y": row["{SetInput}.in_dut.y"],
                }
            }

            self.rabbitmq.send_message("dut.output", dut_message)
            self.rabbitmq.send_message("testbench.output", tb_message)
            self.rabbitmq.send_message("in_dut.output", set_input_message)

            self._l.info(f"Message for row {index}/{total_rows} sent.")

    def stop(self):
        self.rabbitmq.close()

if __name__ == "__main__":
    from pyhocon import ConfigFactory
    
    # Clear log file for monitor
    with open("csv_streamer.log", "w"):
        pass

    # Set logging
    logging.basicConfig(level=logging.INFO, filename="csv_streamer.log")

    # Start service

    config = ConfigFactory.parse_file("service.conf")

    service = CSVStreamer(csv_file=sys.argv[1], rabbit_config=config["rabbitmq"])

    service.setup()

    try: 
        service.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        service.stop()
        sys.exit(0)
