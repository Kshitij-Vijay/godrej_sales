import os
import csv
from analyser.blip_image_text import blip_image_text

def analyse_images(questions):
    # Go into the images folder
    images_dir = os.path.join(os.getcwd(), 'extracted_data', 'images')
    summaries_folder = os.path.join(os.getcwd(), 'summaries')
    os.makedirs(summaries_folder, exist_ok=True)
    output_csv = os.path.join(summaries_folder, 'images.csv')

    results = []

    # Iterate through each image file in the images directory
    for img_file in os.listdir(images_dir):
        img_path = os.path.join(images_dir, img_file)
        if os.path.isfile(img_path) and img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
            print(f"Processing image: {img_file}")
            out = blip_image_text(img_path, questions)  # returns dictionary with 'qna' and 'summary'
            results.append([img_file, out['qna'], out['summary']])

    # Write results to CSV
    with open(output_csv, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'qna', 'summary'])  # Header
        writer.writerows(results)

    print(f"Analysis complete. CSV saved to {output_csv}")

# Example usage:
if __name__ == "__main__":
    questions = ["What is in the image?", "Describe the colors."]
    analyse_images(questions)
