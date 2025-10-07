import pandas as pd
import os
from PIL import Image

CSV_PATH = os.path.join('extracted_data', 'texts', 'image_analysis_summary.csv')
IMAGES_PATH = os.path.join('extracted_data', 'images')

COLUMN_NAMES = ["column_1", "column_2", "column_3"]  # No header in file

def open_image(img_path):
    try:
        img = Image.open(img_path)
        img.show()
    except Exception as e:
        print(f"Error opening {img_path}: {e}")

def edit_value(prompt, current_value):
    print(f"{prompt} (leave blank to keep current): {current_value}")
    new_value = input("New value: ").strip()
    return new_value if new_value else current_value

def process_images():
    df = pd.read_csv(CSV_PATH, names=COLUMN_NAMES, header=None)
    i = 0
    while i < len(df):
        row = df.iloc[i]
        image_file = row['column_1']
        img_full_path = os.path.join(IMAGES_PATH, image_file)

        if not os.path.exists(img_full_path):
            print(f"Image {image_file} not found. Skipping.")
            i += 1
            continue

        print(f"\n=== Reviewing {image_file} ({i+1}/{len(df)}) ===")
        open_image(img_full_path)
        input("(Press Enter to continue...)")

        while True:
            print(f"\nImage Name: {row['column_1']}")
            print("Press [e] to edit name, [g] to edit description, [d] to delete, [Enter] to go to next.")

            cmd = input("> ").strip().lower()
            if cmd == 'e':
                new_name = edit_value("Edit Image Name", row['column_1'])
                if new_name != row['column_1']:
                    new_path = os.path.join(IMAGES_PATH, new_name)
                    if not os.path.exists(new_path):
                        os.rename(img_full_path, new_path)
                        df.at[i, 'column_1'] = new_name
                        img_full_path = new_path
                        print("Image name updated.")
                    else:
                        print("A file with that name already exists. Name not changed.")
            elif cmd == 'g':
                new_desc = edit_value("Edit Description", row['column_3'])
                df.at[i, 'column_3'] = new_desc
                print("Description updated.")
            elif cmd == 'd':
                confirm = input("Are you sure you want to delete this image? (y/n): ").strip().lower()
                if confirm == 'y':
                    try:
                        os.remove(img_full_path)
                        print(f"Deleted {img_full_path}")
                    except Exception as ex:
                        print(f"Could not delete {img_full_path}: {ex}")
                    df = df.drop(df.index[i]).reset_index(drop=True)
                    i -= 1
                    break
            else:
                break
        df.to_csv(CSV_PATH, index=False, header=False)  # Write no headers
        i += 1

if __name__ == "__main__":
    process_images()
