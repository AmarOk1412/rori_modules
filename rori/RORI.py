import json
import requests
import random

from rori import RORIData, RORIEmotions

class RORI:
    def __init__(self):
        self.lang = ""
        self.secret = ""
        self.base_url = ""
        self.port = ""
        with open("config.json") as f:
            data = json.loads(f.read())
            self.lang = data['lang']
            self.secret = data['secret']
            self.base_url = data['base_url']
            self.port = data['port']
        self.emotions = RORIEmotions.RORIEmotions()

    def set_language(self, new_lang):
        self.lang = new_lang

    def getClientFor(self, user, datatype):
        url = "http://" + self.base_url + ":" + self.port + "/client/" + user + "/" + datatype
        response = requests.get(url)
        data = response.content.decode("utf-8")
        return json.loads(data)

    def send(self, destination, data):
        url = "http://" + self.base_url + ":" + self.port + "/send/" + str(destination)
        print('send:'+data.to_json_str())
        res = requests.post(url, data=data.to_json_str())
        return res

    def send_for_best_client(self, datatype, user, content):
        clients_datatype = self.getClientFor(user=user, datatype=datatype)
        if clients_datatype:
            res = self.send(clients_datatype[0]['id'], RORIData.RORIData(client="rori_server", content=content,  author="rori_server", datatype=datatype, secret=self.secret))
            return res
        return None

    def send_to_all_client(self, datatype, user, content, client):
        clients_datatype = self.getClientFor(user=user, datatype=datatype, origin=client)
        for c in clients_datatype:
            self.send(c, RORIData.RORIData(client="rori_server", content=content,  author="rori_server", datatype=datatype, secret=self.secret))

    def get_localized_sentence(self, id, data):
            try:
                json_data = json.loads(data)
                result = json_data[id][self.lang]
                return result
            except:
                return ""

    def continue_action_if(self, key, percentage, factor=20):
        value = self.emotions.get_attr(key)
        mean = 0.0
        for i in range(0,2):
            mean += random.normalvariate(0,1)*factor
        level = percentage + (mean/2)
        return value >= level
