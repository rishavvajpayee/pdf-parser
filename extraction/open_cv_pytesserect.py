from pdf2image import convert_from_path
import os

cwd = os.getcwd()
print(cwd)

pdfs = f'{cwd}/NMR_PDF/747110-1.pdf'
pages = convert_from_path(pdfs, 350)

i = 1
for page in pages:
    image_name = "Page_"+str(i)+".jpg"
    page.save(image_name, "JPEG")
    i = i+1

import cv2
from PIL import Image
from matplotlib import pyplot as plt

def mark_region(image_path):

    im = cv2.imread(image_path)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)

        if y >= 600 and x <= 1000:
            if area > 10000:
                image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
                line_items_coordinates.append([(x,y), (2200, y+h)])

        if y >= 2400 and x<= 2000:
            image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
            line_items_coordinates.append([(x,y), (2200, y+h)])

    plt.imshow(image)
    plt.show
    return {'image': image, 'data': line_items_coordinates}

image_path = f'{cwd}/Page_5.jpg'
output = mark_region(image_path)
line_items_coordinates = output['data']
print(line_items_coordinates)
print("This was line item", len(line_items_coordinates))

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# load the original image
image = cv2.imread(image_path)

# get co-ordinates to crop the image
c = line_items_coordinates[16]

# cropping image img = image[y0:y1, x0:x1]
img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]

plt.figure(figsize=(10,10))
plt.imshow(img)

# convert the image to black and white for better OCR
ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)

# pytesseract image to string to get results
text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))
print(text)
