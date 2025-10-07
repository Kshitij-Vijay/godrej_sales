from create import create
from analyser.analyse import analyse_all
from qa import qa
import json
import os
import shutil
from collections import OrderedDict

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
                    "created": True,
                    "analysed":True,
                    "qna": False
                }
            with open(self.json_path, 'w') as f:
                json.dump(default_data, f, indent=4)
            return True
        return False
    
    def add_name(self,name):
        json_path = os.path.join(os.getcwd(), 'status.json')

        # Load existing data preserving order
        with open(json_path, 'r') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        # Create new OrderedDict with 'type' first
        new_data = OrderedDict([('name', name)])
        new_data.update(data)

        # Write updated data back to the file
        with open(json_path, 'w') as f:
            json.dump(new_data, f, indent=4)
    
    def add_type(self,ty):
        json_path = os.path.join(os.getcwd(), 'status.json')

        # Load existing data preserving order
        with open(json_path, 'r') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        # Create new OrderedDict with 'type' first
        new_data = OrderedDict([('type', ty)])
        new_data.update(data)

        # Write updated data back to the file
        with open(json_path, 'w') as f:
            json.dump(new_data, f, indent=4)

    def add_json_param(self,param,val):
        json_path = os.path.join(os.getcwd(), 'status.json')

        # Load existing data preserving order
        with open(json_path, 'r') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        # Create new OrderedDict with 'type' first
        new_data = OrderedDict([(param, val)])
        new_data.update(data)

        # Write updated data back to the file
        with open(json_path, 'w') as f:
            json.dump(new_data, f, indent=4)
    
    def migrate_out(self, item_folder_path):
        folders_to_move = ['raw_data', 'extracted_data', 'metadata']
        files_to_move = ['status.json']

        single_product_dir = os.path.abspath(os.path.dirname(__file__))

        for folder in folders_to_move:
            src_folder = os.path.join(single_product_dir, folder)
            dest_folder = os.path.join(item_folder_path, folder)
            if os.path.exists(src_folder):
                if os.path.exists(dest_folder):
                    shutil.rmtree(dest_folder)
                shutil.move(src_folder, dest_folder)

        for file in files_to_move:
            src_file = os.path.join(single_product_dir, file)
            dest_file = os.path.join(item_folder_path, file)
            if os.path.exists(src_file):
                if os.path.exists(dest_file):
                    os.remove(dest_file)
                shutil.move(src_file, dest_file)

    def migrate_in(self, item_folder_path):
        folders_to_copy = ['raw_data', 'extracted_data', 'metadata']
        files_to_copy = ['status.json']

        single_product_dir = os.path.abspath(os.path.dirname(__file__))

        for folder in folders_to_copy:
            src_folder = os.path.join(item_folder_path, folder)
            dest_folder = os.path.join(single_product_dir, folder)
            if os.path.exists(src_folder):
                # Remove existing destination folder if it exists
                if os.path.exists(dest_folder):
                    shutil.rmtree(dest_folder)
                shutil.copytree(src_folder, dest_folder)

        for file in files_to_copy:
            src_file = os.path.join(item_folder_path, file)
            dest_file = os.path.join(single_product_dir, file)
            if os.path.exists(src_file):
                if os.path.exists(dest_file):
                    os.remove(dest_file)
                shutil.copy2(src_file, dest_file)

    def new_group(self,name):
        print("new_group")
        self.make_json()
        self.add_type("group")
        self.add_name(name)

    def simple_process(self,name):
        print("simple process")
        self.make_json()
        self.add_type("item")
        self.add_name(name)
        self.create_item()
        self.set_json('c',True)
        print("analysing Items ... ")
        self.analyse_item()
        self.set_json('a',True)
        t = input("Do you want to ask questions ? (y/n) \n")
        if(t == 'y'):
            self.qna()

    def usage(self):
        print("usage")
        self.make_json()
        self.add_type("item")
        name = input("enter name : \n")
        self.add_name(name)
        self.create_item()
        self.set_json('c',True)
        print("analysing Items ... ")
        self.analyse_item()
        self.set_json('a',True)
        t = input("Do you want to ask questions ? (y/n) \n")
        if(t == 'y'):
            self.qna()



it = item()
it.usage()
