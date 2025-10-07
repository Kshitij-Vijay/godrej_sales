import os
import json
from collections import OrderedDict
import shutil

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))  # Absolute path to directory where main.py is located
PRODUCTS_DIR = os.path.join(ROOT_DIR, 'products')
SINGLE_PRODUCT_DIR = os.path.join(ROOT_DIR, 'single_product')


class Navigator:
    def __init__(self):
        self.current_path = PRODUCTS_DIR

    def delete_child_json(self, path, name):
        json_path = os.path.join(path, 'status.json')
        if not os.path.exists(json_path):
            print("No status.json file found.")
            return False

        with open(json_path, 'r') as f:
            data = json.load(f)

        if 'children' in data and isinstance(data['children'], list):
            if name in data['children']:
                data['children'].remove(name)
                with open(json_path, 'w') as f:
                    json.dump(data, f, indent=4)
                print(f"Removed '{name}' from children array.")
                return True
            else:
                print(f"'{name}' not found in children array.")
                return False
        else:
            print("No children array found in the status.json file.")
            return False
        
    def delete_child(self, name):
        target_path = os.path.join(self.current_path, name)
        if os.path.isdir(target_path):
            shutil.rmtree(target_path)
            print(f"Folder '{name}' deleted.")
            return True
        else:
            print(f"Folder '{name}' does not exist.")
            return False


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

    def add_children_json(self, folder_path, new_child):
        json_path = os.path.join(folder_path, 'status.json')

        # Load the existing JSON or initialize if file doesn't exist
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        # Append new child to 'children'
        if 'children' in data and isinstance(data['children'], list):
            data['children'].append(new_child)
        else:
            data['children'] = [new_child]

    # Write updated data back
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)

    def create_group_json(self, folder_name):
        # Path for the new group's json file
        group_folder_path = os.path.join(self.current_path, folder_name)
        json_path = os.path.join(group_folder_path, 'status.json')

        # Example: initial group data, can be customized as needed
        group_data = {
            "name" : folder_name,
            "type": "group"
        }

        # Write data to the json file
        with open(json_path, 'w') as f:
            json.dump(group_data, f, indent=4)

    def list_folders(self):
        return [f for f in os.listdir(self.current_path) if os.path.isdir(os.path.join(self.current_path, f))]

    def show_current_folder(self):
        print(f"Current folder: {os.path.basename(self.current_path)}")

    def show_subfolders(self):
        folders = self.list_folders()
        for i, folder in enumerate(folders, 1):
            print(f"{i}. {folder}")
        return folders

    def go_up(self):
        if self.current_path == PRODUCTS_DIR:
            print("Cannot go up any further from the products folder.")
            return False
        else:
            self.current_path = os.path.dirname(self.current_path)
            return True

    def go_down(self, folder_index, folders):
        if 1 <= folder_index <= len(folders):
            self.current_path = os.path.join(self.current_path, folders[folder_index-1])
            return True
        else:
            print("Invalid folder index.")
            return False

    def create_group_or_item(self):
        choice = input("Create a group (g) or an item (i)? ").strip().lower()
        if choice == 'g':
            self.create_group()
        elif choice == 'i':
            self.create_item()
        else:
            print("Invalid choice. Please enter 'g' or 'i'.")

    def create_group(self):
        while True:
            group_name = input("Enter group name: ").strip()
            if group_name in self.list_folders():
                print("Group with the same name exists. Try again.")
            else:
                self.add_children_json(self.current_path,group_name)
                os.mkdir(os.path.join(self.current_path, group_name))
                print(f"Group '{group_name}' created.")
                self.create_group_json(group_name)
                break

    def create_item(self):
        while True:
            item_name = input("Enter item name: ").strip()
            if item_name in self.list_folders():
                print("Item with the same name exists. Try again.")
            else:
                item_folder_path = os.path.join(self.current_path, item_name)
                os.mkdir(item_folder_path)
                print(f"Item folder '{item_name}' created.")
                self.add_children_json(self.current_path,item_name)
                self.run_item_simple_process(item_folder_path,item_name)
                break

    def run_item_simple_process(self, group_folder_path,item_name):
        import sys
        sys.path.insert(0, SINGLE_PRODUCT_DIR)  
        from single_product.item import item 
        
        original_cwd = os.getcwd()            # Save current working directory
        os.chdir(SINGLE_PRODUCT_DIR)          # Change to 'single_product'
        
        try:
            item_obj = item()
            item_obj.simple_process(name = item_name)
        finally:
            os.chdir(original_cwd)            # Revert to original directory

        self.current_path = group_folder_path

    def run_item_simple_process(self, item_folder_path,item_name):
        import sys
        sys.path.insert(0, SINGLE_PRODUCT_DIR)  
        from single_product.item import item 
        
        original_cwd = os.getcwd()            # Save current working directory
        os.chdir(SINGLE_PRODUCT_DIR)          # Change to 'single_product'
        
        try:
            item_obj = item()
            item_obj.simple_process(name = item_name)
            item_obj.migrate_out(item_folder_path) 
        finally:
            os.chdir(original_cwd)            # Revert to original directory

        self.current_path = item_folder_path

    def get_name(self, folder_path):
        json_path = os.path.join(folder_path, 'status.json')

        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
            return data.get('name')
        else:
            return None
    
    def delete(self):
        # 1. Get the name of the current folder from status.json
        name = self.get_name(self.current_path)
        print("Deleting folder:", name)
        print("Current path:", self.current_path)

        # Save path before going up (current is the folder to delete)
        path_to_delete = self.current_path

        # 2. Go up to parent directory
        self.go_up()
        parent_path = self.current_path
        print("Parent path:", parent_path)

        # 3. Delete the folder by name inside parent
        # (self.current_path is now parent, name is the folder below)
        self.delete_child(name)

        # 4. Update parent's status.json children array
        self.delete_child_json(parent_path, name)




def main():
    navigator = Navigator()
    while True:
        navigator.show_current_folder()
        folders = navigator.show_subfolders()

        user_input = input("Enter command (u-up, c-create, number to go inside folder): ").strip().lower()
        if user_input == 'u':
            navigator.go_up()
        elif user_input == 'c':
            navigator.create_group_or_item()
        elif user_input == 'd':
            navigator.delete()
        elif user_input.isdigit():
            idx = int(user_input)
            navigator.go_down(idx, folders)
        else:
            print("Invalid command.")

if __name__ == '__main__':
    main()
