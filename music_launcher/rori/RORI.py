import json

class RORI:
    def __init__(self):
        self.lang = "en"

    def set_language(self, new_lang):
        self.lang = new_lang

    def getClientFor(self, user, datatype, origin):
        print("Not implemented!\n")

    def send(self, destination, data):
        print("Not implemented!\n")

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
