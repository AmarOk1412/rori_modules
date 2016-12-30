from rori import RORIModule, RORIData
import sys
import random

class Module(RORIModule):
    def process(self, data):
        # TODO, if RORI want or not.
        randomstr = random.choice(["ok", "cant"])
        string_to_say = self.rori.get_localized_sentence(randomstr, self.sentences)
        res = self.rori.send_for_best_client("text", data.author, string_to_say)
        self.stop_processing = True

# TODO, in the future, RORI will have to do this in Rust
if len(sys.argv) == 5:
    author = sys.argv[1][1:-1]
    content = sys.argv[2][1:-1]
    client = sys.argv[3][1:-1]
    datatype = sys.argv[4][1:-1]

    sentences = """{
      "ok": {
        "en":"If you want... tadada da da da. (lower) tadadda da da da...",
        "fr_FR":"Si vous voulez. tadada da da da. (plus bas) tadadda da da da..."
      },
      "cant": {
        "en":"Hmm I can't sing on this endpoint...",
        "fr_FR":"Non, je ne peux pas chanter sur ce point de sortie"
      }
     }
    """
    m = Module(sentences)
    m.process(RORIData(author=author, content=content, client=client, datatype=datatype, secret=""))
    print(m.continue_processing())
else:
    print("usage: python3 module.py author content client datatype)")
