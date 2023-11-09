import os
import smtplib
import logging
from email.message import EmailMessage
import DataHandler


logging.basicConfig(filename='Emailer.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger("emailer")





def send_email(subject, to_email, file_path):
    '''
    send the mail.
    mailserver should use SSL
    '''
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = DataHandler.user_data.get_address()
    msg['To'] = to_email

    logger.debug(msg)
    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    
    with smtplib.SMTP_SSL(DataHandler.user_data.get_mailserver(), DataHandler.user_data.get_mailport()) as smtp:
        smtp.login(DataHandler.user_data.get_address(), DataHandler.user_data.get_password()) 
        smtp.send_message(msg)


def main():
    email_dict = DataHandler.load_csv_to_dict(DataHandler.get_csvpath)
    logger.level = "DEBUG"
    for root, dirs, files in os.walk(DataHandler.get_dirpath):
        for file in files:
            file_name_without_ext = os.path.splitext(file)[0]
            if file_name_without_ext in email_dict:
                email = email_dict[file_name_without_ext]
                send_email(f"File {file} for you", email, os.path.join(root, file),"wkgusdl21@gmail.com")
                logger.info(f"Sent {file} to {email}")

if __name__ == "__main__":
    main()