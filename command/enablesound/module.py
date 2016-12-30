from rori import RORIModule, RORIData
import sys
import random

class Module(RORIModule):
    def process(self, data):
        # If RORI is not enough happy, can say no
        happy = self.rori.emotions.get_attr('happy')
        if happy < 0 and random.randint(0,3) is 1:
            string_to_say = self.rori.get_localized_sentence('later', self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say)
            return
        # Send command to a computer on linux
        res = self.rori.send_for_best_client("shell", data.author, "pactl set-sink-volume 0 100%")
        # Change emotion
        self.rori.emotions.set_attr('happy', str(happy - 1))
        # Return result to client
        if res is not None:
            string_to_say = self.rori.get_localized_sentence('mute', self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say)
        else:
            string_to_say = self.rori.get_localized_sentence('cant', self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say)
        # We don't want more actions
        self.stop_processing = True

# TODO, in the future, RORI will have to do this in Rust
if len(sys.argv) == 5:
    author = sys.argv[1][1:-1]
    content = sys.argv[2][1:-1]
    client = sys.argv[3][1:-1]
    datatype = sys.argv[4][1:-1]
    sentences = """{
      "mute": {
        "en":"sound is on",
        "fr_FR":"Le son est à 100%"
      },
      "cant": {
        "en":"I can't detect endpoint for this command",
        "fr_FR":"Je ne trouve pas de sortie pour cette command..."
      },
      "later": {
        "en":"No, the sound is correct...",
        "fr_FR":"nope, je laisse le son comme ça..."
      }
     }
    """
    m = Module(sentences)
    m.process(RORIData(author=author, content=content, client=client, datatype=datatype, secret=""))
    print(m.continue_processing())
else:
    print("usage: python3 module.py author content client datatype")
