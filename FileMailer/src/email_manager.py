import os
import smtplib
import logging

import asyncio
import time

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
        self.smtp_server = self.config_manager.get('smtp_server')
        self.smtp_port = self.config_manager.get('smtp_port')
        self.username = self.config_manager.get('email_username')
        self.password = self.config_manager.get('email_password')

    async def send_email(self, recipient, subject, body, attachments=None):
        """ Send an email with the given parameters """
        message = MIMEMultipart()
        message['From'] = self.username
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Add attachments if provided
        if attachments:
            for attachment in attachments:
                part = MIMEBase('application', 'octet-stream')
                try:
                    with open(attachment, 'rb') as file:
                        part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment)}")
                    message.attach(part)
                except Exception as e:
                    self.logger.log(f"Failed to attach file {attachment}: {e}", level=logging.ERROR)
                    continue  


        # Retry logic parameters
        retries = 3
        wait_time = 1  # Wait time starts at 1 second

        for attempt in range(retries):
            try:
                # Attempt to send the email
                await self._attempt_send(message)
                self.logger.log(f"Email sent to {recipient}", level=logging.INFO)
                break  # If the email is sent successfully, break out of the retry loop
            except smtplib.SMTPException as e:
                self.logger.log(f"SMTP error on attempt {attempt + 1} when sending email to {recipient}: {e}", level=logging.ERROR)
                if attempt < retries - 1:  # If not the last attempt, wait before retrying
                    time.sleep(wait_time)
                    wait_time *= 2  # Exponential backoff: double the wait time for the next attempt
                else:
                    self.logger.log(f"All retry attempts failed for {recipient}.", level=logging.CRITICAL)
                    raise  # Re-raise the exception after all attempts fail
            finally:
                self.cleanup()

    async def _attempt_send(self, message):
        """ A helper coroutine that attempts to send the email message once. """
        async with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            await server.connect()
            await server.starttls()
            await server.login(self.username, self.password)
            await server.send_message(message)

    def cleanup(self):
        """ Cleanup resources. Placeholder for any cleanup operations needed. """
        # Perform any necessary cleanup after sending an email
        # If you opened any files or resources, close them here
        pass



