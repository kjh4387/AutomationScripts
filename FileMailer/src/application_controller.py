# controller.py

from template_manager import TemplateManager
from csv_manager import DepartmentManager, ContactManager
from file_manager import FileManager
from email_manager import EmailManager
from configuration_manager import ConfigurationManager
from logger import Logger

class ApplicationController:
    def __init__(self, config_file,logger):
        self.logger = logger
        self.config_manager = ConfigurationManager(config_file, self.logger)

        # Load configurations
        contact_csv_file = self.config_manager.get('contact_csv_file')
        department_csv_file = self.config_manager.get('department_csv_file')

        self.contact_manager = ContactManager(contact_csv_file, self.logger)
        self.department_manager = DepartmentManager(department_csv_file, self.logger)
        
        # Load data from CSV files
        self.contact_manager.load()
        self.department_manager.load()

        # Initialize FileManager with the directory from the configuration
        default_directory = self.config_manager.get_default_directory()
        self.file_manager = FileManager(default_directory)
        
        # Initialize other managers
        self.template_manager = TemplateManager()
        self.email_manager = EmailManager(self.config_manager, self.logger)

    # Methods using CSVManager instances
    def get_contact(self, key):
        """Get contact details from ContactManager"""
        return self.contact_manager.get(key)
    
    def get_contact_email(self, department_code, name):
        return self.contact_manager.get_email_by_department_and_name(department_code, name)
    
    def get_department_name(self, department_code):
        return self.department_manager.get(department_code)
    
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
