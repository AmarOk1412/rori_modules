from rori import RORIModule, RORIData
import sys
import random

class Module(RORIModule):
    def process(self, data):
        # TODO, if RORI want or not.
        level = "happy"
        happy = self.rori.emotions.get_attr('happy')
        if happy < 11 and happy > -11:
            level = "soso"
        elif happy < -10:
            level = "bad"
        string_to_say = self.rori.get_localized_sentence(level, self.sentences)
        res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
        self.stop_processing = True
