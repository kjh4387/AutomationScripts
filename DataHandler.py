import logging
import pickle
import keyring
import Pathes
import re
import csv

logger = logging.getLogger("DataHandler")

class user_data:
    service_id = 'email_automation'
    address = None

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
        self.password = address
        self.save_data()


    def put_password(self,password):
        try:
            keyring.delete_password(self.service_id, self.address)
        finally:
            self.address = password
        self.save_data()
        

    def save_data(self):
        if self.address and self.password is not None:
            user_data = {
                'address':self.address,
            }
            with open(Pathes.userdata_path, 'wb') as file:
                pickle.dump(user_data,file)
            keyring.set_password(self.service_id,self.address,self.password)
        '''else:
            raise ValueError'''
        

    def load_data(self):
        try:
            with open(Pathes.userdata_path,'rb') as file:
                loaded_data = pickle.load(file)
                self.address = loaded_data.get('address')
            self.password = keyring.get_password(self.service_id, self.address)
        except:
            raise Exception("UserDataNotExist")
        

class mail_data():
    mail_host = None
    mail_port = None
    def get_mailhost(self):
        if self.mail_host is None:
            raise ValueError
        else:
            return self.mail_host
    
    def get_mailport(self):
        if self.mail_port is None:
            raise 465
        else:
            return self.mail_port

    def put_mailhost(self, hostname):
        self.mail_host = hostname
        
    def put_mailport(self, port_number):
        if is_valid_port(port_number):
            self.mail_port = port_number
        else:
            raise ValueError
        self.save_data()

    def save_data(self):
        if self.mail_host and self.mail_port is not None:
            mail_config = {
                'mail_host':self.mail_host,
                'mail_port':self.mail_port,
            }
            with open(Pathes.mailconfig_path, 'wb') as file:
                pickle.dump(mail_config,file)
        else:
            raise ValueError
    
    def load_data(self):
        try:
            with open(Pathes.mailconfig_path,'rb') as file:
                loaded_data = pickle.load(file)
                self.mail_host = loaded_data.get('mail_host')
                self.mail_port = loaded_data.get('mail_port')
        except:
            raise Exception("MailConfigNotExist")

        


class mail_template():
    postingperiod = ''
    manager = ''

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


    def get_department(self, codename):
        '''
        진료과 코드가 포함된 이름을 입력하면 departmentlist에서 해당하는 진료과명을 찾아 반환합니다.
        ex) GS홍길동 -> 일반외과
        '''
        code = extract_english(codename)
        dict = load_csv_to_dict(Pathes.departmentlist_path)
        if code in dict:
            return dict[code]
        else:
            raise ValueError
        
    def get_postingperiod(self):
        return self.postingperiod
    
    def put_postingperiod(self, period):
        self.postingperiod = period
        self.save_templatedata()

    def get_manager(self):
        return self.manager
    
    def put_manager(self,manager):
        self.manager = manager
        self.save_templatedata()

    def save_templatedata(self):
        if self.postingperiod and self.manager is not None:
            template_config = {
                'postingperiod':self.postingperiod,
                'manager':self.manager,
            }
            with open(Pathes.template_variable_path, 'wb') as file:
                pickle.dump(template_config,file)
        else:
            raise ValueError
    
    def load_templatedata(self):
        try:
            with open(Pathes.template_variable_path_path,'rb') as file:
                loaded_data = pickle.load(file)
                self.postingperiod = loaded_data.get('postingperiod')
                self.manager = loaded_data.get('manager')
        except:
            raise Exception("templateConfigNotExist")
        

        

    
        



def extract_english(text):
    return ''.join([char for char in text.strip() if 'a' <= char <= 'z' or 'A' <= char <= 'Z'])


def load_csv_to_dict(csv_path):
    email_dict = {}
    try:
        with open(csv_path, mode='r') as infile:
            reader = csv.reader(infile)
            email_dict = {rows[0].strip() :rows[1].strip() for rows in reader}
            logger.debug(email_dict)
            
    except FileNotFoundError:
        # If the file doesn't exist, create an empty one
        with open(csv_path, mode='w') as outfile:
            writer = csv.writer(outfile)
            # You can write headers here if needed
            # For example: writer.writerow(['filename', 'email'])
        logger.warning(f"{csv_path} not found. An empty CSV file has been created. please fill up the file.")

    logger.debug(email_dict)
    logger.info("email data done!")
    return email_dict


def is_valid_hostname(hostname):
    # A simple regex pattern for a basic FQDN check
    pattern = re.compile(r'^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$')
    return pattern.match(hostname) is not None

def is_valid_port(port):
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except ValueError:
        return False


def get_dirpath():
    #will changed to GUI function.
    return "./attatchment_files"

def get_csvpath():
    #will changed to GUI function
    return "./emaillist.csv"

if __name__ == "__main__":
    test = user_data()
    test.put_address("123")

