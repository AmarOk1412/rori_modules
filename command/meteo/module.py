from rori import RORIModule, RORIData
import sys
import random
import subprocess
import re
import json

class Module(RORIModule):
    def getMeteo(self, city):
        command = "curl \"http://api.openweathermap.org/data/2.5/weather?appid=e9b4f18cf513f45ea12baeea7dc31746&q=" + city + "\""
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
            m = re.findall(r"(weather|meteo).in.(the city of |)(\w*)", data.content)
            city = m[0][-1]
            json_meteo = self.getMeteo(city)
            meteo = json.loads(json_meteo)
            try:
                string_to_say = self.rori.get_localized_sentence('current_meteo', self.sentences) + city + ": " + meteo["weather"][0]["description"] + "."
                res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
                temp = meteo["main"]["temp"]-273.15
                string_to_say = "The current temperature is " + str(temp)
                res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
            except:
                if meteo["message"] == "Error: Not found city":
                    string_to_say = self.rori.get_localized_sentence('bad_meteo', self.sentences)
                    res = self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
        # We don't want more actions
        self.stop_processing = True
