import logging
import pickle
import keyring
import Pathes

logger = logging.getLogger(__name__)

class user_data:
    service_id = 'email_automation'
    address = ''
    mail_server = ''
    mail_port = ''

    def __init__(self):
        with open(Pathes.userdata_path, 'rb') as file:
            loaded_data = pickle.load(file)

    def get_address(self):
        if self.address is None:
            raise ValueError
        else:
            return self.address

    def get_password(self):
        try:
            password = keyring.get_password(self.service_id, self.address)
            if password is None:
                raise ValueError
            else:
                return password
        except Exception as e:
            logger.error("An error occurred while retrieving password. {e}")
            logger.error("contact to developer with log file. ")
            raise SyntaxError


    def put_address(self,address):
        try:
            keyring.delete_password(self.service_id, self.address)
        finally:
            self.address = address


    def put_password(self,password):
        self.password = password
        

    def save_userdata(self):
        if self.address and self.mail_server and self.mail_port and self.password is not None:
            user_data = {
                'address':self.address,
                'mail_server':self.mail_server,
                'mail_port':self.mail_port,
            }
            with open(Pathes.userdata_path, 'wb') as file:
                pickle.dump(user_data,file)
            keyring.set_password(self.service_id,self.address,self.password)
        else:
            raise ValueError
        

    def load_data(self):
        try:
            with open(Pathes.userdata_path,'rb') as file:
                loaded_data = pickle.load(file)
                self.address = loaded_data.get('address')
            self.password = keyring.get_password(self.service_id, self.address)
        except:
            raise Exception("UserDataNotExist")
        

class mail_data():
    mail_server = None
    mail_port = None
    #서버와 포트 관련된 코드(get, set, save, load) 제작 필요


class mail_content:

    def get_mailserver(self):
        return self.mail_server

    def get_mailport(self):
        return self.mail_port


def get_dirpath():
    #will changed to GUI function.
    return "./attatchment_files"

def get_csvpath():
    #will changed to GUI function
    return "./emaillist.csv"

class mail_template():
    #템플릿 세팅 및 직렬화 기능 미완성. 구현 필요
    #template = get_template()

    def get_template(self):
        '''
        template이 txt file이기 때문에, template을 string으로 변환하기 위해 사용합니다.
        '''
        template = ''
        try:
            with open(Pathes.template_path, 'r') as f:
                while True:
                    line = f.readline()
                    if not line: break
                    template = template + line
                logger.debug(template)
                f.close()
                return template
        except FileNotFoundError:
            return None


    def get_mail_content(self,department,postingperiod,manager):
        '''
        template을 로드하고 포함된 가변 값을 세팅합니다.
        '''
        # Get the template from the user
        template = input(self.get_template())
        # Replace placeholders with actual values
        mail_content = template.format(department , postingperiod, manager)
        return mail_content


