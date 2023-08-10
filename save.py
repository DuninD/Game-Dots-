import json


class SavingSystem:
    def __init__(self):
        self.data = self.read('users.json')

    def write(self, data, filename):
        data = json.dumps(data)
        data = json.loads(str(data))
        with open(filename, 'w') as file:
            json.dump(data, file)

    def read(self, filename):
        with open(filename, 'r') as file:
            return json.load(file)
