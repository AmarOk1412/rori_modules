import datetime
import random
import re
from rori import DBManager, EmotionsManager, Module

class Database(DBManager):
    def select_message_from_today(self, author):
        '''get messages from today'''
        dbcur = self.conn.cursor()
        current_day = str(datetime.datetime.now()).split(' ')[0]
        today_messages = "SELECT body From History Where author_ring_id=\"" + author + "\" AND tm>= Datetime('" + current_day + "');"
        return dbcur.execute(today_messages).fetchall()

class Module(Module):
    def process(self, interaction):
        '''Say bye to the devices if never seen'''
        alreadySeen = False
        nbSeen = 0
        for message in Database().select_message_from_today(interaction.author_ring_id):
            p = re.compile('^(salut|bonjour|bonsoir|hei|hi|hello|yo|o/)( rori| ?!?)$', re.IGNORECASE)
            m = re.findall(p, message[0])
            if len(m) > 0:
                nbSeen += 1
                if nbSeen > 1:
                    alreadySeen = True
                    break
        if alreadySeen:
            randomstr = random.choice(["aurevoir", "next", "goodnight", "bye"])
            string_to_say = self.rori.get_localized_sentence(randomstr, self.sentences)
            self.rori.send_for_best_client("text/plain", interaction.author_ring_id, string_to_say)
            # Update emotions
            csadness = EmotionsManager().get_emotions(interaction.author_ring_id)[4]
            csadness = 20 if csadness > 20 else csadness
            EmotionsManager().go_to_emotion(ring_id=interaction.author_ring_id, delta=2, joy=60, sadness=csadness)
        else:
            # Say nothing
            canger = EmotionsManager().get_emotions(interaction.author_ring_id)[3]
            canger = 40 if canger > 40 else canger
            cjoy = EmotionsManager().get_emotions(interaction.author_ring_id)[1]
            cjoy = 50 if cjoy > 50 else cjoy
            EmotionsManager().go_to_emotion(ring_id=interaction.author_ring_id, delta=1, anger=canger, joy=cjoy)
        self.stop_processing = True
