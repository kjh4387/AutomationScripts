import logging
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, log_file, level=logging.INFO):
        self.logger = logging.getLogger('EmailAutomationLogger')
        self.logger.setLevel(level)

        # Create a file handler that logs messages to a file, with rotation
        handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=5)
        handler.setLevel(level)

        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)

    def log(self, message, level=logging.INFO):
        """ Log a message with the specified logging level """
        if level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)
        else:
            self.logger.info(message)


