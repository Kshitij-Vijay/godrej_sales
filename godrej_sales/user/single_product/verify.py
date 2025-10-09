import os
import pandas as pd
from PIL import Image

def manage_text_file(file_path): # to process a single text file
    edited = False
    if not os.path.exists(file_path):
        print("File does not exist.")
        return

    with open(file_path, 'r') as file:
        content = file.read()
    print("File content:\n")
    print(content)

    action = input("\nPress 'e' to edit, 's' to save as is, or 'd' to delete: ").lower()

    if action == 's':
        print("File saved as it is. Exiting.")
        return edited

    elif action == 'd':
        os.remove(file_path)
        print(f"File {file_path} deleted.")
        edited = True
        return edited

    elif action == 'e':
        print("\nEnter the new content below. To finish, enter a line with only 'EOF' and press Enter:\n")
        new_lines = []
        while True:
            line = input()
            if line == "EOF":
                break
            new_lines.append(line)
        new_content = "\n".join(new_lines)
        with open(file_path, 'w') as file:
            file.write(new_content)
        print(f"\nFile {file_path} saved with new content.")
        edited = True
        return edited

    else:
        print("Invalid option. Exiting.")
        return edited



def open_image(image_path):
    print(image_path)
    img = Image.open(image_path)
    img.show()


def process_images():
    summaries_path = os.path.join('summaries', 'images.csv')
    images_folder = os.path.join('extracted_data', 'images')
    edited = False
    if not os.path.exists(summaries_path):
        print("images.csv file does not exist in summaries folder.")
        return edited

    df = pd.read_csv(summaries_path)

    for index, row in df.iterrows():
        image_name = row['name']
        summary = row['summary']
        image_path = os.path.join(images_folder, image_name)

        if not os.path.exists(image_path):
            print(f"Image {image_name} not found.")
            continue

        print(f"Image: {image_name}")
        input("Press Enter to open the image...")
        open_image(image_path)

        input("Press Enter after viewing the image...")

        print(f"Summary: {summary}")
        action = input("Press 'e' to edit the summary, 'd' to delete the image, 'n' to next image: ").lower()

        if action == 'd':
            os.remove(image_path)
            df.drop(index, inplace=True)
            edited = True
            print(f"Deleted {image_name} and removed from CSV.")
        elif action == 'e':
            new_summary = input("Enter new summary: ")
            df.at[index, 'summary'] = new_summary
            edited = True
            print("Summary updated.")
        elif action == 'n':
            continue
        else:
            print("Invalid input, moving to next image.")

    df.to_csv(summaries_path, index=False)
    print("Finished processing images.")
    return edited

    
def process_folder_all(folder_path): # to process all the files when the folder location is given
    text_files = []
    other_files = []
    edited = False
    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)
        if os.path.isfile(full_path):
            if file.lower().endswith('.txt'):
                text_files.append(full_path)
            else:
                other_files.append(full_path)

    print(f"\nFound {len(text_files)} text files and {len(other_files)} other files in {folder_path}")

    for text_file in text_files:
        print(f"\nManaging text file: {text_file}")
        b = manage_text_file(text_file)
        if b == True:
            edited = True

    return edited



def process_folder(folder_path): # to select and process specific files when location is given
    edited = False
    text_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.txt') and os.path.isfile(os.path.join(folder_path, f))]

    if not text_files:
        print("\nNo text files found in", folder_path)
        return

    while True:
        print("\nText files in", folder_path)
        for idx, file in enumerate(text_files, start=1):
            print(f"{idx}. {file}")
        print("exit. Exit this menu")

        choice = input("\nEnter the number of the file to edit, 'a' for all, or 'exit' to quit: ").lower()

        if choice == 'exit':
            print("Exiting text file editor.")
            break

        elif choice == 'a':
            for file in text_files:
                print(f"\nManaging file: {file}")
                b = manage_text_file(os.path.join(folder_path, file))
                if b == True:
                    edited = True

        else:
            try:
                num = int(choice)
                if 1 <= num <= len(text_files):
                    file_to_edit = os.path.join(folder_path, text_files[num - 1])
                    b = manage_text_file(file_to_edit)
                    if b == True:
                        edited = True
                else:
                    print("Invalid file number.")
            except ValueError:
                print("Invalid input, please enter a number, 'a', or 'exit'.")

    
    return edited


def verify_main():
    base_folder = 'extracted_data'
    if not os.path.exists(base_folder) or not os.path.isdir(base_folder):
        print(f"Folder {base_folder} does not exist.")
        return

    edited = False

    subfolders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]

    if not subfolders:
        print("No subfolders found in extracted_data.")
        return

    print("Subfolders in 'extracted_data':")
    for idx, folder in enumerate(subfolders, start=1):
        print(f"{idx}. {folder}")

    while True:
        try:
            c = input("\nEnter the number of the folder to process ['exit' to go out]: ")
            choice = int(c)
            if c == 'exit':
                break
            if 1 <= choice <= len(subfolders):
                selected_folder = os.path.join(base_folder, subfolders[choice - 1])
                b = process_folder(selected_folder)
                if b == True:
                    edited = True
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    c = input("Do you want to verify images(y/n) ??")
    if c == 'y':
        b = process_images()
        if b == True:
            edited = True

    if edited == True:
        print("Changes have been made. Re-analysing...")
        from create import re_analyse
        re_analyse()


if __name__ == "__main__":
    verify_main()
