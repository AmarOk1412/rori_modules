from rori import RORIModule, RORIData
import sys, os, re

class Module(RORIModule):
    def process(self, data):
        question = self.rori.is_awaiting(data.author)
        if question is not None:
            m = re.findall(r"^(rori.{0,5}|a?)(wait!|attends !)(.+)", data.content.lower())
            data.content = m[0][2]
            # TODO, in other thread?
            self.rori.reprocess(data)
            string_to_say = self.rori.get_localized_sentence('but', self.sentences) + question
            res = self.rori.send_for_best_client("text", data.author, string_to_say)
            happy = self.rori.emotions.get_attr('happy')
            self.rori.emotions.set_attr('happy', str(happy + 1))
        self.stop_processing = True
