from create import create
from analyser.analyse import analyse_all
from qa import qa
import json
import os

class item:
    def __init__(self):
        self.json_path = os.path.join(os.getcwd(), 'status.json')

    def create_item(self):
        create()

    def analyse_item(self):
        analyse_all()

    def qna(self):
        qa()

    def check_json(self, p):
        with open(self.json_path, 'r') as f:
            data = json.load(f)
        key_map = {'c': 'created', 'a': 'analysed', 'q': 'qna'}
        key = key_map.get(p.lower())
        if key and key in data:
            return data[key]
        else:
            return None

    def set_json(self, p, v):
        with open(self.json_path, 'r') as f:
            data = json.load(f)
        key_map = {'c': 'created', 'a': 'analysed', 'q': 'qna'}
        key = key_map.get(p.lower())
        if key:
            data[key] = v
            with open(self.json_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        else:
            return False

    def make_json(self):
        if not os.path.exists(self.json_path):
            default_data = {
                "created": False,
                "analysed": False,
                "qna": False
            }
            with open(self.json_path, 'w') as f:
                json.dump(default_data, f, indent=4)
            return True
        return False

    def simple_process(self):
        self.make_json()
        self.create_item()
        self.set_json('c',True)
        print("analysing Items ... ")
        self.analyse_item()
        self.set_json('a',True)
        t = input("Do you want to ask questions ? (y/n) \n")
        if(t == 'y'):
            self.qna()



obj = item()
obj.simple_process()
