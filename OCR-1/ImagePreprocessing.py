import cv2
from PIL import Image
from matplotlib import pyplot as plt

teams1="Pictures/OCR Team Sample-2.jpg"
teams1_image=cv2.imread(teams1)



# function to display the image.
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

def inverted_image(image):
    inverted_image = cv2.bitwise_not(image)
    cv2.imwrite("Pictures/Inverted Image.png", inverted_image)
    inverted="Pictures/Inverted Image.png"
    return inverted,inverted_image
def grayscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("Pictures/Gray Image.png", gray_image)
    gray="Pictures/Gray Image.png"
    return gray,gray_image


def black_and_white(image):
    gray,gray_image = grayscale(image)
    thresh,black_and_white_image=cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
    cv2.imwrite("Pictures/Black and White.png", black_and_white_image)
    black_and_white="Pictures/Black and White.png"
    return black_and_white, black_and_white_image


def bounding_boxes(image):
    gray,gray_image = grayscale(image)
    blur=cv2.GaussianBlur(gray_image,(7,7),0)
    thresh=cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    index_kernel_image=cv2.getStructuringElement(cv2.MORPH_RECT,(3,13))
    dilate=cv2.dilate(thresh,index_kernel_image,iterations=1)
    cv2.imwrite("Pictures/Index.png",index_kernel_image)
    contours=cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours=contours[0]\
        if len(contours)==2 \
        else contours[1]
    contours=sorted(contours,key=lambda x: cv2.boundingRect(x)[0])
    bounding_box_image = image
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if (h < 30 and w > 36):
            cv2.rectangle(bounding_box_image, (x, y), (x + w, y + h), (36, 255, 12), 2)
    cv2.imwrite("Pictures/Bounding Boxes.png", bounding_box_image)
    bounding_boxes = "Pictures/Bounding Boxes.png"
    return bounding_boxes,bounding_box_image


display_image(teams1)
inverted,inverted_image=inverted_image(teams1_image)
display_image(inverted)
gray,gray_image=grayscale(teams1_image)
display_image(gray)
black_and_white, black_and_white_image=black_and_white(teams1_image)
display_image(black_and_white)
bounding_boxes,bounding_boxes_image=bounding_boxes(teams1_image)
display_image(bounding_boxes)


