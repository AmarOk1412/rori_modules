import random
from rori import EmotionsManager, Module

class Module(Module):
    def process(self, interaction):
        '''Stop music on compatible devices'''
        emotions = EmotionsManager().get_emotions(interaction.author_ring_id)
        cjoy = emotions[1]
        csadness = emotions[4]
        if (cjoy < 30 or csadness > 60) and random.randint(0,3) is 1:
            # RORI do not want to play music
            string_to_say = self.rori.get_localized_sentence('later', self.sentences)
            self.rori.send_for_best_client("text/plain", interaction.author_ring_id, string_to_say)
            self.stop_processing = True
            return

        # Start music and change emotions
        res = self.rori.send_for_best_client("music", interaction.author_ring_id, "stop")
        csadness = 60 if csadness < 60 else csadness
        cjoy = 30 if csadness > 30 else cjoy
        EmotionsManager().go_to_emotion(ring_id=interaction.author_ring_id, delta=10, joy=cjoy, sadness=csadness)

        # Send if success or not
        if res:
            string_to_say = self.rori.get_localized_sentence('stop', self.sentences)
            self.rori.send_for_best_client("text/plain", interaction.author_ring_id, string_to_say)
        else:
            string_to_say = self.rori.get_localized_sentence('cant', self.sentences)
            self.rori.send_for_best_client("text/plain", interaction.author_ring_id, string_to_say)
        self.stop_processing = True