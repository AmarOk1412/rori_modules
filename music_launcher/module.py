from rori import RORIModule, RORIData

class Module(RORIModule):
    def process(self, data):
        string_to_say = self.rori.get_localized_sentence('playMusic')
        clients_music = self.rori.getClientFor(user="AmarOk", datatype="music", origin=data.client)
        clients_answer = self.rori.getClientFor(user="AmarOk", datatype="text", origin=data.client)
        if clients_music:
            self.rori.send(clients_music[0], RORIData(content="random", datatype="music"))
        if clients_answer:
            self.rori.send(clients_answer[0], RORIData(content=string_to_say, datatype="text"))
        self.stop_processing = True

m = Module()
m.process(RORIData(content="random", datatype="music"))
