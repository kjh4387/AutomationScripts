import keyring
import logging
from getpass import getpass

logger = logging.getLogger(__name__)

def store_credentials():
    service_id = 'my_service'
    
    user_id = input("Enter your ID: ")
    user_pw = getpass("Enter your password (it won't be displayed): ")
    
    keyring.set_password(service_id, user_id, user_pw)
    logger.info("Credentials stored successfully!")

def retrieve_credentials():
    service_id = 'my_service'
    
    user_id = input("Enter the ID to retrieve the associated password: ")
    password = keyring.get_password(service_id, user_id)
    
    if password:
        return password
    else:
        print(f"No password found for {user_id}")

def main():
    choice = input("Do you want to (s)tore credentials or (r)etrieve them? ").lower()

    if choice == 's':
        store_credentials()
    elif choice == 'r':
        retrieve_credentials()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()