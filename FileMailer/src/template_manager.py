import logging

class TemplateManager:
    def __init__(self, template_file, logger):
        self.template_file = template_file
        self.logger = logger
        self.template_content = ""

    def load_template(self):
        """ Load the email template from a file """
        try:
            with open(self.template_file, 'r', encoding='utf-8') as file:
                self.template_content = file.read()
                self.logger.log("Email template loaded successfully.", level=logging.INFO)
        except FileNotFoundError:
            self.logger.log(f"Template file {self.template_file} not found.", level=logging.ERROR)
        except Exception as e:
            self.logger.log(f"An error occurred while loading the template: {e}", level=logging.ERROR)

    def render(self, **kwargs):
        """ Populate the template with given data """
        try:
            return self.template_content.format(**kwargs)
        except KeyError as e:
            self.logger.log(f"Missing a value for the key in the template: {e}", level=logging.ERROR)
            return None
        except Exception as e:
            self.logger.log(f"An error occurred while rendering the template: {e}", level=logging.ERROR)
            return None


