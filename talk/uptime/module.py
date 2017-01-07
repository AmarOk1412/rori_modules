from rori import RORIModule, RORIData
import sys, os, re

class Module(RORIModule):
    def process(self, data):
        output = os.popen('uptime','r').read()
        m = re.findall(r"[0-9A-z:]+ up  ([0-9\:]+)", output)
        string_to_say = self.rori.get_localized_sentence('time', self.sentences) + m[0].replace(":","h")
        res = self.rori.send_for_best_client("text", data.author, string_to_say)
        self.stop_processing = True
