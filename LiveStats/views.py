from django.shortcuts import render
from .forms import UploadFileForm
from PIL import Image
import pytesseract
from django.conf import settings
import os
import TextParsing
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .SSH import run_stacked_display
from api_calls import SportsAPI as SportsAPI

@csrf_exempt
def run_ssh(request):
    if request.method == "POST":
        data = request.json
        action = data.get("action")
        
        if action == "stackedDisplay":
            response_message = run_stacked_display()
            return JsonResponse({"message": response_message})
    
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

            context = {
        'PlayerArray': arrayOfPlayerNames,
    }
            return render(request, 'result.html', context)
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


## API calls ##
def Get_League_Standings(request):
    API = SportsAPI()
    standings = API.get_league_standings()

    return (request, 'league_standings.html', {'standings': standings})

def stats_page(request):
    return render(request, 'stats_page.html')
