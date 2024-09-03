import json

class GraphManager:
    def __init__(self, json_file):
        self.json_file = json_file

    def get_data(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
        return data

    def add_data(self, new_data):
        data = self.get_data()
        data.append(new_data)
        with open(self.json_file, 'w') as file:
            json.dump(data, file)
