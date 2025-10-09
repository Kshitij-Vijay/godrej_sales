from create import create
from analyser.analyse import analyseee
from embeddings import store_embeds
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
        analyseee()
        store_embeds()

    def re_analyse(self):
        # only deletes summaries and again analyses extracted data
        from chat_handler import re_analyse
        re_analyse()

        

    def chat(self):
        from chat import chatbot
        chatbot()


    def check_json(self, p):  # to check json param
        if not os.path.exists(self.json_path):
            return None  # Return None if file does not exist

        with open(self.json_path, 'r') as f:
            data = json.load(f)

        key_map = {'c': 'created', 'a': 'analysed', 'q': 'qna'}
        key = key_map.get(p.lower())
        if key and key in data:
            return data[key]
        else:
            return None


    def set_json(self, p, v):  # to add json param
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

    def make_json(self):  # to make the initial json file
        if not os.path.exists(self.json_path):
            default_data = {
                    "created": True,
                    "analysed": False,
                }
            with open(self.json_path, 'w') as f:
                json.dump(default_data, f, indent=4)
            return True
        return False
    
    def add_name(self,name): # adding name to the json file
        json_path = os.path.join(os.getcwd(), 'status.json')

        with open(json_path, 'r') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        new_data = OrderedDict([('name', name)])
        new_data.update(data)

        with open(json_path, 'w') as f:
            json.dump(new_data, f, indent=4)
    
    def add_type(self,ty):  # to add item or group
        json_path = os.path.join(os.getcwd(), 'status.json')

        with open(json_path, 'r') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        new_data = OrderedDict([('type', ty)])
        new_data.update(data)

        with open(json_path, 'w') as f:
            json.dump(new_data, f, indent=4)

    def add_json_param(self,param,val): # add json param
        json_path = os.path.join(os.getcwd(), 'status.json')

        with open(json_path, 'r') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        new_data = OrderedDict([(param, val)])
        new_data.update(data)

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

    def initialize(self):
        folders = ['summaries', 'extracted_data', 'raw_data']
        file = 'status.json'

        for folder in folders:
            if os.path.exists(folder) and os.path.isdir(folder):
                shutil.rmtree(folder)
                print(f"Deleted folder: {folder}")
            else:
                print(f"Folder not found: {folder}")

        if os.path.exists(file) and os.path.isfile(file):
            os.remove(file)
            print(f"Deleted file: {file}")
        else:
            print(f"File not found: {file}")

    def first_cry(self):  #call this method when creating the item for the first time
        print("This item has no data. Start by adding data \n")
        self.make_json()  # making the initial json file
        self.add_type("item") # adding name to the item
        name = input("enter name : \n") 
        self.add_name(name)
        self.create_item()  # adding data
        self.set_json('c',True)  # making the item created
        c = input("Do you want to verify (y/n)??")
        if c == 'y':
            from verify import verify_main
            verify_main()
        print("analysing Items ... ")
        self.analyse_item()
        self.set_json('a',True)
        t = input("Do you want to ask questions ? (y/n) \n")
        if(t == 'y'):
            self.chat()


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
            self.chat()

    def usage(self):
        print("usage")  # in the method
        created = self.check_json('c')
        if created == True:
            print("The item has been created aldready, what do you want to do ? \n")
            option = input(" \n1. Add data or Verify \n2. Analyse again\n3. QNA\n")
            if option == '1':
                self.create_item()
                c = input("Do you want to verify (y/n)??")
                if c == 'y':
                    from verify import verify_main
                    verify_main()
            elif option == '2':
                self.re_analyse()
            elif option == '3':
                self.chat()
        else:
            self.first_cry()  
            



it = item()
# it.initialize()
it.usage()
