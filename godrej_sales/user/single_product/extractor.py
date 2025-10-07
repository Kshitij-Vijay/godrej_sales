import os
import fitz  # PyMuPDF
from image_to_text import image_to_text
from image_to_object import extract_objects_from_image  # new module

EXTRACTED_FOLDER = "extracted_data"
TEXT_FOLDER = os.path.join(EXTRACTED_FOLDER, "texts")
IMAGE_FOLDER = os.path.join(EXTRACTED_FOLDER, "images")
OBJECTS_FOLDER = os.path.join(EXTRACTED_FOLDER, "objects")  # folder for extracted object images

def extract_pdf_contents(pdf_path):
    os.makedirs(TEXT_FOLDER, exist_ok=True)
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    os.makedirs(OBJECTS_FOLDER, exist_ok=True)

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    doc = fitz.open(pdf_path)
    combined_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Render page as PNG image
        pix = page.get_pixmap()
        img_filename = f"{pdf_name}_page{page_num+1}.png"
        img_path = os.path.join(IMAGE_FOLDER, img_filename)
        pix.save(img_path)
        print(f"Saved page image to {img_path}")

        # Extract objects from the page image using OpenCV
        extract_objects_from_image(img_path, OBJECTS_FOLDER, pdf_name, page_num + 1)

        # Get OCR text from image_to_text
        page_text = image_to_text(img_path)
        combined_text += page_text + "\n"

    # Save combined OCR text for all pages
    text_path = os.path.join(TEXT_FOLDER, f"{pdf_name}.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(combined_text)
    print(f"OCR text extracted to {text_path}")
