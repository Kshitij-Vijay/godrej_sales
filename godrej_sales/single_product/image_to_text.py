from PIL import Image
import pytesseract

def image_to_text(image_path: str) -> str:
    # Open image with PIL
    img = Image.open(image_path)
    
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img)
    
    return text
