from .utils import DBManager
import dbus
import json


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


class Database(DBManager):
    def select_devices_with_datatype(self, username, datatype):
        '''get devices with a datatype for the given user'''
        dbcur = self.conn.cursor()
        compatible_devices = "SELECT hash FROM Devices Where username=\"" + username + "\" AND additional_types LIKE \"%" + datatype + "%\";"
        return dbcur.execute(compatible_devices).fetchall()

    def get_username(self, d_id):
        '''get devices with a datatype for the given user'''
        dbcur = self.conn.cursor()
        username_req = "SELECT username FROM Devices Where id=\"" + d_id + "\";"
        return dbcur.execute(username_req).fetchall()

    def is_compatible_with_datatype(self, d_id, datatype):
        '''get devices with a datatype for the given user'''
        dbcur = self.conn.cursor()
        compatible_devices = "SELECT hash FROM Devices Where id=\"" + d_id + "\" AND additional_types LIKE \"%" + datatype + "%\";"
        return len(dbcur.execute(compatible_devices).fetchall()) != 0

class RORI:
    def __init__(self):
        self.lang = 'en'

    def send_for_best_client(self, datatype, device, content, metadatas={}):
        '''Send a mesage to the best device'''
        if len(content) == 0:
            return False
        db = Database()
        bus = dbus.SessionBus()
        configuration_mngr = bus.get_object('cx.ring.Ring', '/cx/ring/Ring/ConfigurationManager', introspect=False)
        sendTextMessage = configuration_mngr.get_dbus_method('sendTextMessage', 'cx.ring.Ring.ConfigurationManager')
        config = ''
        simple_payloads = {datatype: content}
        #payloads = {**simple_payloads, **metadatas} # Python > 3.5... Travis seems to not like it.
        payloads = merge_two_dicts(simple_payloads, metadatas)
        with open('config.json', 'r') as f:
            config = json.loads(f.read())
        if datatype == "text/plain":
            sendTextMessage(config['ring_id'], device["ring_id"], payloads)
        else:
            username = db.get_username(str(device["id"]))[0][0]
            if len(username) == 0:
                if db.is_compatible_with_datatype(str(device["id"]), datatype):
                    sendTextMessage(config['ring_id'], device["ring_id"], payloads)
                else:
                    return False
            else:
                chosen_device = db.select_devices_with_datatype(username, datatype)
                if len(chosen_device) > 0:
                    sendTextMessage(config['ring_id'], chosen_device[0][0], payloads)
                else:
                    return False
        return True

    def get_localized_sentence(self, id, data):
        '''Get translated sentence linked to a token'''
        try:
            json_data = json.loads(data)
            result = json_data[id][self.lang]
            return result
        except:
            return ""
