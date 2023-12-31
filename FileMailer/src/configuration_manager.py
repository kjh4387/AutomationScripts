import keyring
import logging
import json
import os

from logger import Logger


# Here, we are assuming that the Logger class has been defined in the same file or is accessible in the environment.
# This would replace the previous ConfigurationManager class definition in the same file or module.

class ConfigurationManager:
    def __init__(self, config_file, logger):
        self.config_file = config_file
        self.config_data = {}
        self.logger = logger
        self.load_config()
        
    
    def save_subject(self, subject):
        self.set('email_subject', subject)
        self.save_config()

    def get_subject(self):
        return self.get('email_subject', default='Default Subject') 
        

    def load_config(self):
        """ Load configuration from a JSON file """
        try:
            with open(self.config_file, 'r') as file:
                self.config_data = json.load(file)
                self.logger.log("Configuration loaded successfully.")
        except FileNotFoundError:
            self.logger.log(f"No configuration file found at {self.config_file}. A new one will be created upon saving.", level=logging.WARNING)
            self.create_default_config()
        except json.JSONDecodeError as e:
            self.logger.log(f"Error decoding JSON from the configuration file: {e}", level=logging.ERROR)
            self.create_default_config()

    def save_config(self):
        """ Save configuration to a JSON file, excluding the password """
        try:
            # Remove the password before saving to file
            email_password = self.config_data.pop('smtp_password', None)
            
            with open(self.config_file, 'w') as file:
                json.dump(self.config_data, file, indent=4)
                self.logger.log("Configuration saved successfully.")
            
            # Restore the password in the current instance
        except Exception as e:
            self.logger.log(f"Failed to save configuration: {e}", level=logging.ERROR)


    def set_email_credentials(self, username, password):
        """ Set email username and save password securely in the keyring """
        self.config_data['smtp_user'] = username
        keyring.set_password('email_automation', username, password)

    def get_email_credentials(self):
        """ Get email credentials """
        username = self.config_data.get('smtp_user')
        password = keyring.get_password('email_automation', username)
        if password:
            return password
        else:
            return ""

    def get(self, key, default=None):
        """ Get a value from the configuration data. """
        return self.config_data.get(key, default)

    def get_config_path():
        return 'config.json'
    
    def create_default_config(self):
        """ Create a default configuration with essential settings """
        self.config_data = {
            "contact_data": "./contacts.csv",
            "department_data": "./departments.csv",
            "directory": "./test"
            
        }
        self.save_config()

    def set_current_template_path(self, template_path):
        """ Set the current template path in the configuration. """
        self.config_data['current_template_path'] = template_path
        self.save_config()

    def get_current_template_path(self):
        """ Get the current template path from the configuration. """
        return self.get('current_template_path')
    
    def set(self, key, value):
        """ Set a value in the configuration data and save the configuration. """
        self.config_data[key] = value
        self.save_config()  # Save changes after updating the configuration

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
    
    def get_email_config(self):
        return {
            'smtp_server': self.get('smtp_server',""),
            'smtp_port': self.get('smtp_port',""),
            'smtp_user': self.get('smtp_user',""),
            'smtp_password': self.get_email_credentials(),  # You might be using keyring for the password
            'use_tls': self.get('use_tls', True),

        }
if __name__ == "__main__":
    logger = Logger("log")
    defaultconfig = ConfigurationManager("config.json",logger)
    
    