class RORIData:
    def __init__(self, content, datatype):
        self.author = "RORI"
        self.content = content
        self.client = "RORI"
        self.datatype = datatype

    def to_json_str(self):
        return """{
         "author":"%s",
         "content":"%s",
         "client":"%s",
         "datatype":"%s"
        }
        """ % (self.author, self.content, self.client, self.datatype)
