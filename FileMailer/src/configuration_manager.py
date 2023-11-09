import keyring
import logging
import json
from .logger import Logger


# Here, we are assuming that the Logger class has been defined in the same file or is accessible in the environment.
# This would replace the previous ConfigurationManager class definition in the same file or module.

class ConfigurationManager:
    def __init__(self, config_file, log_file='config_manager.log'):
        self.config_file = config_file
        self.config_data = {}
        self.logger = Logger(log_file)

    def load_config(self):
        """ Load configuration from a JSON file """
        try:
            with open(self.config_file, 'r') as file:
                self.config_data = json.load(file)
                self.logger.log("Configuration loaded successfully.")
        except FileNotFoundError:
            self.logger.log(f"No configuration file found at {self.config_file}. A new one will be created upon saving.", level=logging.WARNING)
        except json.JSONDecodeError as e:
            self.logger.log(f"Error decoding JSON from the configuration file: {e}", level=logging.ERROR)

    def save_config(self):
        """ Save configuration to a JSON file, excluding the password """
        try:
            # Remove the password before saving to file
            email_username = self.config_data.pop('email_username', None)
            email_password = self.config_data.pop('email_password', None)
            
            with open(self.config_file, 'w') as file:
                json.dump(self.config_data, file, indent=4)
                self.logger.log("Configuration saved successfully.")
            
            # Restore the password in the current instance
            if email_username:
                self.config_data['email_username'] = email_username
            if email_password:
                self.config_data['email_password'] = email_password
        except Exception as e:
            self.logger.log(f"Failed to save configuration: {e}", level=logging.ERROR)


    def set_email_credentials(self, username, password):
        """ Set email username and save password securely in the keyring """
        self.config_data['email_username'] = username
        keyring.set_password('email_automation', username, password)

    def get_email_credentials(self):
        """ Get email credentials """
        username = self.config_data.get('email_username')
        password = keyring.get_password('email_automation', username)
        return username, password

# Example usage:
config_manager = ConfigurationManager('config.json')
config_manager.load_config()  # Load the configuration file

# Set email credentials
config_manager.set_email_credentials('user@example.com', 'securepassword')

# Save the configuration to file
config_manager.save_config()

# Get email credentials
username, password = config_manager.get_email_credentials()
print(f"Email username: {username}")
print(f"Email password: {'*' * len(password)}")  # For security reasons, don't print the actual password