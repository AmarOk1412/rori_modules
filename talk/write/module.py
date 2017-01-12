from rori import RORIModule, RORIData
import sys, os, re

class Module(RORIModule):
    def process(self, data):
        question = self.rori.is_awaiting(data.author)
        # If we already have the contact
        if question is not None:
            m = re.findall(r"(\"|')(.+)(\"|')", data.content)
            if len(m) is 0:
                string_to_say = self.rori.get_localized_sentence('easy', self.sentences)
                res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
            else:
                end = self.rori.get_localized_sentence('?', self.sentences)
                destination_user = question[:-len(end)].split(' ')[-1]
                string_to_say = self.rori.get_localized_sentence('message', self.sentences).format(destination_user, data.author) + m[0][1]
                self.rori.send_for_best_client("text", destination_user, string_to_say, data.client)
                self.rori.remove_awaiting(data.author)
        else:
            # We don't know what to write
            m = re.findall(r"(send|write|crit|envoi).{0,30}message.{0,10}( à | a | to )(\w*)", data.content)
            string_to_say = self.rori.get_localized_sentence('sure', self.sentences) + m[0][2] + self.rori.get_localized_sentence('?', self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
            question = self.rori.get_localized_sentence('awaiting', self.sentences) + m[0][2] + self.rori.get_localized_sentence('?', self.sentences)
            self.rori.set_awaiting("write", data.author, question)
            happy = self.rori.emotions.get_attr('happy')
            self.rori.emotions.set_attr('happy', str(happy + 1))
        self.stop_processing = True
