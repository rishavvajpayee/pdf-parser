"""
PDF TO TEXT
""" 

import os
import time
import shutil
import pytesseract
from utils.utils import *
from pdf2image import convert_from_path
from jsonparser import json_parser

class PdfParser():
    @classmethod
    def on_get(cls, req, resp):
        resp.text = "Api running successfully"
        return resp

    @classmethod
    def on_post(cls, req, resp):
        # Retrieve file extension
        try:
            file = req.get_media()
            for part in file:
                if part.content_type == 'application/json':
                    resp.media = part.get_media()
                elif part.name == 'file':
                    name = part.secure_filename
                    name = name.split(".")[0]
                    path = f"{cwd}/parser/NMR_PDF/{name}.pdf"
                    print(name)
                    with open(path, 'wb') as outfile:
                        part.stream.pipe(outfile)

            final_json = main(path)
            resp.text = json.dumps(final_json)
            return resp

        except Exception as error:
            print(error)

# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
cwd = os.getcwd()
def main(read_path):
    """
    Convert PDF to Text
    """
    t1 = time.time()
    try:
        file_name = read_path.split("/")[-1].split(".")[0]
        pages = convert_from_path(read_path, 350)

        i = 1
        directory = f"{file_name}"

        # Parent Directory path
        parent_dir = cwd
        directorypath = os.path.join(parent_dir, directory)
        try:
            os.mkdir(directorypath)
        except:
            try:
                os.rmdir(directorypath)
            except OSError as error:
                print(error)
                shutil.rmtree(directorypath)

            os.mkdir(directorypath)

        for page in pages:
            image_name = "Page_" + str(i) + ".jpg"

            page.save(f"{directorypath}/{image_name}", "JPEG")
            print(f"{image_name} SAVED.")
            i = i+1

        total_pages = i

        try:
            os.mkdir(f'{cwd}/parser/tesseract_output/{file_name}.txt')
        except OSError as os_error:
            print(os_error)
            try:
                shutil.rmtree(f'{cwd}/parser/tesseract_output/{file_name}.txt')
            except:
                os.remove(f'{cwd}/parser/tesseract_output/{file_name}.txt')

        for i in range(total_pages):
            if i == 0:
                continue
            path = f'{cwd}/{file_name}/Page_{i}.jpg'
            print(f"code running for path = {path}")
            text = pytesseract.image_to_string(path)

            with open(f'{cwd}/parser/tesseract_output/{file_name}.txt', 'a',encoding='utf-8') as file:
                file.write(text)

        location = f'{cwd}/parser/tesseract_output/{file_name}.txt'

        file_list = get_file_list(location)
        return_json = json_parser(file_list, location)
        return_statement = "ho gaya"
        return return_json
        # return_statement = convert_to_json(return_json, file_name)

        # json_to_text(file_name)

    except Exception as error:
        return_statement = error
        print(F"ERROR IN MAIN FUNCTION WITH FILE : {file_name} | Message : {error}")

    finally:
        print(return_statement)
        t2 = time.time()
        print(f"RAN MAIN FUNCTION | TIMINGS : {round(t2-t1,5)}")


# if __name__ == "__main__":
    # path = f'{cwd}/parser/NMR_PDF/746485-1.pdf' # add the pdf files to NMR files
    # main(path)