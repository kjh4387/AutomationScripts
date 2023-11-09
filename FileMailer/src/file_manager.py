
import os
import re

class FileManager:
    def __init__(self, logger, directory=None,):
        self.directory = directory if directory else ""
        self.logger = logger

    def update_directory(self, new_directory):
        """Updates the current working directory."""
        if os.path.isdir(new_directory):
            self.directory = new_directory
        else:
            raise ValueError(f"The directory {new_directory} does not exist.")

    def list_files(self):
        """Returns a list of file names in the current directory."""
        if not self.directory:
            raise ValueError("No directory has been set to list files from.")
        try:
            return [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
        except FileNotFoundError as e:
            # Handle the error appropriately, such as logging it and returning an empty list
            self.logger(f"Error listing files: {e}")
            return []

    def get_file_info(self, filename):
        """Extracts and returns information from a given filename."""
        # Use a regular expression to split the filename into department code and name
        match = re.match(r'([A-Z]+)([\uAC00-\uD7A3]+)', filename)
        if match:
            department, receiver = match.groups()
            return {'department_code': department, 'receiver': receiver}
        else:
            # Handle the case where the filename doesn't match the expected format
            return {'department_code': '', 'receiver': ''}

