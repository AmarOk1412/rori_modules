from RORI import RORI

class RORIModule:
    def __init__(self, ip, port):
        self.rori = RORI(ip, port)
        self.stop_processing = False

    def process(self, data):
        pass

    def continue_processing(self):
        return not self.stop_processing
