from django.shortcuts import render
from .forms import UploadFileForm
from PIL import Image
import pytesseract
from django.conf import settings
import os
import TextParsing
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .SSH import run_stacked_display
from django.views.decorators.http import require_http_methods
import json
from LSDtest1.testingcelery import my_background_task



@csrf_exempt
def run_ssh(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))  # Parse the JSON data
            action = data.get("action")
            
            if action == "stackedDisplay":
                # Offload the long-running operation to a background task
                # response_message = run_stacked_display()  # This needs to be offloaded
                my_background_task.delay(arg1, arg2)
                # Temporarily, return an immediate response for testing
                return JsonResponse({"message": "Stacked display operation initiated"})
        except json.JSONDecodeError as e:
            # Handle JSON decoding error (malformed JSON)
            return JsonResponse({"message": "Invalid JSON format"}, status=400)

    # If the request method isn't POST or if the action is not specified or recognized
    return JsonResponse({"message": "Invalid request"}, status=400)
    
#pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe" #requires local path
def handle_uploaded_file(f, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

#2/19-Jordan
def home_view(request):
    return render(request, 'home.html')

#jordan testing git
#yuh

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

""" #old function 
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
