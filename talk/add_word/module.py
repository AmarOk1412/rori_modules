from rori import RORIModule, RORIData
import sys
import re

class Module(RORIModule):
    def process(self, data):
        m = re.findall(r"add_word: (.+)", data.content)
        words = m[0].split(':')
        self.rori.add_word_to_category(word=words[0], category=words[1])
        string_to_say = self.rori.get_localized_sentence("added", self.sentences)
        res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
        happy = self.rori.emotions.get_attr('happy')
        self.rori.emotions.set_attr('happy', str(happy + 1))
        self.stop_processing = True
