from rori import RORIModule, RORIData

class Module(RORIModule):
    def process(self, data):
        clients_music = self.rori.getClientFor(user="AmarOk", datatype="music", origin=data.client)
        clients_answer = self.rori.getClientFor(user="AmarOk", datatype="text", origin=data.client)
        if clients_music:
            self.rori.send(clients_music[0], RORIData(content="random", datatype="music"))
        if clients_answer:
            self.rori.send(clients_answer[0], RORIData(content="J'allume la musique", datatype="text"))
        self.stop_processing = True

m = Module()
m.process(RORIData(content="random", datatype="music"))
