import logging
import os
import sys


def configure_logger():
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    log_filename = "logs/output.log"
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)

    output_file_handler = logging.FileHandler(log_filename)
    output_file_handler.setFormatter(log_formatter)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(log_formatter)

    log.addHandler(output_file_handler)
    log.addHandler(stdout_handler)
