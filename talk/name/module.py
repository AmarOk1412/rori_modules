import random
from rori import EmotionsManager, Module

class Module(Module):
    def process(self, interaction):
        '''Say what means RORI'''
        randomstr = random.choice(["acronym","long","short"])
        string_to_say = self.rori.get_localized_sentence(randomstr, self.sentences)
        self.rori.send_for_best_client("text/plain", interaction.author_ring_id, string_to_say)
        # Update emotions
        csadness = EmotionsManager().get_emotions(interaction.author_ring_id)[4]
        csadness = 20 if csadness > 20 else csadness
        cjoy = EmotionsManager().get_emotions(interaction.author_ring_id)[1]
        cjoy = 60 if cjoy < 65 else cjoy
        EmotionsManager().go_to_emotion(ring_id=interaction.author_ring_id, delta=2, joy=cjoy, sadness=csadness)
        self.stop_processing = True
