import json
import requests


class Scheduler:
    def __init__(self):
        with open('config.json', 'r') as config:
            conf_json = json.load(config)
            self.api = conf_json['api_listener']
    
    def get_module_id(self, module):
        r = requests.get(f'http://{self.api}/module/{module}')
        if r.status_code != 200:
            return None
        return r.json()['id']

    def add_or_update(self, module, ring_id, username, metadatas, seconds=0, minutes=0, hours=0, days='', at='', repeat=False):
        module_id = self.get_module_id(module)
        if not module_id:
            return False
        parameter = metadatas
        parameter['username'] = username
        parameter['ring_id'] = ring_id
        task_id = self.search_module(module, username, parameter)
        endpoint = 'update' if task_id else 'add'
        data = {
            'id': str(task_id if task_id else 0),
            'module': str(module_id),
            'parameter': str(json.dumps(parameter)),
            'seconds': str(seconds),
            'minutes': str(minutes),
            'hours': str(hours),
            'days': days,
            'at': at,
            'repeat': str(repeat),
        }

        r = requests.post(f'http://{self.api}/task/{endpoint}', json=data)
        return r.status_code == 200


    def search_module(self, module, author, metadatas):
        module_id = self.get_module_id(module)
        if not module_id:
            return False
        data = {'author': author}
        for key in metadatas.keys():
            if key != 'sa':
                data[key] =metadatas[key]
        r = requests.post(f'http://{self.api}/task/search/{module_id}', json=data)
        if r.status_code != 200:
            return None
        return r.json()['id']

    def rm(self, module, author, metadatas):
        task_id = self.search_module(module, author, metadatas)
        if not task_id:
            return False
        r = requests.delete(f'http://{self.api}/task/{task_id}')
        return r.status_code == 200
