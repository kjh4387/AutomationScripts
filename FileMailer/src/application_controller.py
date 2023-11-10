# controller.py

from template_manager import TemplateManager
from csv_manager import DepartmentManager, ContactManager
from file_manager import FileManager
from email_manager import EmailManager
from configuration_manager import ConfigurationManager


class ApplicationController:
    
    def __init__(self, config_file,logger):
        self.logger = logger
        self.config_manager = ConfigurationManager(config_file, self.logger)
        self.load_data()

        # Load configurations
        contact_csv_file = self.config_manager.get('contact_data')
        department_csv_file = self.config_manager.get('department_data')

        template_directory = self.config_manager.get('template_directory')
        self.template_manager = TemplateManager(template_directory, self.logger)

        self.contact_manager = ContactManager(contact_csv_file, self.logger)
        self.department_manager = DepartmentManager(department_csv_file, self.logger)
        
        # Load data from CSV files
        self.contact_manager.load()
        self.department_manager.load()

        # Initialize FileManager with the directory from the configuration
        directory = self.config_manager.get("directory")
        self.file_manager = FileManager(self.logger, directory)
        
        # Initialize other managers
        self.template_manager = TemplateManager(self.config_manager.get('template_path'),self.logger)
        self.email_manager = EmailManager(self.config_manager, self.logger)


    def load_data(self):
        """load json and set to data"""
        self.config_manager

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
    
    def get_current_template_path(self):
        """ Get the current template path from ConfigurationManager. """
        return self.config_manager.get_current_template_path()
    
    def get_all_contacts(self):
        """Retrieve a list of all contacts in the format 'DEPTCodeName: Email'."""
        try:
            # Assuming ContactManager has a method called get_all that returns a dictionary
            # where the keys are 'DEPTCodeName' and the values are 'Email'
            contacts_dict = self.contact_manager.get_all()
            # Format the contact information for display in the GUI
            contacts_list = [f"{dept_code_name}: {email}" for dept_code_name, email in contacts_dict.items()]
            return contacts_list
        except Exception as e:
            self.logger.log(f"Failed to retrieve contacts: {e}", level='ERROR')
            return []
        
    def import_contacts_from_csv(self, csv_path):
        try:
            # Assuming ContactManager has an import method
            self.contact_manager.import_from_csv(csv_path)
            self.logger.log("Contacts imported successfully.", level='INFO')
            return True
        except Exception as e:
            self.logger.log(f"Failed to import contacts: {e}", level='ERROR')
            return False

    def add_contact(self, contact_details):
        # Logic to add a new contact
        self.contact_manager.add(contact_details['name'], contact_details['email'])
        self.contact_manager.save()

    def edit_contact(self, original_name, contact_details):
        # Logic to edit an existing contact
        self.contact_manager.update(original_name, contact_details['email'])
        self.contact_manager.save()

    def delete_contact(self, contact_name):
        # Logic to delete an existing contact
        self.contact_manager.delete(contact_name)
        self.contact_manager.save()

    def save_contacts(self):
        # Logic to save all contacts
        self.contact_manager.save()

    def get_all_departments(self):
        """Retrieve a list of all departmens in the format 'DEPTCode: name'."""
        try:

            departments_dict = self.department_manager.get_all()
            # Format the contact information for display in the GUI
            departments_list = [f"{code}: {name}" for code, name in departments_dict.items()]
            return departments_list
        except Exception as e:
            self.logger.log(f"Failed to retrieve departments: {e}", level='ERROR')
            return []

    def add_department(self, department_detailes):
        # Adds a new department
        self.department_manager.add(department_detailes['code'], department_detailes['name'])
        self.department_manager.save()
    
    def edit_department(self, original_name, department_details):
        # Logic to edit an existing contact
        self.department_manager.update(original_name, department_details['name'])
        self.department_manager.save()

    def save_department(self):
        # Logic to save all contacts
        self.department_manager.save()

    def delete_department(self, department_name):
        # Logic to delete an existing contact
        self.department_manager.delete(department_name)
        self.department_manager.save()

    def import_departments_from_csv(self, csv_path):
        try:
            # Assuming ContactManager has an import method
            self.department_manager.import_from_csv(csv_path)
            self.logger.log("Departments imported successfully.", level='INFO')
            return True
        except Exception as e:
            self.logger.log(f"Failed to import departments: {e}", level='ERROR')
            return False
    # More methods will be added here to handle other actions like sending emails,
    # managing contacts, managing departments, etc.
