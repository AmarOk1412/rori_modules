from rori import RORIModule, RORIData
import sys, os, re, time
import threading


class Alarm(threading.Thread):
    def __init__(self, hours, minutes):
        super(Alarm, self).__init__()
        self.hours = int(hours)
        self.minutes = int(minutes)
        self.keep_running = True
        self.is_running = True

    def run(self):
        try:
            while self.keep_running:
                now = time.localtime()
                if (now.tm_hour == self.hours and now.tm_min == self.minutes):
                    self.is_running = False
                    return
                time.sleep(60)
        except:
            return

    def just_die(self):
        self.keep_running = False


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
                    res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
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
        res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
        alarm.start()
        while alarm.is_running:
            time.sleep(20)
        string_to_say = self.rori.get_localized_sentence('ping', self.sentences) + data.author
        happy = self.rori.emotions.get_attr('happy')
        self.rori.emotions.set_attr('happy', str(happy - 1))
        res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
