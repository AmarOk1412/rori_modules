from rori import DirectReplyMDProcessor, EmotionsManager, Module

class Module(Module):
    def process(self, interaction):
        '''RORI try to sing or not'''
        cjoy = EmotionsManager().get_emotions(str(interaction.device_author["id"]))[1]
        sing = self.rori.get_localized_sentence('cant', self.sentences)
        if cjoy > 60:
            sing = self.rori.get_localized_sentence('ok', self.sentences)
        rmd = DirectReplyMDProcessor(interaction).process()
        self.rori.send_for_best_client(
            "text/plain", interaction.device_author, sing, rmd)

        # Update emotions
        csadness = EmotionsManager().get_emotions(str(interaction.device_author["id"]))[4]
        csadness = 20 if csadness > 20 else csadness
        cjoy = 70 if cjoy < 70 else cjoy
        EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=2, joy=cjoy, sadness=csadness)

        self.stop_processing = True
