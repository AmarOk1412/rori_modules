from rori import RORIModule, RORIData
import sys
import sqlite3
import random
import datetime
import re


class DBManager():
    def __init__(self):
        self.conn=sqlite3.connect('history.db')

    def select_message_from_today(self, author):
        dbcur = self.conn.cursor()
        current_day = str(datetime.datetime.now()).split(' ')[0]
        today_messages = "SELECT Content From Messages Where Author=\"{0}\" AND Msg_date>= Datetime('{1}');".format(author, current_day)
        return dbcur.execute(today_messages).fetchall()

    def __del__(self):
        self.conn.close()


class Module(RORIModule):
    def process(self, data):
        db = DBManager()
        messages = db.select_message_from_today(data.author)
        alreadySeen = False
        for message in messages:
            m = re.findall(r"^(salut|bonjour|bonsoir|hei|hi|hello|yo|o/)( rori| ?!?)$", message[0])
            if len(m) > 0:
                alreadySeen = True
                break
        if alreadySeen:
            randomstr = random.choice(["already", "already2", ""])
            string_to_say = self.rori.get_localized_sentence(randomstr, self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say)
        else:
            randomstr = random.choice(["salut", "bonjour", "longtime", "o/"])
            string_to_say = self.rori.get_localized_sentence(randomstr, self.sentences)
            res = self.rori.send_for_best_client("text", data.author, string_to_say)
        self.stop_processing = True
