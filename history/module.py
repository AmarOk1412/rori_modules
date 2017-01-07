from rori import RORIData, RORIModule
import sys
import sqlite3
import datetime

class DBManager():
    def __init__(self):
        self.conn=sqlite3.connect('history.db')

    def store_data(self, author, content, client, datatype):
        dbcur = self.conn.cursor()
        isMessageTableRequest = "SELECT * FROM sqlite_master WHERE name ='Messages' and type='table'; "
        dbcur.execute(isMessageTableRequest)
        result = dbcur.fetchone()
        if not result:
            createTableRequest = "CREATE TABLE Messages(id INTEGER PRIMARY KEY ASC, Author TEXT, Content TEXT, Client TEXT, Datatype TEXT, Msg_date DATETIME);"
            dbcur.execute(createTableRequest)
            self.conn.commit()
        addMessageRequest = "INSERT INTO Messages(Author, Content, Client, Datatype, Msg_date) VALUES(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\")".format(author, content, client, datatype, str(datetime.datetime.now()))
        dbcur.execute(addMessageRequest)
        self.conn.commit()

    def __del__(self):
        self.conn.close()

class Module(RORIModule):
    def process(self, data):
        db = DBManager()
        db.store_data(data.author, data.content, data.client, data.datatype)
