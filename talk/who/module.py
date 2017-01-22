from rori import RORIModule, RORIData
import re
import wikipedia


class Module(RORIModule):
    def process(self, data):
        m = re.findall(r"(who.is|qui.es(t)).(.*)", data.content)
        who = m[0][-1]
        try:
            print("############")
            print(who[:4])
            if who[:4].lower() != "rori":
                string_to_say = wikipedia.summary(who, sentences=2)
                res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
            else:
                string_to_say = self.rori.get_localized_sentence('me', self.sentences)
                res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
        except:
            string_to_say = self.rori.get_localized_sentence('dont_know', self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
        self.continue_processing = False
