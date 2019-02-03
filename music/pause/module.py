import random
from rori import DirectReplyMDProcessor, EmotionsManager, Module

class Module(Module):
    def process(self, interaction):
        '''Pause music for compatible devices'''
        rmd = DirectReplyMDProcessor(interaction).process()
        emotions = EmotionsManager().get_emotions(str(interaction.device_author["id"]))
        cjoy = emotions[1]
        csadness = emotions[4]
        if (cjoy < 30 or csadness > 60) and random.randint(0,3) is 1:
            # RORI do not want to play music
            string_to_say = self.rori.get_localized_sentence('later', self.sentences)
            self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
            self.stop_processing = True
            return

        # Start music and change emotions
        res = self.rori.send_for_best_client("music", interaction.device_author, "pause", rmd)
        csadness = 60 if csadness > 60 else csadness
        cjoy = 80 if csadness < 80 else cjoy
        EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=5, joy=cjoy, sadness=csadness)

        # Send if success or not
        if res:
            string_to_say = self.rori.get_localized_sentence('ok', self.sentences)
            self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
        else:
            string_to_say = self.rori.get_localized_sentence('cant', self.sentences)
            self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
        self.stop_processing = True
