from rori import RORIModule, RORIData
import sys, os, re, time
from alarm import Alarm

class Module(RORIModule):
    def process(self, data):
        print(data.content)
        m = re.findall(r"(in|at|dans|à|a).([0-9]+)(:|h|.*)([0-9]*)", data.content)
        print(m[0])
        hour = 0
        minute = 0
        if m[0][0] == "dans" or m[0][0] == "in":
            now = time.localtime()
            hour = now.tm_hour
            minute = now.tm_min
            if m[0][2] is not ':' and m[0][2] is not 'h':
                is_min = re.findall(r"(hour|heure|min|[0-9]+ ?h|[0-9]+ ?m)", data.content)
                if len(is_min) == 0:
                    string_to_say = self.rori.get_localized_sentence('cant', self.sentences)
                    res = self.rori.send_for_best_client("text", data.author, string_to_say)
                    return
                if 'm' in is_min[0]:
                    minute += int(m[0][1])
                else:
                    hour += int(m[0][1])
            else:
                hour += int(m[0][1])
                if m[0][3] is not '':
                    minute += int(m[0][3])
        else:
            hour = int(m[0][1])
            if m[0][3] is not '':
                minute = int(m[0][3])

        hour = (hour + int(minute / 60))%24
        minute = minute % 60
        minute_str = "%02d" % minute
        hour_str = "%02d" % hour

        alarm = Alarm(int(hour), int(minute))
        string_to_say = self.rori.get_localized_sentence('set', self.sentences) + hour_str + "h" + minute_str
        res = self.rori.send_for_best_client("text", data.author, string_to_say)
        alarm.start()
        while alarm.is_running:
            time.sleep(20)
        string_to_say = self.rori.get_localized_sentence('ping', self.sentences) + data.author
        res = self.rori.send_for_best_client("text", data.author, string_to_say)

# TODO, in the future, RORI will have to do this in Rust
if len(sys.argv) == 5:
    author = sys.argv[1][1:-1]
    content = sys.argv[2][1:-1]
    client = sys.argv[3][1:-1]
    datatype = sys.argv[4][1:-1]

    sentences = """{
      "ping": {
        "en":"Hei! Ping ",
        "fr_FR":"Hei ! Ping "
      },
      "set": {
        "en":"I will ping you at ",
        "fr_FR":"Je vous enverrais un message à "
      },
      "cant": {
        "en":"I don't understand...",
        "fr_FR":"Désolé, je n'ai pas pigé ta phrase."
      }
     }
    """
    m = Module(sentences)
    m.process(RORIData(author=author, content=content, client=client, datatype=datatype, secret=""))
    print(m.continue_processing())
else:
    print("usage: python3 module.py author content client datatype)")
