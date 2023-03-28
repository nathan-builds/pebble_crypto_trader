import logging
from constants.base_constants import Constants


class PebbleLogger():


    def __init__(self, log_name, console_enabled, file_enabled, file_path=None):
        self.log_name = log_name
        self.is_console_enabled = console_enabled
        self.is_file_enabled = file_enabled
        self.file_path = file_path

    def get_logger(self):
        logger = logging.getLogger(self.log_name)
        logger.setLevel(logging.INFO)

        if self.is_console_enabled:
            stream = logging.StreamHandler()
            stream_formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s -  %(message)s')
            stream.setFormatter(stream_formatter)
            logger.addHandler(stream)
        if self.is_file_enabled:
            file = logging.FileHandler(self.file_path)
            file_formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s -  %(message)s')
            file.setFormatter(file_formatter)
            logger.addHandler(file)
        return logger
