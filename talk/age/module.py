from rori import RORIModule, RORIData
import sys
import random

class Module(RORIModule):
    def process(self, data):
        randomstr = random.choice(["2011","immortal"])
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
      "2011": {
        "en":"I was created in 2011.",
        "fr_FR":"J'ai été créée en 2011"
      },
      "immortal": {
        "en":"You know, I'm immortal, so I will be young forever",
        "fr_FR":"Comme je suis immortelle, je serais à jamais jeune."
      }
     }
    """
    m = Module(sentences)
    m.process(RORIData(author=author, content=content, client=client, datatype=datatype, secret=""))
    print(m.continue_processing())
else:
    print("usage: python3 module.py author content client datatype)")
