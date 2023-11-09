# controller.py

from template_manager import TemplateManager
from csv_manager import DepartmentManager, ContactManager
from file_manager import FileManager
from email_manager import EmailManager
from configuration_manager import ConfigurationManager
from logger import Logger

class ApplicationController:
    def __init__(self):
        # Configuration for the application, if there's a specific directory to start with, it can be passed here.
        self.configuration_manager = ConfigurationManager("./config")
        self.logger = Logger()
        
        # Start with an empty or default path if you have one
        default_path = self.configuration_manager.get('default_path', '')
        self.file_manager = FileManager(default_path)
        
        self.template_manager = TemplateManager()
        self.email_manager = EmailManager(self.configuration_manager, self.logger)
        self.contact_manager = ContactManager(self.configuration_manager, self.logger)
        self.department_manager = DepartmentManager(self.configuration_manager, self.logger)

    def update_file_directory(self, new_directory):
        # Update the directory in file manager and possibly refresh the file list
        try:
            self.file_manager.update_directory(new_directory)
            self.logger.log(f"Directory updated to {new_directory}")
            return True
        except ValueError as e:
            self.logger.log(f"Failed to update directory: {e}")
            return False

    def get_file_list(self):
        # Retrieve the file list from the file manager
        try:
            files = self.file_manager.list_files()
            return files
        except ValueError as e:
            self.logger.log(f"Failed to list files: {e}")
            return []

    def get_file_details(self, filename):
        return self.file_manager.get_file_info(filename)

    # More methods will be added here to handle other actions like sending emails,
    # managing contacts, managing departments, etc.
