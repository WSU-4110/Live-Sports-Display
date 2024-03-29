
import cv2
import numpy as np
import matplotlib.pyplot as plt





def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    #Using GaussianBlur to bring out edges in the image

    kernel = np.ones((3, 3), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    #Using dialation to bring out edges

    return image


