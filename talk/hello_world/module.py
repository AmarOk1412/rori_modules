from rori import RORIModule, RORIData
import sys
import random

class Module(RORIModule):
    def process(self, data):
        randomstr = random.choice(["salut", "bonjour", "longtime", "o/"])
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
      "salut": {
        "en":"Hi",
        "fr_FR":"Salut"
      },
      "bonjour": {
        "en":"Hello",
        "fr_FR":"Bonjour"
      },
      "longtime": {
        "en":"Hello, it's been a long time",
        "fr_FR":"Salut ! Ça faisait un petit bout de temps..."
      },
      "o/": {
        "en":"o/",
        "fr_FR":"o/"
      }
     }
    """
    m = Module(sentences)
    m.process(RORIData(author=author, content=content, client=client, datatype=datatype, secret=""))
    print(m.continue_processing())
else:
    print("usage: python3 module.py author content client datatype)")
