from rori import RORIModule, RORIData
import sys, os, re

class Module(RORIModule):
    def process(self, data):
        output = os.popen('uptime','r').read()
        m = re.findall(r"[0-9A-z:]+ up  ([0-9\:]+)", output)
        string_to_say = self.rori.get_localized_sentence('time', self.sentences) + m[0].replace(":","h")
        res = self.rori.send_for_best_client("text", data.author, string_to_say)
        self.stop_processing = True

# TODO, in the future, RORI will have to do this in Rust
if len(sys.argv) == 5:
    author = sys.argv[1][1:-1]
    content = sys.argv[2][1:-1]
    client = sys.argv[3][1:-1]
    datatype = sys.argv[4][1:-1]

    sentences = """{
      "time": {
        "en":"I'm up since ",
        "fr_FR":"Je suis activée depuis "
      }
     }
    """
    m = Module(sentences)
    m.process(RORIData(author=author, content=content, client=client, datatype=datatype, secret=""))
    print(m.continue_processing())
else:
    print("usage: python3 module.py author content client datatype)")
