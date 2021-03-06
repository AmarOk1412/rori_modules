import datetime
import random
import re
from rori import DBManager, DirectReplyMDProcessor, EmotionsManager, Module

class Database(DBManager):
    def select_message_from_today(self, author):
        '''get messages from today'''
        dbcur = self.conn.cursor()
        current_day = str(datetime.datetime.now()).split(' ')[0]
        today_messages = "SELECT body From History Where author_ring_id=\"" + author + "\" AND tm>= Datetime('" + current_day + "');"
        return dbcur.execute(today_messages).fetchall()

class Module(Module):
    def process(self, interaction):
        '''Say hi to the devices if never seen'''
        rmd=DirectReplyMDProcessor(interaction).process()
        # TODO multidevice hi.
        alreadySeen = False
        nbSeen = 0
        for message in Database().select_message_from_today(str(interaction.device_author["id"])):
            p = re.compile('^(salut|bonjour|bonsoir|hei|hi|hello|yo|o/)( rori| ?!?)$', re.IGNORECASE)
            m = re.findall(p, message[0])
            if len(m) > 0:
                nbSeen += 1
                if nbSeen > 1:
                    alreadySeen = True
                    break
        if alreadySeen:
            randomstr = random.choice(["already", "already2", ""])
            string_to_say = self.rori.get_localized_sentence(randomstr, self.sentences)
            self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
            # Update emotions
            csadness = EmotionsManager().get_emotions(str(interaction.device_author["id"]))[4]
            csadness = 20 if csadness > 20 else csadness
            EmotionsManager().go_to_emotion(d_id=str(interaction.device_author["id"]), delta=2, joy=60, sadness=csadness)
        else:
            randomstr = random.choice(["salut", "bonjour", "longtime", "o/"])
            string_to_say = self.rori.get_localized_sentence(randomstr, self.sentences)
            res = self.rori.send_for_best_client("text/plain", interaction.device_author, string_to_say, rmd)
        self.stop_processing = True
