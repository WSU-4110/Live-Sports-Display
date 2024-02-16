import cv2
from PIL import Image
from matplotlib import pyplot as plt
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
image_file="Pictures/OCR Team Sample.png"
teams_image=cv2.imread(image_file)
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
ocr=pytesseract.image_to_string(teams_image)
print(ocr)

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
def bounding_box(im_path):
    for c in contours:
        x,y,w,h=cv2.boundingRect(c)
        if (h<30 and w>36):
            roi=image_file[y:y+h, x:x+h]
            cv2.imwrite("Index.png",roi)
            cv2.rectangle(teams_image,(x,y),(x+w,y+h),(36,255,12),2)
            display_image(roi)
    cv2.imwrite("Pictures/BoxedTeams.png",teams_image)
    boxed_teams="Pictures/BoxedTeams.png"
    display_image(boxed_teams)


#display_image(image_file)
bounding_box(image_file)
