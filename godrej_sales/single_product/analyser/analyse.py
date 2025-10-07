import os
import json
from analyser.text_analyser import embed_text
from analyser.pdf_analyser import embed_pdf, extract_pdf_content
from analyser.metadata import TextFileMetadata
from analyser.clean_text import clean_text
from analyser.text_summary import summarize_text
from analyser.image_analyser import analyse_images

EXTRACTED_TEXT_FOLDER = "extracted_data/texts"
EXTRACTED_PDF_FOLDER = "extracted_data/pdfs"
METADATA_FOLDER = "metadata"

def analyse_texts():
    metadata_list = []
    summaries = []

    for file_name in os.listdir(EXTRACTED_TEXT_FOLDER):
        if not file_name.endswith(".txt"):
            continue

        file_path = os.path.join(EXTRACTED_TEXT_FOLDER, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        # Clean the noisy OCR text
        cleaned_text = clean_text(raw_text)

        # Summarize the cleaned text
        summary = summarize_text(cleaned_text)
        summaries.append(summary)

        # Embed the cleaned text for metadata
        embedding = embed_text(cleaned_text)
        description = f"Embedding for cleaned & summarized text file {file_name}"

        metadata = TextFileMetadata(
            path=file_path,
            description=description,
            embedding=embedding
        )
        metadata_list.append(metadata)

        print(f"Processed, cleaned, summarized, and embedded {file_name}")

    # Save combined summaries into single text file
    os.makedirs(METADATA_FOLDER, exist_ok=True)
    combined_path = os.path.join(METADATA_FOLDER, "texts.txt")
    with open(combined_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(summaries))

    print(f"Saved combined summaries into {combined_path}")

    return metadata_list

def analyse_pdfs():
    metadata_list = []

    for file_name in os.listdir(EXTRACTED_PDF_FOLDER):
        if not file_name.endswith(".pdf"):
            continue

        file_path = os.path.join(EXTRACTED_PDF_FOLDER, file_name)
        print(f"[INFO] Extracting and embedding PDF: {file_name}")

        pdf_content = extract_pdf_content(file_path)
        print(f"[INFO] Extracted {len(pdf_content.texts)} texts, {len(pdf_content.images)} images, {len(pdf_content.tables)} tables.")

        embedding_vectors = embed_pdf(file_path)
        description = f"Embedding vectors for PDF file {file_name}"

        metadata = TextFileMetadata(
            path=file_path,
            description=description,
            embedding=embedding_vectors
        )
        metadata_list.append(metadata)

        print(f"Processed and embedded {file_name}")

    return metadata_list

def analyse_all():
    text_metadata = analyse_texts()
    pdf_metadata = analyse_pdfs()
    img_metadata = analyse_images()

    all_metadata = text_metadata + pdf_metadata

    output_path = os.path.join(METADATA_FOLDER, "all_metadata.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([m.model_dump() for m in all_metadata], f, indent=2)

    print(f"Saved combined metadata for {len(all_metadata)} items to {output_path}")

if __name__ == "__main__":
    analyse_all()
