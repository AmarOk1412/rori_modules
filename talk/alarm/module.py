from rori import DirectReplyMDProcessor, EmotionsManager, Module
import sys, os, re, time

class Module(Module):
    def process(self, interaction):
        '''RORI wake up user'''
        rmd = DirectReplyMDProcessor(interaction).process()
        self.stop_processing = True
        m = re.findall(r"(in|at|dans|à|a).([0-9]+)(:|h|.*)([0-9]*)", interaction.body)
        hour = 0
        minute = 0
        if m[0][0] == "dans" or m[0][0] == "in":
            now = time.localtime()
            hour = now.tm_hour
            minute = now.tm_min
            if m[0][2] is not ':' and m[0][2] is not 'h':
                is_min = re.findall(r"(hour|heure|min|[0-9]+ ?h|[0-9]+ ?m)", interaction.body)
                if len(is_min) == 0:
                    string_to_say = self.rori.get_localized_sentence('cant', self.sentences)
                    self.rori.send_for_best_client("text/plain", interaction.author_ring_id, string_to_say, rmd)
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
        string_to_say = hour_str + ":" + minute_str
        res = self.rori.send_for_best_client("alarm",  interaction.author_ring_id, string_to_say, rmd)
        if res is None:
            string_to_say = self.rori.get_localized_sentence('nodetect', self.sentences)
            self.rori.send_for_best_client("text/plain", interaction.author_ring_id, string_to_say, rmd)
        else:
            string_to_say = self.rori.get_localized_sentence('ok', self.sentences) + string_to_say
            self.rori.send_for_best_client("text/plain", interaction.author_ring_id, string_to_say, rmd)

        # Update emotions
        cjoy = EmotionsManager().get_emotions(interaction.author_ring_id)[1]
        cjoy = 40 if cjoy < 40 else cjoy
        EmotionsManager().go_to_emotion(ring_id=interaction.author_ring_id, delta=1, joy=cjoy)
