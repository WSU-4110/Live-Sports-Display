from django.shortcuts import render
from .forms import UploadFileForm
from PIL import Image
import pytesseract
from django.conf import settings
import os
import TextParsing

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\17344\Desktop\djangotest\djangotest2\Lib\site-packages\pytesseract\pytesseract.py'
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
def handle_uploaded_file(f, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

#2/19-Jordan
def home_view(request):
    return render(request, 'home.html')


def upload_and_ocr(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            # Use TextParsing to process the image and extract player names
            arrayOfPlayerNames = TextParsing.imageToPlayerNames(file_path)
            # For demonstration, join names into a string to display. Adjust as necessary.
            playerNamesText = ', '.join(arrayOfPlayerNames)
            return render(request, 'result.html', {'text': playerNamesText})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

"""
def upload_and_ocr(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            text = OCR_Image(file_path)
            return render(request, 'result.html', {'text': text})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
"""

def OCR_Image(path):
    image = Image.open(path)
    text = pytesseract.image_to_string(image)
    return text
