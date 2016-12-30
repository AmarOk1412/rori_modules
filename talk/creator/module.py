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
        "en":"AmarOk is my programmer. He was born in 1994 in... eum, it is not important. He takes AmarOk as his pseudonym before he knows Amarok the free software. Amarok is an Inuit god. The wolf god (it explains the logo of the software).",
        "fr_FR":"AmarOk est mon créateur. Il est né en 1994 dans... boarf, pas important. Il a pris AmarOk comme pseudo avant de connaître le logiciel (et la voiture). AmarOk est le nom d'une divinité inuite (un dieu loup, ce qui explique le logo du logiciel)."
      },
      "no_details": {
        "en":"There are so many nice things to say about my creator... But we will not go on forever. I encourage you to visit his website: https://enconn.fr",
        "fr_FR":"Il y a tant de belles choses à dire sur AmarOk, mais pour faire court, allez voir son site https://enconn.fr"
      }
     }
    """
    m = Module(sentences)
    m.process(RORIData(author=author, content=content, client=client, datatype=datatype, secret=""))
    print(m.continue_processing())
else:
    print("usage: python3 module.py author content client datatype)")
