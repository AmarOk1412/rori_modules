import random
import subprocess
import re
import json
from rori import DirectReplyMDProcessor, EmotionsManager, Module

class Module(Module):
    def getMeteo(self, city):
        command = "curl \"http://api.openweathermap.org/data/2.5/weather?appid=e9b4f18cf513f45ea12baeea7dc31746&q=" + city + "\""
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, _ = process.communicate()
        return output.decode("utf-8")

    def process(self, interaction):
        '''Retrieve the current meteo'''
        rmd = DirectReplyMDProcessor(interaction).process()
        self.stop_processing = True
        emotions = EmotionsManager().get_emotions(str(interaction.device_author["id"]))
        cjoy = emotions[1]
        csadness = emotions[4]
        if (cjoy < 30 or csadness > 60) and random.randint(0,3) is 1:
            # RORI do not want to play music
            string_to_say = self.rori.get_localized_sentence('later', self.sentences)
            self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
            return

        m = re.findall(r"(weather|meteo).{1,30}in.(the city of |)(\w*)", interaction.body)
        city = m[0][-1]
        json_meteo = self.getMeteo(city)
        meteo = json.loads(json_meteo)
        try:
            description = meteo["weather"][0]["description"]
            string_to_say = self.rori.get_localized_sentence('current_meteo', self.sentences) + city + self.rori.get_localized_sentence('is', self.sentences) + description + ".\n"
            temp = meteo["main"]["temp"]-273.15
            temp_str = '%i' % temp
            string_to_say +=  self.rori.get_localized_sentence('current_temp', self.sentences) + temp_str + self.rori.get_localized_sentence('degrees', self.sentences)
            self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)

            # Change emotions
            if 'clear' in description or 'clouds' in description or 'snow' in description:
                csadness = 20 if csadness > 20 else csadness
                cjoy = 80 if csadness < 80 else cjoy
                EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=3, joy=cjoy, sadness=csadness)
            elif 'rain' in description or 'drizzle' in description:
                csadness = 35 if csadness > 35 else csadness
                cjoy = 60 if csadness < 60 else cjoy
                EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=2, joy=cjoy, sadness=csadness)
            else:
                csadness = 50 if csadness > 50 else csadness
                cjoy = 50 if csadness < 50 else cjoy
                EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=5, joy=cjoy, sadness=csadness)
        except:
            if meteo["message"] == "Error: Not found city":
                string_to_say = self.rori.get_localized_sentence('bad_meteo', self.sentences)
                self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
            # Change emotions
            csadness = 60 if csadness < 60 else csadness
            cjoy = 40 if csadness > 40 else cjoy
            EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=2, joy=cjoy, sadness=csadness)
