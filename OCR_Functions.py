from PIL import Image
import pytesseract



pytesseract.pytesseract.tesseract_cmd = r'path to Tesseract.exe'
#Path to Tesseract.exe on local system must be specified


def OCR_Image(path):
    image = Image.open(path)
    txt = pytesseract.image_to_string(path)
    return txt
#Basic function to take a png file on local system and return a string of text
