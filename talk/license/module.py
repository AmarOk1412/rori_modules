from rori import RORIModule, RORIData
import sys
import random

class Module(RORIModule):
    def process(self, data):
        randomstr = random.choice(["details","no_details"])
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
      "details": {
        "en":"Of course ! long live to free software ! You can read my source code on this repository: https://github.com/AmarOk1412/RORI",
        "fr_FR":"Bien sûr, je suis un logiciel libre sous WTFPL. Vous pouvez trouver mon code ici : https://github.com/AmarOk1412/RORI"
      },
      "no_details": {
        "en":"Yeah! And I want to be improved.",
        "fr_FR":"Oui, et je veux être améliorée."
      }
     }
    """
    m = Module(sentences)
    m.process(RORIData(author=author, content=content, client=client, datatype=datatype, secret=""))
    print(m.continue_processing())
else:
    print("usage: python3 module.py author content client datatype)")
