from rori import DirectReplyMDProcessor, EmotionsManager, Module
import random

class Module(Module):
    def process(self, interaction):
        '''Answer to thx'''
        rmd = DirectReplyMDProcessor(interaction).process()
        cjoy = EmotionsManager().get_emotions(str(interaction.device_author["id"]))[1]
        choice = random.randint(0,4)
        if choice != 4:
            sentences = ['welcome', 'np', 'servitor']
            to_say = self.rori.get_localized_sentence(sentences[choice-1], self.sentences)
            self.rori.send_for_best_client("text/plain", interaction.device_author, to_say, rmd)

        # Update emotions
        csadness = EmotionsManager().get_emotions(str(interaction.device_author["id"]))[4]
        csadness = 20 if csadness > 20 else csadness
        cjoy = 65 if cjoy < 65 else cjoy
        EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=2, joy=cjoy, sadness=csadness)

        self.stop_processing = True