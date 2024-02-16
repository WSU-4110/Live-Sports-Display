import cv2
from PIL import Image
from matplotlib import pyplot as plt

image_file = "Pictures/Sample.png"
image = cv2.imread(image_file)


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


# function to invert the image.
def inverted_image(image):
    inverted_image = cv2.bitwise_not(image)
    cv2.imwrite("Pictures/inverted.png", inverted_image)
    display_image("Pictures/inverted.png")


def grayscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("Pictures/gray_image.png", gray_image)
    display_image("Pictures/gray_image.png")

def black_and_white(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh,black_and_white=cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
    cv2.imwrite("Pictures/black_and_white.png", black_and_white)
    display_image("Pictures/black_and_white.png")
    return black_and_white

def noise_removal(image):
    black_and_white_image=black_and_white(image)
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    black_and_white_image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    black_and_white_image = cv2.erode(image, kernel, iterations=1)
    black_and_white_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    black_and_white_image = cv2.medianBlur(image, 3)
    noise_removed=cv2.imwrite("temp/no_noise.jpg", black_and_white_image)
    display_image(noise_removed)
    return (black_and_white_image)


display_image(image_file)
inverted_image(image)
grayscale(image)
black_and_white(image)
noise_removal(image)
