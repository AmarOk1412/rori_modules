import json

class RORIData:
    def __init__(self, author, content, client, datatype, secret):
        self.author = author
        self.content = content
        self.client = client
        self.datatype = datatype
        self.secret = secret

    def to_json_str(self):
        return """{
         "author":"%s",
         "content":"%s",
         "client":"%s",
         "datatype":"%s",
         "secret":"%s"
        }
        """ % (self.author, self.content, self.client, self.datatype, self.secret)

def create_data_from_json(str_json):
    data = json.loads(str_json)
    return RORIData(author=data["author"], content=data["content"], client=data["client"], datatype=data["datatype"], secret=data["secret"])
