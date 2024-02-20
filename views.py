from django.http import HttpResponse

from api_calls import *

# Create your views here.

def say_hello(request):
    return HttpResponse('Hello World')
def say_hello2(request):
    return HttpResponse("Hellllloooooooo!")

def returnInfo(request):
    team_id = "583ed157-fb46-11e1-82cb-f4ce4684ea4c"
    return HttpResponse(returnData(team_id))