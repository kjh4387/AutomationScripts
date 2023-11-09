from .base_handler import BaseDataHandler
from config.paths import MAILCONFIG_PATH

class MailData(BaseDataHandler):
    def __init__(self):
        super().__init__(MAILCONFIG_PATH)
        self.mail_host = None
        self.mail_port = None

    def set_mail_server(self, host, port):
        self.mail_host = host
        self.mail_port = port
        self.save_data({
            'mail_host': self.mail_host,
            'mail_port': self.mail_port
        })

    def load_mail_server(self):
        data = self.load_data()
        self.mail_host = data.get('mail_host')
        self.mail_port = data.get('mail_port')
