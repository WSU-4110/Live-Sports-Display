import cv2
import pytest
from matplotlib import pyplot as plt

teams1 = "Pictures/OCR Team Sample.png"
teams1_image = cv2.imread(teams1)


def test_change_image():
    inverted_image = cv2.bitwise_not(teams1_image)
    cv2.imwrite("Pictures/Inverted Image.png", inverted_image)
    inverted = "Pictures/Inverted Image.png"
    return inverted


def test_display_image():
    im_path = test_display_image()
    dpi = 80
    image_data = plt.imread(im_path)
    height, width = image_data.shape[:2]
    FigureSize = width / float(dpi), height / float(dpi)
    Figure = plt.figure(figsize=FigureSize)
    ax = Figure.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.imshow(image_data, cmap='gray')
    plt.show()


def test_change_image():
    gray_image = cv2.cvtColor(teams1_image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("Pictures/Gray Image.png", gray_image)
    gray = "Pictures/Gray Image.png"
    return gray


def test_display_image():
    im_path = test_change_image()
    dpi = 80
    image_data = plt.imread(im_path)
    height, width = image_data.shape[:2]
    FigureSize = width / float(dpi), height / float(dpi)
    Figure = plt.figure(figsize=FigureSize)
    ax = Figure.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.imshow(image_data, cmap='gray')
    plt.show()


def test_change_image():
    gray_image = cv2.cvtColor(teams1_image, cv2.COLOR_BGR2GRAY)
    thresh, black_and_white_image = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
    cv2.imwrite("Pictures/Black and White.png", black_and_white_image)
    black_and_white = "Pictures/Black and White.png"
    return black_and_white


def test_display_image():
    im_path = test_change_image()
    dpi = 80
    image_data = plt.imread(im_path)
    height, width = image_data.shape[:2]
    FigureSize = width / float(dpi), height / float(dpi)
    Figure = plt.figure(figsize=FigureSize)
    ax = Figure.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.imshow(image_data, cmap='gray')
    plt.show()
