import json
import os

FILE_PATH = 'logs/logs.json'


class DataBaseHandling:
    def __init__(self):
        """Creates a json file if there is not one"""
        try:
            if not os.path.exists(FILE_PATH):
                raise
        except:
            with open(FILE_PATH, 'w') as f:
                data = {
                    'name': ['username', 'password', 'server_address', 'server_ip']
                }
                json.dump(data, f)
        pass

    def is_new(self, name) -> bool:
        """Returns True if person is new in the database else False"""
        with open(FILE_PATH, 'r') as f:
            data = json.load(f)
        if name in data:
            return False
        return True

    def validate_data(self, name, username, password):
        """Return True if the username and password of the person in database is correct else Fasle"""
        with open(FILE_PATH, 'r') as f:
            data = json.load(f)
        if data[name][0] == username and data[name][1] == password:
            return True
        return False

    def write_to_file(self, name, username, password, address):
        """Write data to the file if not already existing"""
        with open(FILE_PATH, 'r') as f:
            data = json.load(f)
        with open(FILE_PATH, 'w') as f:
            data[name] = [username, password, address]
            json.dump(data, f)
