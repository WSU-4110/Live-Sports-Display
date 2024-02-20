import cv2
from matplotlib import pyplot as plt
import pytesseract
from nba_api.stats.static import players

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
image_file="Pictures/OCR Team Sample.png"
image_file_2="Pictures/OCR Team Sample-2.jpg"
teams_image=cv2.imread(image_file)
teams_image_2=cv2.imread(image_file_2)

"""
These are lines of code for image preprocessing.
gray_color=cv2.cvtColor(teams_image,cv2.COLOR_BGR2GRAY)
cv2.imwrite("Pictures/gray_image.png",gray_color)
blur=cv2.GaussianBlur(gray_color,(7,7),0)
thresh=cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
kernal=cv2.getStructuringElement(cv2.MORPH_RECT,(3,13))
dilate=cv2.dilate(thresh,kernal,iterations=1)
cv2.imwrite("Pictures/index_kernal.png",kernal)
contours=cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
contours=contours[0]\
    if len(contours)==2 \
    else contours[1]
contours=sorted(contours,key=lambda x: cv2.boundingRect(x)[0])
"""
#This is where the PyTesseract OCR scans the images.
ocr=pytesseract.image_to_string(teams_image)
ocr_2=pytesseract.image_to_string(teams_image_2)
print(ocr)
print(ocr_2)

"""
This is the function to display the image.
def display_image(im_path):
    dpi = 80
    image_data = plt.imread(im_path)
    height, width = image_data.shape[:2]
    FigureSize = width / float(dpi), height / float(dpi)
    Figure = plt.figure(figsize=FigureSize)
    ax = Figure.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.imshow(image_data, cmap='gray')
    plt.show()

This is the function to create bounding boxes across parts of the pictures, which can help with image preprocessing
in order to accurately OCR the text.
def bounding_box(im_path):
    for c in contours:
        x,y,w,h=cv2.boundingRect(c)
        if (h<30 and w>36):
            cv2.rectangle(teams_image,(x,y),(x+w,y+h),(36,255,12),2)
    cv2.imwrite("Pictures/BoxedTeams.png",teams_image)
    boxed_teams="Pictures/BoxedTeams.png"
    display_image(boxed_teams)
"""
#This is the function for making comparison with OCR

def playerlist():
    all_players = players.get_players()
    players_in_string = ""
    for player in all_players:
        players_in_string += ' ' + player['full_name'] + '\n'
    return players_in_string
def clear_input(input):
    all_players = players.get_players()
    players_in_string=playerlist()
    print(players_in_string)
    string_input=set(input.split())
    string_players=set(players_in_string.split())
    cleaned=string_input&string_players
    return cleaned

#Test for OCR refinement.
ocr_clean=clear_input(ocr)
ocr_clean_2=clear_input(ocr_2)
print("Clean Test 1: ",ocr_clean)
print("Clean Test 2: ",ocr_clean_2)