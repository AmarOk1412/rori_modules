from rori import RORIModule, RORIData

class Module(RORIModule):
    def process(self, data):
        string_to_say = self.rori.get_localized_sentence('playMusic')
        res = self.rori.send_for_best_client("music", "AmarOk", "start", data.client)
        if res is not None:
            print(res.text)
        res = self.rori.send_for_best_client("text", "AmarOk", string_to_say, data.client)
        if res is not None:
            print(res.text)
        self.stop_processing = True

m = Module('127.0.0.1','3000')
m.process(RORIData(content="random", datatype="music"))
