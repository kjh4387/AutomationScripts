import os
import string
import re

class SafeFormatter(string.Formatter):
        def get_value(self, key, args, kwds):
            if isinstance(key, str):
                return kwds.get(key, '{' + key + '}')
            else:
                return super().get_value(key, args, kwds)

class TemplateManager:
    def __init__(self, template_directory, logger):
        self.template_directory = template_directory
        self.logger = logger

    def load_template(self, template_name):
        """ Load a template from a file. """
        template_path = os.path.join(self.template_directory, template_name)
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            self.logger.log(f"Template file {template_name} not found.", level='ERROR')
            return None
        except Exception as e:
            self.logger.log(f"An error occurred while loading the template: {e}", level='ERROR')
            return None

    def save_template(self, template_path, content):
        """ Save a template to a file. """
        try:
            with open(template_path, 'w', encoding='utf-8') as file:
                file.write(content)
            self.logger.log(f"Template {template_path} saved successfully.", level='INFO')
            return True
        except Exception as e:
            self.logger.log(f"An error occurred while saving the template: {e}", level='ERROR')
            return False

    def prepare_template(self, template_content, **kwargs):
        """ Prepare the template by replacing placeholders with actual values or leaving them if missing. """
        formatter = SafeFormatter()
        try:
            return formatter.format(template_content, **kwargs)
        except Exception as e:
            self.logger.log(f"An error occurred while preparing the template: {e}", level='ERROR')
            return None

    def find_placeholders(self, template_content):
        """Find placeholders within the template content."""
        placeholders = re.findall(r'\{(\w+)\}', template_content)
        return list(set(placeholders))  # Remove duplicates
    