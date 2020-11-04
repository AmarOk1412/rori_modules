import json
from .utils import DBManager

class Database(DBManager):
    def get_username(self, d_id):
        '''get devices with a datatype for the given user'''
        dbcur = self.conn.cursor()
        username_req = "SELECT username FROM Devices Where hash=\"" + d_id + "\";"
        return dbcur.execute(username_req).fetchall()

class Interaction:
    def __init__(self, interaction):
        json_value = json.loads(interaction)
        self.device_author = json_value['device_author']
        self.body = json_value['body']
        self.time = json_value['time']
        self.metadatas = json_value['metadatas']

    def get_author(self):
        return Database().get_username(self.device_author['ring_id'])[0][0]