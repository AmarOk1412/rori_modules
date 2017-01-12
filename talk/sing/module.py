from rori import RORIModule, RORIData
import sys
import random

class Module(RORIModule):
    def process(self, data):
        # TODO, if RORI want or not.
        randomstr = random.choice(["ok", "cant"])
        string_to_say = self.rori.get_localized_sentence(randomstr, self.sentences)
        res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
        happy = self.rori.emotions.get_attr('happy')
        self.rori.emotions.set_attr('happy', str(happy + 1))
        self.stop_processing = True
