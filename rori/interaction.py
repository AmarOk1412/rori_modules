import json

class Interaction:
    def __init__(self, interaction):
        json_value = json.loads(interaction)
        self.device_author = json_value['device_author']
        self.body = json_value['body']
        self.time = json_value['time']
        self.metadatas = json_value['metadatas']
