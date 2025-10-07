import os
import csv
from pathlib import Path
from analyser.blip_image_text import blip_image_text

# Assuming blip_image_text and dependencies are imported or defined above

def analyse_images(questions):
    root_dir = Path(__file__).parent.parent.resolve()  # root folder of your project
    images_dir = root_dir / 'extracted_data' / 'images'
    output_dir = root_dir / 'extracted_data' / 'texts'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = output_dir / 'image_analysis_summary.csv'

    results = []

    for img_file in images_dir.iterdir():
        if img_file.is_file() and img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            print(f"Processing image: {img_file.name}")
            out = blip_image_text(str(img_file), questions)
            results.append([img_file.name, out['qna'], out['summary']])

    with open(output_csv, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['image_name', 'qna', 'summary'])
        writer.writerows(results)

    print(f"Analysis complete. CSV saved to {output_csv}")

# Example usage:
if __name__ == "__main__":
    questions = ["What is in the image?", "Describe the colors."]
    analyse_images(questions)
