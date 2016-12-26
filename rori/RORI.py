import json
import requests

from rori import RORIData

class RORI:
    def __init__(self, url, port):
        self.lang = "en"
        self.base_url = url
        self.port = port

    def set_language(self, new_lang):
        self.lang = new_lang

    def getClientFor(self, user, datatype):
        url = "http://" + self.base_url + ":" + self.port + "/client/" + user + "/" + datatype
        response = requests.get(url)
        data = response.content.decode("utf-8")
        return json.loads(data)

    def send(self, destination, data):
        url = "http://" + self.base_url + ":" + self.port + "/send/" + str(destination)
        res = requests.post(url, data=data.to_json_str())
        return res

    def send_for_best_client(self, datatype, user, content, client):
        clients_datatype = self.getClientFor(user=user, datatype=datatype)
        if clients_datatype:
            res = self.send(clients_datatype[0]['id'], RORIData.RORIData(content=content, datatype=datatype))
            return res
        return None

    def send_to_all_client(self, datatype, user, content, client):
        clients_datatype = self.getClientFor(user=user, datatype=datatype, origin=client)
        for c in clients_datatype:
            self.send(c, RORIData.RORIData(content=content, datatype=datatype))


    def get_localized_sentence(self, id):
            try:
                with open('sentences.json') as f:
                    data = f.read()
                    json_data = json.loads(data)
                    result = json_data[id][self.lang]
                    return result
                return ""
            except:
                return ""
