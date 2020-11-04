import appdirs
import feedparser
import json
import re

from rori import DirectReplyMDProcessor, EmotionsManager, Scheduler

class Module(Module):
    def process(self, interaction):
        '''Add new feeds to follow'''
        rmd = DirectReplyMDProcessor(interaction).process()
        self.stop_processing = True
        url = re.search("(?P<url>https?://[^\s]+)", myString).group("url")
        config_dir = appdirs.user_data_dir('RORI', 'AmarOk')

        emotions = EmotionsManager().get_emotions(str(interaction.device_author["id"]))
        cjoy = emotions[1]
        csadness = emotions[4]

        with open(f'{config_dir}/feed/config.json', 'r+') as config:
            data = json.load(config)

        new_data = []

        for rsc in data:
            if rsc['url'] == url:
                string_to_say = self.rori.get_localized_sentence('found', self.sentences)
                self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
                csadness = 40 if csadness < 40 else csadness
                cjoy = 50 if csadness > 50 else cjoy
                EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=2, joy=cjoy, sadness=csadness)
            else:
                new_data.append(rsc)

        with open(f'{config_dir}/feed/config.json', 'w+') as config:
            config.write(json.dumps(new_data))


        if new_data.empty():
            success = Scheduler().rm('parse_feed', interaction.get_author(), [])
            if not success:
                string_to_say = self.rori.get_localized_sentence('failed', self.sentences)
                self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
                csadness = 60 if csadness < 60 else csadness
                cjoy = 40 if csadness > 40 else cjoy
                EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=2, joy=cjoy, sadness=csadness)
                return