import os

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
        """ Prepare the template by replacing placeholders with actual values. """
        try:
            return template_content.format(**kwargs)
        except KeyError as e:
            self.logger.log(f"Missing a placeholder in the template: {e}", level='ERROR')
            return None
        except Exception as e:
            self.logger.log(f"An error occurred while preparing the template: {e}", level='ERROR')
            return None
