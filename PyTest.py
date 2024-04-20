import cv2
import pytest
from matplotlib import pyplot as plt
teams1 = "Pictures/OCR Team Sample.png"
teams1_image = cv2.imread(teams1)


class Testing:

    def __init__(self):
        self.ChangeImage()
        self.DisplayImage()

    def ChangeImage(self):
        pass

    def DisplayImage(self):
        pass


class InvertedImage:
    def ChangeImage(self):
        inverted_image = cv2.bitwise_not(teams1_image)
        cv2.imwrite("Pictures/Inverted Image.png", inverted_image)
        inverted = "Pictures/Inverted Image.png"
        return inverted

    def DisplayImage(self):
        im_path = self.ChangeImage()
        dpi = 80
        image_data = plt.imread(im_path)
        height, width = image_data.shape[:2]
        FigureSize = width / float(dpi), height / float(dpi)
        Figure = plt.figure(figsize=FigureSize)
        ax = Figure.add_axes([0, 0, 1, 1])
        ax.axis('off')
        ax.imshow(image_data, cmap='gray')
        plt.show()

class GrayScale:
    def ChangeImage(self):
        gray_image = cv2.cvtColor(teams1_image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("Pictures/Gray Image.png", gray_image)
        gray = "Pictures/Gray Image.png"
        return gray

    def DisplayImage(self):
        im_path = self.ChangeImage()
        dpi = 80
        image_data = plt.imread(im_path)
        height, width = image_data.shape[:2]
        FigureSize = width / float(dpi), height / float(dpi)
        Figure = plt.figure(figsize=FigureSize)
        ax = Figure.add_axes([0, 0, 1, 1])
        ax.axis('off')
        ax.imshow(image_data, cmap='gray')
        plt.show()

class BlackAndWhite:
    def ChangeImage(self):
        gray_image = cv2.cvtColor(teams1_image, cv2.COLOR_BGR2GRAY)
        thresh, black_and_white_image = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
        cv2.imwrite("Pictures/Black and White.png", black_and_white_image)
        black_and_white = "Pictures/Black and White.png"
        return black_and_white

    def DisplayImage(self):
        im_path = self.ChangeImage()
        dpi = 80
        image_data = plt.imread(im_path)
        height, width = image_data.shape[:2]
        FigureSize = width / float(dpi), height / float(dpi)
        Figure = plt.figure(figsize=FigureSize)
        ax = Figure.add_axes([0, 0, 1, 1])
        ax.axis('off')
        ax.imshow(image_data, cmap='gray')
        plt.show()

class Bounding_Boxes:

    def ChangeImage(self):
        gray_image = cv2.cvtColor(teams1_image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray_image, (7, 7), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        index_kernel_image = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
        dilate = cv2.dilate(thresh, index_kernel_image, iterations=1)
        cv2.imwrite("Pictures/Index.png", index_kernel_image)
        contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] \
            if len(contours) == 2 \
            else contours[1]
        contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
        bounding_box_image = teams1_image
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if (h < 30 and w > 36):
                cv2.rectangle(bounding_box_image, (x, y), (x + w, y + h), (36, 255, 12), 2)
        cv2.imwrite("Pictures/Bounding Boxes.png", bounding_box_image)
        bounding_boxes = "Pictures/Bounding Boxes.png"
        return bounding_boxes

    def DisplayImage(self):
        im_path = self.ChangeImage()
        dpi = 80
        image_data = plt.imread(im_path)
        height, width = image_data.shape[:2]
        FigureSize = width / float(dpi), height / float(dpi)
        Figure = plt.figure(figsize=FigureSize)
        ax = Figure.add_axes([0, 0, 1, 1])
        ax.axis('off')
        ax.imshow(image_data, cmap='gray')
        plt.show()


if __name__ == "__main__":
    inverted_image=InvertedImage()
    inverted_image.DisplayImage()
    gray_scale=GrayScale()
    gray_scale.DisplayImage()
    black_and_white=BlackAndWhite()
    black_and_white.DisplayImage()
    bounding_boxes=Bounding_Boxes()
    bounding_boxes.DisplayImage()