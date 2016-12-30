from rori import RORIModule, RORIData
import sys
import random

class Module(RORIModule):
    def process(self, data):
        # TODO, if RORI want or not.
        level = "happy"
        happy = self.rori.emotions.get_attr('happy')
        if happy < 11 and happy > -11:
            level = "soso"
        elif happy < -10:
            level = "bad"
        string_to_say = self.rori.get_localized_sentence(level, self.sentences)
        res = self.rori.send_for_best_client("text", data.author, string_to_say)
        self.stop_processing = True

# TODO, in the future, RORI will have to do this in Rust
if len(sys.argv) == 5:
    author = sys.argv[1][1:-1]
    content = sys.argv[2][1:-1]
    client = sys.argv[3][1:-1]
    datatype = sys.argv[4][1:-1]

    sentences = """{
      "happy": {
        "en":"I am good, thank you for your interest in me.",
        "fr_FR":"Super ! Merci de ton intérêt"
      },
      "soso": {
        "en":"so so",
        "fr_FR":"bof"
      },
      "bad": {
        "en":"I'm a little bit sad...",
        "fr_FR":"Pas terrible"
      }
     }
    """
    m = Module(sentences)
    m.process(RORIData(author=author, content=content, client=client, datatype=datatype, secret=""))
    print(m.continue_processing())
else:
    print("usage: python3 module.py author content client datatype)")
