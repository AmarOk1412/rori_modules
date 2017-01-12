from rori import RORIModule, RORIData
import sys, os, re, time


class Module(RORIModule):
    def process(self, data):
        m = re.findall(r"(in|at|dans|à|a).([0-9]+)(:|h|.*)([0-9]*)", data.content)
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
        happy = self.rori.emotions.get_attr('happy')
        self.rori.emotions.set_attr('happy', str(happy - 1))

        string_to_say = hour_str + ":" + minute_str
        res = self.rori.send_for_best_client("alarm", data.author, string_to_say)
        if res is None:
            string_to_say = self.rori.get_localized_sentence('nodetect', self.sentences)
            self.rori.send_for_best_client("text", data.author, string_to_say)
        else:
            string_to_say = self.rori.get_localized_sentence('ok', self.sentences) + string_to_say
            self.rori.send_for_best_client("text", data.author, string_to_say)
