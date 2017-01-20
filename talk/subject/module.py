from rori import RORIModule, RORIData
import subprocess
import random
import re

class Module(RORIModule):
    def getSubjects(self, sentence):
        command = "python rori_modules/nltk/getsubject.py \"" + sentence + "\""
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        return output.decode("utf-8")

    def process(self, data):
        # If RORI is not enough happy, can say no
        happy = self.rori.emotions.get_attr('happy')
        if happy < 0 and random.randint(0,3) is 1:
            string_to_say = self.rori.get_localized_sentence('later', self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
        else:
            m = re.findall(r"subject.{0,100}(sentence|line|phrase|in): (.+)", data.content)
            sentence = m[0][-1]
            subjects = self.getSubjects(sentence)
            if len(subjects) is 0:
                string_to_say = self.rori.get_localized_sentence('bad_sentence', self.sentences)
                res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
            else:
                string_to_say = self.rori.get_localized_sentence('subjects', self.sentences) + subjects[:-2]
                res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
        # We don't want more actions
        self.stop_processing = True
