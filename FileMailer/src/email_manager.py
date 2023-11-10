import os
import smtplib
import logging

import time

import socket

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class EmailManager:
    def __init__(self, config_manager, logger):
        self.config_manager = config_manager
        self.logger = logger
        self.update_config()

    def update_config(self):
        """ Update the SMTP settings from the configuration manager. """


    def send_email(self, recipient, subject, body, attachments=None):
        """ Send an email with the given parameters """
        email_config = self.config_manager.get_email_config()
        message = MIMEMultipart()
        message['From'] = email_config['smtp_user']
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Add attachments if provided
        if attachments:
            part = MIMEBase('application', 'octet-stream')
            try:
                with open(attachments, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachments)}")
                message.attach(part)
            except Exception as e:
                self.logger.log(f"Failed to attach file {attachments}: {e}", level=logging.ERROR)



            try:
                with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                    server.starttls()
                    server.login(email_config['smtp_user'], email_config['smtp_password'])
                    server.send_message(message)
                self.logger.log(f"Email sent to {recipient}", level=logging.INFO)
            except smtplib.SMTPAuthenticationError:
                self.logger.log("SMTP Authentication failed. Check username/password.", level=logging.ERROR)
                raise smtplib.SMTPAuthenticationError("SMTP Authentication failed. Check username/password.")
            except smtplib.SMTPException as e:
                self.logger.log(f"SMTP error when sending email to {recipient}: {e}", level=logging.ERROR)
                raise smtplib.SMTPException(f"SMTP error when sending email to {recipient}: {e}")
            except Exception as e:
                self.logger.log(f"Failed to send email to {recipient}: {e}", level=logging.ERROR)
                raise Exception(f"Failed to send email to {recipient}: {e}")
    '''
    async def _attempt_send(self, message):
        """ A helper coroutine that attempts to send the email message once. """
        source_address = "localhost"
        try:
            async with aiosmtplib.SMTP(hostname=self.config_manager.config_data["smtp_server"],
                               port=int(self.config_manager.config_data["smtp_port"]),
                               source_address=source_address) as server:
                await server.connect()
                await server.starttls()
                await server.login(self.config_manager.config_data["smtp_user"], self.config_manager.config_data["smtp_password"])
                await server.send_message(message)
        except KeyError as e:
            self.logger.log("need email configuration.")
            raise KeyError
    '''
    def cleanup(self):
        """ Cleanup resources. Placeholder for any cleanup operations needed. """
        # Perform any necessary cleanup after sending an email
        # If you opened any files or resources, close them here
        pass



