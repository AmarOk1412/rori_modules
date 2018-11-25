import re
import wikipedia
from rori import DirectReplyMDProcessor, EmotionsManager, Module

class Module(Module):
    def process(self, interaction):
        '''Search somebody on wikipedia'''
        rmd = DirectReplyMDProcessor(interaction).process()
        m = re.findall(r"(who.is|qui.es(t)).(.*)",
                       interaction.body, re.IGNORECASE)
        who = m[0][-1]
        try:
            if who[:4].lower() != "rori":
                string_to_say = wikipedia.summary(who, sentences=2)
                self.rori.send_for_best_client("text/plain", interaction.author_ring_id, string_to_say, rmd)
            else:
                string_to_say = self.rori.get_localized_sentence('me', self.sentences)
                self.rori.send_for_best_client("text/plain", interaction.author_ring_id, string_to_say, rmd)
        except:
            string_to_say = self.rori.get_localized_sentence('dont_know', self.sentences)
            self.rori.send_for_best_client("text/plain", interaction.author_ring_id, string_to_say, rmd)
        self.stop_processing = True
