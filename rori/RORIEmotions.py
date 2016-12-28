import sqlite3
import datetime

class RORIEmotions:
    def __init__(self):
        self.conn=sqlite3.connect('rori.db')

    def create_attr_table(self):
        dbcur = self.conn.cursor()
        isAttrTableRequest = "SELECT * FROM sqlite_master WHERE name ='Attributes' and type='table'; "
        dbcur.execute(isAttrTableRequest)
        result = dbcur.fetchone()
        if not result:
            createTableRequest = "CREATE TABLE Attributes(id INTEGER PRIMARY KEY ASC, Name TEXT, Value INTEGER);"
            dbcur.execute(createTableRequest)
            self.conn.commit()

    def get_attr(self, attribute):
        self.create_attr_table()
        cursor = self.conn.cursor()
        cursor.execute("SELECT Value FROM Attributes WHERE Name=\"{0}\"".format(attribute))
        result = cursor.fetchone()
        if result is None:
            return 0
        return result[0]

    def is_present(self, attribute):
        cursor = self.conn.cursor()
        cursor.execute("SELECT Value FROM Attributes WHERE Name=\"{0}\"".format(attribute))
        return cursor.fetchone() is not None

    def set_attr(self, attribute, newValue):
        if int(newValue) > 100 or int(newValue) < -100:
            return
        self.create_attr_table()
        cursor = self.conn.cursor()
        if self.is_present(attribute) is None:
            cursor.execute("INSERT INTO Attributes(Name, Value) VALUES(\"{0}\", {1})".format(attribute, newValue))
        else:
            cursor.execute("UPDATE Attributes SET Value={0} WHERE Name=\"{1}\"".format(newValue, attribute))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
