from rori import RORIModule, RORIData
import sys
import random

class Module(RORIModule):
    def process(self, data):
        # If RORI is not enough happy, can say no
        happy = self.rori.emotions.get_attr('happy')
        if happy > 10 and random.randint(0,3) is 1:
            string_to_say = self.rori.get_localized_sentence('later', self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say)
            return
        res = self.rori.send_for_best_client("music", data.author, "stop")
        # Change emotion
        self.rori.emotions.set_attr('happy', str(happy - 10))
        # Return result to client
        if res is not None:
            string_to_say = self.rori.get_localized_sentence('stop', self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say)
        else:
            string_to_say = self.rori.get_localized_sentence('cant', self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say)
        self.stop_processing = True

# TODO, in the future, RORI will have to do this in Rust
if len(sys.argv) == 5:
    author = sys.argv[1][1:-1]
    content = sys.argv[2][1:-1]
    client = sys.argv[3][1:-1]
    datatype = sys.argv[4][1:-1]
    sentences = """{
      "stop": {
        "en":"Music is off!",
        "fr_FR":"Je coupe la musique."
      },
      "cant": {
        "en":"I can't detect endpoint for music command",
        "fr_FR":"Je ne trouve pas de sortie pour la musique..."
      },
      "later": {
        "en":"But the music is good...",
        "fr_FR":"Attends au moins la fin de celle-ci."
      }
     }
    """
    m = Module('127.0.0.1','3000',sentences)
    m.process(RORIData(author=author, content=content, client=client, datatype=datatype, secret=""))
    print(m.continue_processing())
else:
    print("usage: python3 module.py author content client datatype")
