import keyring
from .base_handler import BaseDataHandler
from config.paths import USERDATA_PATH

class UserData(BaseDataHandler):
    def __init__(self, address=None):
        super().__init__(USERDATA_PATH)
        self.service_id = 'email_automation'
        self.address = address

    def get_password(self):
        return keyring.get_password(self.service_id, self.address)

    def set_credentials(self, address, password):
        self.address = address
        keyring.set_password(self.service_id, self.address, password)
        self.save_data({'address': self.address})

    def load_credentials(self):
        data = self.load_data()
        self.address = data.get('address')
        if self.address:
            self.password = self.get_password()
