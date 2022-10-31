"""
PDF TO TEXT
"""

import PyPDF2
from jsonparser import json_parser
from utils.utils import *

def main(read_path):
    """
    Convert PDF to Text
    """
    try:
        file_name = read_path.split("/")[-1].split(".")[0]

        with open(read_path , "rb") as pdf_file:
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            number_of_pages = read_pdf.getNumPages()

            page_content = ''

            for i in range(number_of_pages):
                page = read_pdf.pages[i]
                page_content += "\n \n" + page.extractText()

        data = page_content.split(".")

        location = f'/home/ctp/Desktop/pdf-parser/parser/txt/{file_name}.txt'
        newdata = ''
        try:
            with open(location, 'w', encoding='utf-8') as file:
                        file.write(newdata)

        except:
            print(f"NO FILE FOUND WITH FILE NAME : {file_name}")

        for line in data:
            line = line.strip()
            if line:
                with open(location, 'a', encoding='utf-8') as file:
                    file.write(line)

        file_list = get_file_list(location)
        return_json = json_parser(file_list, location)
        return_statement = convert_to_json(return_json, file_name)

        print(return_statement)

    except Exception as error:
        print(F"Error in the Main Function with file {file_name} | Message : {error}")

if __name__ == "__main__":
    path = '/home/ctp/Desktop/pdf-parser/parser/NMR_PDF/746485-1.pdf'
    main(path)