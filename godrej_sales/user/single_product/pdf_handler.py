import os
import shutil
import tkinter as tk
from tkinter import filedialog
from extractor import extract_pdf_contents

RAW_PDF_FOLDER = os.path.join("raw_data", "pdfs")
EXTRACTED_PDF_FOLDER = os.path.join("extracted_data", "pdfs")

def handle_pdf():
    os.makedirs(RAW_PDF_FOLDER, exist_ok=True)
    os.makedirs(EXTRACTED_PDF_FOLDER, exist_ok=True)
    root = tk.Tk()
    root.withdraw()
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not pdf_path:
        print("No PDF selected.")
        return

    # Gather all PDF files from both locations for consistent naming
    existing_files = os.listdir(RAW_PDF_FOLDER) + os.listdir(EXTRACTED_PDF_FOLDER)
    max_num = 0
    for file in existing_files:
        name, ext = os.path.splitext(file)
        if ext.lower() == ".pdf" and name.isdigit():
            num = int(name)
            if num > max_num:
                max_num = num
    next_num = max_num + 1

    dest_name = f"{next_num}.pdf"
    dest_path_raw = os.path.join(RAW_PDF_FOLDER, dest_name)
    dest_path_extracted = os.path.join(EXTRACTED_PDF_FOLDER, dest_name)

    shutil.copy(pdf_path, dest_path_raw)
    shutil.copy(pdf_path, dest_path_extracted)
    print(f"Copied PDF to {dest_path_raw} and {dest_path_extracted}")

    extract_pdf_contents(dest_path_raw)  # or dest_path_extracted; use whichever you want to analyze

