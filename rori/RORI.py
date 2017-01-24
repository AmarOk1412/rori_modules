import json
import requests
import random
import sqlite3

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

    def reprocess(self, data):
        url = "http://" + self.base_url + ":" + self.port + "/reprocess"
        res = requests.post(url, data=data.to_json_str())
        return res

    def send(self, destination, data):
        url = "http://" + self.base_url + ":" + self.port + "/send/" + str(destination)
        res = requests.post(url, data=data.to_json_str())
        return res

    def send_for_best_client(self, datatype, user, content, data_from=None):
        clients_datatype = self.getClientFor(user=user, datatype=datatype)
        if clients_datatype:
            pos = 0
            if data_from is not None:
                cpt = 0
                for client in clients_datatype:
                    if client['name'] == data_from:
                        pos = cpt
                        break
                    cpt += 1
            res = self.send(clients_datatype[pos]['id'], RORIData.RORIData(client="rori_server", content=content,  author="rori_server", datatype=datatype, secret=self.secret))
            return res
        return None

    def send_to_all_client(self, datatype, user, content, client):
        clients_datatype = self.getClientFor(user=user, datatype=datatype, origin=client)
        for c in clients_datatype:
            self.send(c, RORIData.RORIData(client="rori_server", content=content,  author="rori_server", datatype=datatype, secret=self.secret))

    def add_word_to_category(self, category, word):
        url = "http://" + self.base_url + ":" + self.port + "/add_word/" + category + "/" + word
        response = requests.get(url)
        return response

    def rm_word_from_category(self, category, word):
        url = "http://" + self.base_url + ":" + self.port + "/rm_word/" + category + "/" + word
        response = requests.get(url)
        return response

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

    def create_awaiting_table(self):
        dbcur = self.emotions.conn.cursor()
        isAttrTableRequest = "SELECT * FROM sqlite_master WHERE name ='Awaiting' and type='table'; "
        dbcur.execute(isAttrTableRequest)
        result = dbcur.fetchone()
        if not result:
            createTableRequest = "CREATE TABLE Awaiting(id INTEGER PRIMARY KEY ASC, ModuleName TEXT, User TEXT, Question TEXT);"
            dbcur.execute(createTableRequest)
            self.emotions.conn.commit()

    def set_awaiting(self, module_name, user, question):
        self.create_awaiting_table()
        cursor = self.emotions.conn.cursor()
        cursor.execute("INSERT INTO Awaiting(ModuleName, User, Question) VALUES(\"{0}\", \"{1}\", \"{2}\")".format(module_name, user, question))
        self.emotions.conn.commit()

    def is_awaiting(self, user):
        self.create_awaiting_table()
        cursor = self.emotions.conn.cursor()
        cursor.execute("SELECT Question FROM Awaiting WHERE User=\"{0}\"".format(user))
        result = cursor.fetchone()
        if result is None:
            return result
        return result[0]

    def remove_awaiting(self, user):
        self.create_awaiting_table()
        cursor = self.emotions.conn.cursor()
        cursor.execute("DELETE FROM Awaiting WHERE User=\"{0}\"".format(user))
        self.emotions.conn.commit()
