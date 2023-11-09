import logging
import pickle

class BaseDataHandler:
    def __init__(self, pickle_path):
        self.pickle_path = pickle_path
        self.logger = logging.getLogger(self.__class__.__name__)

    def save_data(self, data):
        with open(self.pickle_path, 'wb') as file:
            pickle.dump(data, file)

    def load_data(self):
        try:
            with open(self.pickle_path,'rb') as file:
                return pickle.load(file)
        except FileNotFoundError as e:
            self.logger.error(f"No configuration found at {self.pickle_path}: {e}")
            raise
