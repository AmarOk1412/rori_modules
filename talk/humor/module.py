from rori import EmotionsManager, Module

class Module(Module):
    def process(self, interaction):
        '''Say when RORI is born'''
        cjoy = EmotionsManager().get_emotions(interaction.author_ring_id)[1]
        humor = self.rori.get_localized_sentence('soso', self.sentences)
        if cjoy > 60:
            humor = self.rori.get_localized_sentence('happy', self.sentences)
        if cjoy < 40:
            humor = self.rori.get_localized_sentence('bad', self.sentences)
        self.rori.send_for_best_client("text/plain", interaction.author_ring_id, humor)

        # Update emotions
        csadness = EmotionsManager().get_emotions(interaction.author_ring_id)[4]
        csadness = 20 if csadness > 20 else csadness
        cjoy = 60 if cjoy < 65 else cjoy
        EmotionsManager().go_to_emotion(ring_id=interaction.author_ring_id, delta=2, joy=cjoy, sadness=csadness)

        self.stop_processing = True
