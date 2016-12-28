from rori import RORIModule, RORIData
import sys

class Module(RORIModule):
    def process(self, data):
        res = self.rori.send_for_best_client("shell", data.author, "i3lock")
        if res is not None:
            string_to_say = self.rori.get_localized_sentence('lock', self.sentences)
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
      "mute": {
        "en":"screen is locked",
        "fr_FR":"écran verrouillé !"
      },
      "cant": {
        "en":"I can't detect endpoint for this command",
        "fr_FR":"Je ne trouve pas de sortie pour cette command..."
      }
     }
    """
    m = Module('127.0.0.1','3000',sentences)
    m.process(RORIData(author=author, content=content, client=client, datatype=datatype))
    print(m.continue_processing())
else:
    print("usage: python3 module.py author content client datatype)")
