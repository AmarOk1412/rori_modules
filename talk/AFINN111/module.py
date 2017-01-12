from rori import RORIModule, RORIData
import json
from urllib.request import urlopen

class Module(RORIModule):
    def process(self, data):
        afinnjson = urlopen('https://raw.githubusercontent.com/wooorm/afinn-111/master/index.json')
        content = afinnjson.read().decode("utf-8")
        content_json = json.loads(content)
        score = 0
        words = 0
        for w in data.content.split(" "):
            try:
                score += content_json[w]
                words += 1
            except:
                continue
        if words is 0:
            words += 1
        cumulate = score/words
        string_to_say = ""
        if cumulate >= 1:
            string_to_say = self.rori.get_localized_sentence("thanks", self.sentences)
        elif cumulate >= 0:
            string_to_say = self.rori.get_localized_sentence("plus", self.sentences)
        elif cumulate >= -1:
            string_to_say = self.rori.get_localized_sentence("minus", self.sentences)
        else:
            string_to_say = self.rori.get_localized_sentence("minable", self.sentences)
        res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
        self.stop_processing = True
