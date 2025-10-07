import cv2
import os

def extract_objects_from_image(image_path, output_folder, pdf_name, page_num):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to load image: {image_path}")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)  # isolate non-white

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    obj_folder = os.path.join(output_folder, f"{pdf_name}_page{page_num}")
    os.makedirs(obj_folder, exist_ok=True)

    for i, contour in enumerate(contours, start=1):
        x, y, w, h = cv2.boundingRect(contour)

        if w < 20 or h < 20:  # filter noise small objects
            continue

        obj_img = img[y:y+h, x:x+w]
        obj_path = os.path.join(obj_folder, f"object_{i}.png")
        cv2.imwrite(obj_path, obj_img)
        print(f"Saved object image to {obj_path}")
