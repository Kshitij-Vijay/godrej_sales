import fitz  # PyMuPDF
import base64
from typing import List
from pydantic import BaseModel, Field

class TextBlockModel(BaseModel):
    page: int
    text: str

class ImageModel(BaseModel):
    page: int
    width: int
    height: int
    image_b64: str

class TableModel(BaseModel):
    page: int
    content: str  # Simple text representation of table for now

class PDFContentModel(BaseModel):
    texts: List[TextBlockModel] = Field(default_factory=list)
    images: List[ImageModel] = Field(default_factory=list)
    tables: List[TableModel] = Field(default_factory=list)

def extract_pdf_content(pdf_path: str) -> PDFContentModel:
    doc = fitz.open(pdf_path)
    texts = []
    images = []
    tables = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("blocks")
        page_text = "\n".join(block[4] for block in blocks if block[4].strip())
        if page_text.strip():
            texts.append(TextBlockModel(page=page_num + 1, text=page_text))

        img_list = page.get_images(full=True)
        for img in img_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            images.append(ImageModel(
                page=page_num + 1,
                width=base_image["width"],
                height=base_image["height"],
                image_b64=image_b64
            ))

        for block in blocks:
            text = block[4]
            if "\t" in text or "  " in text:
                tables.append(TableModel(page=page_num + 1, content=text))

    return PDFContentModel(texts=texts, images=images, tables=tables)
