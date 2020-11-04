import appdirs
import feedparser
import json
import re
import os

from rori import DirectReplyMDProcessor, Module, EmotionsManager, Scheduler

class Module(Module):
    def process(self, interaction):
        '''Add new feeds to follow'''
        rmd = DirectReplyMDProcessor(interaction).process()
        self.stop_processing = True
        url = re.search("(?P<url>https?://[^\s]+)", interaction.body).group("url")
        config_dir = appdirs.user_data_dir('RORI', 'AmarOk')
        config_file = f'{config_dir}/feed/config.json'
        parsed = feedparser.parse(url)

        emotions = EmotionsManager().get_emotions(str(interaction.device_author["id"]))
        cjoy = emotions[1]
        csadness = emotions[4]

        if not os.path.exists(config_file):
            directory = os.path.dirname(config_file)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(config_file, 'w+') as config:
                config.write(json.dumps([{
                    "name": parsed.feed.title,
                    "url": url
                }]))
            success = Scheduler().add_or_update('parse_feed', interaction.device_author["ring_id"], interaction.get_author(), interaction.metadatas, minutes=5, repeat=True)
            if not success:
                string_to_say = self.rori.get_localized_sentence('failed', self.sentences)
                self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
                csadness = 60 if csadness < 60 else csadness
                cjoy = 40 if csadness > 40 else cjoy
                EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=2, joy=cjoy, sadness=csadness)
                return
        else:
            with open(config_file, 'r') as config:
                data = json.load(config)

            for rsc in data:
                if url == rsc['url']:
                    string_to_say = self.rori.get_localized_sentence('found', self.sentences)
                    self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
                    csadness = 60 if csadness < 60 else csadness
                    cjoy = 40 if csadness > 40 else cjoy
                    EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=2, joy=cjoy, sadness=csadness)
                    return

            data.append({
                "name": parsed.feed.title,
                "url": url
            })

            with open(f'{config_dir}/feed/config.json', 'w+') as config:
                config.write(json.dumps(data))

        string_to_say = self.rori.get_localized_sentence('added', self.sentences)
        self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
        csadness = 40 if csadness < 40 else csadness
        cjoy = 60 if csadness > 60 else cjoy
        EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=2, joy=cjoy, sadness=csadness)
