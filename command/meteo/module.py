import random
import subprocess
import re
import geocoder
import json
import time
from rori import DirectReplyMDProcessor, EmotionsManager, Module

class Module(Module):
    def getMeteo(self, city, forecast=False):
        mode = "forecast" if forecast else "weather"
        command = f'curl "http://api.openweathermap.org/data/2.5/{mode}?appid=e9b4f18cf513f45ea12baeea7dc31746&q={city}"'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, _ = process.communicate()
        return output.decode("utf-8")

    def processDesc(self, meteo, interaction, rmd, city, emotions, offsetDay=0):
        description = meteo["weather"][0]["description"]
        string_to_say = ''
        if offsetDay <= 1:
            meteo_str = 'current_meteo'
            is_str = 'is'
            if offsetDay == 1:
                meteo_str = 'tomorrow_meteo'
                is_str = 'will'

            string_to_say = self.rori.get_localized_sentence(meteo_str, self.sentences) + city + self.rori.get_localized_sentence(is_str, self.sentences) + description + ".\n"
        else:
            string_to_say = self.rori.get_localized_sentence('in_first', self.sentences) + str(offsetDay) + self.rori.get_localized_sentence('in_sec', self.sentences) + city + self.rori.get_localized_sentence('will', self.sentences) + description + ".\n"

        temp = meteo["main"]["temp"]-273.15
        temp_str = '%i' % temp
        string_to_say +=  self.rori.get_localized_sentence('temp', self.sentences) + temp_str + self.rori.get_localized_sentence('degrees', self.sentences)
        self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)

        # Change emotions
        cjoy = emotions[1]
        csadness = emotions[4]
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

    def parseDay(self, day):
        # TODO should be improved and translated
        if day == 'one':
            return 1
        elif day == 'two':
            return 2
        elif day == 'three':
            return 3
        elif day == 'four':
            return 4
        elif day == 'five':
            return 5
        return int(day)

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

        m = re.findall(r"(tomorrow|day)", interaction.body)
        forecastMode = len(m) != 0
        split_str = re.split(' (in) ', interaction.body)
        m = re.findall(r" (for|next) ", interaction.body)
        forMode = len(m) != 0
        city = ''
        getNext = False
        for splitted in split_str:
            m = re.findall(r"(([A-z]|[0-9])+) +days", splitted)
            if m and not forMode:
                getNext = False
                continue
            if getNext:
                city = splitted.split()[0]
            if splitted == 'in':
                getNext = True

        if city == '':
            g = geocoder.ip('me') # TODO retrieve peer ip
            city = g.city

        self.rori.send_for_best_client("text/plain", interaction.device_author, city, rmd)
        json_meteo = self.getMeteo(city, forecastMode)
        meteo = json.loads(json_meteo)
        try:
            if forecastMode:
                nbDays = 1
                block = 4 # The answer is a JSON with the weather each 3 hours, so 4 * 3 = 12 = midday

                dayParsed = False
                m = re.findall(r"tomorrow", interaction.body)

                if len(m) != 0:
                    dayParsed = True
                if not dayParsed:
                    m = re.findall(r"(([A-z]|[0-9])+) +days", interaction.body)
                    nbDays = self.parseDay(m[0][0].lower())
                    if nbDays > 5:
                        nbDays = 5 # Max for the AP
                if forMode:
                    for d in range(0, nbDays):
                        meteoBlock = meteo["list"][block + 8 * d]
                        self.processDesc(meteoBlock, interaction, rmd, city, emotions, d + 1)
                        time.sleep(1)
                else:
                    meteoBlock = meteo["list"][block + 8 * (nbDays - 1)]
                    self.processDesc(meteoBlock, interaction, rmd, city, emotions, nbDays)

            else:
                self.processDesc(meteo, interaction, rmd, city, emotions)
        except:
            if meteo["message"] == "Error: Not found city":
                string_to_say = self.rori.get_localized_sentence('bad_meteo', self.sentences)
                self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
            # Change emotions
            csadness = 60 if csadness < 60 else csadness
            cjoy = 40 if csadness > 40 else cjoy
            EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=2, joy=cjoy, sadness=csadness)
