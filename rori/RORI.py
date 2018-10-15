from .utils import DBManager
import dbus
import json

class Database(DBManager):
    def select_devices_with_datatype(self, username, datatype):
        '''get devices with a datatype for the given user'''
        dbcur = self.conn.cursor()
        compatible_devices = "SELECT ring_id From Devices Where username=\"" + username + "\" AND additional_types LIKE \"%" + datatype + "%\";"
        return dbcur.execute(compatible_devices).fetchall()

    def get_username(self, ring_id):
        '''get devices with a datatype for the given user'''
        dbcur = self.conn.cursor()
        username_req = "SELECT username From Devices Where ring_id=\"" + ring_id + "\";"
        return dbcur.execute(username_req).fetchall()

    def is_compatible_with_datatype(self, ring_id, datatype):
        '''get devices with a datatype for the given user'''
        dbcur = self.conn.cursor()
        compatible_devices = "SELECT ring_id From Devices Where ring_id=\"" + ring_id + "\" AND additional_types LIKE \"%" + datatype + "%\";"
        return len(dbcur.execute(compatible_devices).fetchall()) != 0

class RORI:
    def __init__(self):
        self.lang = 'en'

    def send_for_best_client(self, datatype, from_ring_id, content):
        '''Send a mesage to the best device'''
        if len(content) == 0:
            return False
        db = Database()
        bus = dbus.SessionBus()
        configuration_mngr = bus.get_object('cx.ring.Ring', '/cx/ring/Ring/ConfigurationManager', introspect=False)
        sendTextMessage = configuration_mngr.get_dbus_method('sendTextMessage', 'cx.ring.Ring.ConfigurationManager')
        config = ''
        with open('config.json', 'r') as f:
            config = json.loads(f.read())
        if datatype == "text/plain":
            sendTextMessage(config['ring_id'], from_ring_id, {datatype: content})
        else:
            username = db.get_username(from_ring_id)[0][0]
            if len(username) == 0:
                if db.is_compatible_with_datatype(from_ring_id, datatype):
                    sendTextMessage(config['ring_id'], from_ring_id, {datatype: content})
                else:
                    return False
            else:
                chosen_device = db.select_devices_with_datatype(username, datatype)
                if len(chosen_device) > 0:
                    sendTextMessage(config['ring_id'], chosen_device[0][0], {datatype: content})
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
