class RORIData:
    def __init__(self, author, content, client, datatype):
        self.author = author
        self.content = content
        self.client = client
        self.datatype = datatype

    def to_json_str(self):
        return """{
         "author":"%s",
         "content":"%s",
         "client":"%s",
         "datatype":"%s"
        }
        """ % (self.author, self.content, self.client, self.datatype)
