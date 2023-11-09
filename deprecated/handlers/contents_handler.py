from .base_handler import BaseDataHandler
from config.paths import TEMPLATE_VARIABLES_PATH

class MailTemplate(BaseDataHandler):
    def __init__(self):
        super().__init__(TEMPLATE_VARIABLES_PATH)
        self.posting_period = None
        self.manager = None
        self.template = None

    def set_template_data(self, template):
        self.template = template

    def load_template_data(self):
        data = self.load_data()
        self.posting_period = data.get('posting_period')
        self.manager = data.get('manager')
