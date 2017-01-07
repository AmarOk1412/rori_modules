from rori import RORIModule, RORIData
import sys
import random

class Module(RORIModule):
    def process(self, data):
        # If RORI is not enough happy, can say no
        happy = self.rori.emotions.get_attr('happy')
        if happy < 0 and random.randint(0,3) is 1:
            string_to_say = self.rori.get_localized_sentence('later', self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say)
            return
        # Send command to a computer on i3
        res = self.rori.send_for_best_client("shell", data.author, "i3lock")
        # Change emotion
        self.rori.emotions.set_attr('happy', str(happy - 1))
        # Return result to client
        if res is not None:
            string_to_say = self.rori.get_localized_sentence('lock', self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say)
        else:
            string_to_say = self.rori.get_localized_sentence('cant', self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say)
        # We don't want more actions
        self.stop_processing = True
