from rori import RORIModule, RORIData

class Module(RORIModule):
    def process(self, data):
        string_to_say = self.rori.get_localized_sentence('playMusic', self.sentences)
        res = self.rori.send_for_best_client("music", "AmarOk", "start", data.client)
        res = self.rori.send_for_best_client("text", "AmarOk", string_to_say, data.client)
        self.stop_processing = True

# TODO, in the future, RORI will have to do this in Rust
sentences = """{
  "playMusic": {
      "en":"Music!",
      "fr_FR":"Musique !"
    }
 }
"""
m = Module('127.0.0.1','3000',sentences)
m.process(RORIData(content="random", datatype="music"))
print(m.continue_processing())
