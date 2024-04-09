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
from .tasks import my_background_task
from api_calls import SportsAPI
import paramiko
import time

@csrf_exempt
def run_stacked_display(request):
    if request.method == "POST":
        hostname = 'us2.pitunnel.com'  
        username = 'timkosinski'  
        password = '20010972'  
        port = 60735  #Will change every bootup!

        player_names = "Deandre Ayton,Jabari Walker,Random"
        
        execute_command = (
            f"echo '{player_names}' > /home/timkosinski/rpi-rgb-led-matrix/bindings/python/samples/Players.txt "
        )


        try:
            # Initialize the SSH client with settings for PiTunnel access
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, port=port, username=username, password=password)
        
            # Execute the Python script with TTY
            stdin, stdout, stderr = client.exec_command(execute_command, get_pty=True)
        
            # Read the output and error if needed
            output = stdout.read().decode()
            errors = stderr.read().decode()
            print(output)
            print(errors)
        finally:
            client.close()
        
        return JsonResponse({"message": "Stacked display command executed successfully."})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def run_single_display(request):
    if request.method == "POST":
        hostname = 'us2.pitunnel.com'
        username = 'jordan'
        password = 'CSC4110LSD'
        port = 41315

        player_names = "Deandre Ayton,Jabari Walker,Random"
        
        execute_command = (
            "sudo -S bash -c '"
            "python3 -m venv /env1; "
            "source /env1/bin/activate; "
            "/home/jordan/env1/pyscripts/strandtest.py'"
        )


        try:
            # Initialize the SSH client with settings for PiTunnel access
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, port=port, username=username, password=password)
        
            # Execute the Python script with TTY
            stdin, stdout, stderr = client.exec_command(execute_command, get_pty=True)
        
            # Read the output and error if needed
            output = stdout.read().decode()
            errors = stderr.read().decode()
            print(output)
            print(errors)
        finally:
            client.close()
        
        return JsonResponse({"message": "Single display command executed successfully."})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


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


def OCR_Image(path):
    image = Image.open(path)
    text = pytesseract.image_to_string(image)
    return text


## API calls ##
def Get_League_Standings(request):
    API = SportsAPI()
    standings = API.get_league_standings()

    return render(request, 'league_standings.html', {'standings': standings})

def Get_Game_Schedule(request):
    API = SportsAPI()
    schedule = API.get_current_schedule()

    return render(request, 'game_schedule.html', {'schedule': schedule})

def Get_Live_Team_Stats(request):
    inputted_team_name = request.GET.get('inputted_team_name', '')
    API = SportsAPI()
    stats = API.get_live_team_stats(inputted_team_name)

    context = {
        'stats': stats,
        'inputted_team_name': inputted_team_name
    }
    return render(request, 'live_team_stats.html', context)

def Get_Live_Game_Stats(request):
    inputted_team_name = request.GET.get('inputted_team_name', '')
    API = SportsAPI()
    stats = API.get_live_game_stats(inputted_team_name)

    context = {
        'stats': stats,
        'inputted_team_name': inputted_team_name
    }
    return render(request, 'live_game_stats.html', context)

def Get_Live_Player_Stats(request):
    inputted_player_name = request.GET.get('inputted_player_name', '')
    API = SportsAPI()
    stats = API.get_live_player_stats(inputted_player_name)

    context = {
        'stats': stats,
        'inputted_player_name': inputted_player_name
    }
    return render(request, 'live_player_stats.html', context)
    
def stats_page(request):
    return render(request, 'stats_page.html')

