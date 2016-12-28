from rori import RORI

class RORIModule:
    def __init__(self, ip, port, sentences):
        self.rori = RORI.RORI(ip, port)
        self.stop_processing = False
        self.sentences = sentences

    def process(self, data):
        pass

    def continue_processing(self):
        return not self.stop_processing
