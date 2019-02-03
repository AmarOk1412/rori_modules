import random
from rori import DirectReplyMDProcessor, EmotionsManager, Module

class Module(Module):
    def process(self, interaction):
        '''Say when RORI is born'''
        randomstr = random.choice(["details","no_details"])
        string_to_say = self.rori.get_localized_sentence(randomstr, self.sentences)
        rmd = DirectReplyMDProcessor(interaction).process()
        self.rori.send_for_best_client(
            "text/plain", interaction.device_author, string_to_say, rmd)
        # Update emotions
        csadness = EmotionsManager().get_emotions(str(interaction.device_author["id"]))[4]
        csadness = 20 if csadness > 20 else csadness
        cjoy = EmotionsManager().get_emotions(str(interaction.device_author["id"]))[1]
        cjoy = 60 if cjoy < 65 else cjoy
        EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=2, joy=cjoy, sadness=csadness)
        self.stop_processing = True
