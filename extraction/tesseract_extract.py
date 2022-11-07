import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' # install tesseract and add the file path here.
import os

cwd = os.getcwd()

# def ocr_core(path):
for i in range(19):
    if i == 0:
        continue
    path = f'{cwd}/Page_{i}.jpg'

    print(f"code running for path = {path}")

    text = pytesseract.image_to_string(path)

    with open(f'{cwd}/tesseract_output/output.txt', 'a',encoding='utf-8') as file:
        file.write(text)

# path = 'test/image.jpeg' # path to where you want to save the jpeg

# if __name__ == "__main__":
#     ocr_core(path)