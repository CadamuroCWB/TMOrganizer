from pdf2image import convert_from_path
from cv2 import cv2
from numpy import np
from PIL import Image

import pytesseract

def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def save_images(images, output_folder):
    for i, img in enumerate(images):
        img.save(f"{output_folder}/page_{i + 1}.png", "PNG")

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text
