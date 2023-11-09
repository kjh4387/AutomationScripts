import logging
import csv
    

class CSVManager:
    def __init__(self, csv_file, logger):
        self.csv_file = csv_file
        self.data = {}
        self.logger = logger

    def load(self):
        """ Load data from a CSV file """
        try:
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                self.data = {rows[0]: rows[1] for rows in reader}
                self.logger.log(f"{self.__class__.__name__} data loaded successfully.", level=logging.INFO)
        except FileNotFoundError:
            self.logger.log(f"{self.csv_file} not found.", level=logging.ERROR)
        except Exception as e:
            self.logger.log(f"An error occurred while loading data: {e}", level=logging.ERROR)

    def save(self):
        """ Save data to a CSV file """
        try:
            with open(self.csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for key, value in self.data.items():
                    writer.writerow([key, value])
                self.logger.log(f"{self.__class__.__name__} data saved successfully.", level=logging.INFO)
        except Exception as e:
            self.logger.log(f"An error occurred while saving data: {e}", level=logging.ERROR)

    def get(self, key):
        """ Get data for a given key """
        return self.data.get(key)

    def add(self, key, value):
        """ Add new data """
        self.data[key] = value
        self.logger.log(f"Added {key}: {value} to {self.__class__.__name__}.", level=logging.INFO)

    def update(self, key, value):
        """ Update existing data """
        if key in self.data:
            self.data[key] = value
            self.logger.log(f"Updated {key} to {value} in {self.__class__.__name__}.", level=logging.INFO)

    def delete(self, key):
        """ Delete data """
        if key in self.data:
            del self.data[key]
            self.logger.log(f"Deleted {key} from {self.__class__.__name__}.", level=logging.INFO)

    def search(self, search_term):
        """ Search for data by key or value """
        return {key: value for key, value in self.data.items() if search_term.lower() in key.lower() or search_term.lower() in value.lower()}

class DepartmentManager(CSVManager):
    # Inherits all methods from CSVManager
    # Additional department-specific methods can be added here
    pass

class ContactManager(CSVManager):
    # Inherits all methods from CSVManager
    # Additional contact-specific methods can be added here
    pass


