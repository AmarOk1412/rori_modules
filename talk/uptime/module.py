
from datetime import timedelta
from rori import DirectReplyMDProcessor, EmotionsManager, Module

class Module(Module):
    def process(self, interaction):
        '''Say since when the server is up'''
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds = uptime_seconds))
            uptime_string = uptime_string[:uptime_string.rfind(':')].replace(':','h')
        string_to_say = self.rori.get_localized_sentence('time', self.sentences) + uptime_string
        rmd = DirectReplyMDProcessor(interaction).process()
        self.rori.send_for_best_client(
            "text/plain", interaction.author_ring_id, string_to_say, rmd)
        # Update emotions
        cjoy = EmotionsManager().get_emotions(interaction.author_ring_id)[1]
        cjoy = 20 if cjoy > 20 else cjoy
        EmotionsManager().go_to_emotion(ring_id=interaction.author_ring_id, delta=1, joy=cjoy)
        self.stop_processing = True
