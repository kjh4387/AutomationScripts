import os
import csv
import smtplib
import logging
from email.message import EmailMessage

# Constants
DIR_PATH = "path_to_directory" # Provide the path to the directory
CSV_PATH = "database.csv" # Provide the path to the CSV file

logger = logging.getLogger("emailer")

def load_csv_to_dict(csv_path):
    email_dict = {}
    with open(csv_path, mode='r') as infile:
        reader = csv.reader(infile)
        email_dict = {rows[0]:rows[1] for rows in reader}
        logger.debug(email_dict)
    logger.info("email data done!")
    return email_dict

def send_email(subject, to_email, file_path, sender_address, sender_password, mailserver = 'smtp.gmail.com', mailport = '465'):
    '''
    send the mail.
    mailserver should use SSL
    '''
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "your_email@gmail.com"
    msg['To'] = to_email

    logger.debug(msg)
    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    
    with smtplib.SMTP_SSL(mailserver, mailport) as smtp:
        smtp.login(sender_address, sender_password) 
        smtp.send_message(msg)

def main():
    email_dict = load_csv_to_dict(CSV_PATH)

    for root, dirs, files in os.walk(DIR_PATH):
        for file in files:
            file_name_without_ext = os.path.splitext(file)[0]
            if file_name_without_ext in email_dict:
                email = email_dict[file_name_without_ext]
                send_email(f"File {file} for you", email, os.path.join(root, file))
                print(f"Sent {file} to {email}")

if __name__ == "__main__":
    main()