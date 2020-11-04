import random
import feedparser
import json
import appdirs

from rori import DirectReplyMDProcessor, EmotionsManager, Module

class RSSParser:
    def __init__(self, name, url):
        self.lastTitle = ''
        self.name = name
        self.url = url
        self.cache_dir = appdirs.user_cache_dir('RORI', 'AmarOk')
        self.cached_file = f'{self.cache_dir}/feed/{self.name}.cache'
        try:
            with open(self.cached_file, 'r') as f:
                self.lastTitle = f.readline()
        except IOError:
            pass
    
    def get_news(self):
        result = []
        parsed = feedparser.parse(self.url)
        previousLatest = self.lastTitle
        try:
            with open(self.cached_file, 'w+') as f:
                newId = parsed.entries[0].id
                f.write(newId)
                self.lastTitle = newId
        except IOError:
            pass
        
        for entry in parsed.entries:
            if entry.id == previousLatest:
                break
            result.append({
                'id': entry.id,
                'title': entry.title,
                'link': entry.link,
                'description': entry.description,
                'published': entry.published,
            })
        return result


class Module(Module):
    def process(self, interaction):
        '''Check followed RSS feeds'''
        try:
            rmd = DirectReplyMDProcessor(interaction).process()
            self.stop_processing = True
            emotions = EmotionsManager().get_emotions(str(interaction.device_author["id"]))
            cjoy = emotions[1]
            csadness = emotions[4]
            if (cjoy < 30 or csadness > 60) and random.randint(0,3) == 1:
                # RORI do not want to play music
                string_to_say = self.rori.get_localized_sentence('later', self.sentences)
                self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
                return

            config_dir = appdirs.user_data_dir('RORI', 'AmarOk')
            with open(f'{config_dir}/feed/config.json') as config:
                data = json.load(config)
            for rsc in data:
                parser = RSSParser(rsc['name'], rsc['url'])
                for news in parser.get_news():
                    # TODO localized
                    name = rsc['name']
                    title = news['title']
                    description = news['description']
                    link = news['link']
                    to_say = f'New post for {name}: {title}\n'
                    to_say += f'{description}: {link}'
                    self.rori.send_for_best_client("text/plain", interaction.device_author, to_say, rmd)

            # Enable sound on linux
            csadness = 60 if csadness > 60 else csadness
            cjoy = 80 if csadness < 80 else cjoy
            EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=10, joy=cjoy, sadness=csadness)
        except:
            pass

# TODO replace interaction.device_author ? same for emotionsManager