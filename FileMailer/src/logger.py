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
        self.app = None

    def set_app(self, app):
        """ Set the reference to the Tkinter app. """
        self.app = app

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
        if self.app:
            formatted_message = self.format_message(message, level)
            self.app.log_message(formatted_message)


    def format_message(self, message, level):
        """ Format the message for display in the GUI. """
        level_name = logging.getLevelName(level)
        return f"{level_name}: {message}"