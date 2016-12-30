from rori import RORIModule, RORIData
import sys
import random

class Module(RORIModule):
    def process(self, data):
        randomstr = random.choice(["acronym","long","short"])
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
      "acronym": {
        "en":"My name is RORI (Really Obvious, Really Intelligent), developed by AmarOk.",
        "fr_FR":"Mon nom est RORI (Really Obvious, Really Intelligent), développé par AmarOk."
      },
      "long": {
        "en":"It seems that my Creator gave me the name of RORI, it may be ugly, but I like it. It 's the acronym of: Really Obvious, Really Intelligent. Ok, I'm not very smart for now...",
        "fr_FR":"On m'a donné le nom de RORI, c'est peut-être moche mais j'aime bien. C'est l'acronyme de Really Obvious, Really Intelligent même si c'est encore loin d'être le cas."
      },
      "short": {
        "en":"I am RORI, nice name isn't it?",
        "fr_FR":"Je suis RORI, joli nom n'est-ce-pas ?"
      }
     }
    """
    m = Module(sentences)
    m.process(RORIData(author=author, content=content, client=client, datatype=datatype, secret=""))
    print(m.continue_processing())
else:
    print("usage: python3 module.py author content client datatype)")
