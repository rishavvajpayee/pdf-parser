import json
import os

from datetime import date

# today = date.today()
# print("Today's date:", str(today))
# today = str(today).split("-")[0]
# print(today)

cwd = os.getcwd()

def get_file_list(location):
    file_list = []

    print(f"START READING FILE AND STORE IN LIST FROM DOWNLOAD LOCATION : {location}")
    with open(location, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                file_list.append(line)

    return file_list

def convert_to_json(return_json, file_name):
    try :
        path = f'/home/ctp/Desktop/pdf-parser/parser/json/{file_name}.json'
        with open(path, 'w', encoding = 'utf-8') as  file:
            file.write(json.dumps(return_json))
        return f"{file_name} converted to Json | Message : Saved at : {path}"

    except Exception as error:
        return f"Error in file | {file_name} | Message : {error}"

def json_to_text(file_name):
    try:
        path = f'{cwd}/parser/json/{file_name}.json'
        with open(path, 'r', encoding= "utf-8")as file:
            data = json.load(file)

        dob = data["peer_review"]["DOB"]

        dob = dob.split("/")[-1]
        today = date.today()
        today = str(today).split("-")[0]

        age = int(today) - int(dob)

        text = ""

        text += file_name + "\n \n"
        text += f"{age} years old Patient :" + data["peer_review"]["client_contact"] + ",email-id :" + data["peer_review"]["email"] + " "
        text += ",DOB :" + data["peer_review"]["DOB"] + "\n \n"
        text += "Treatment requested : " + data["medical_records"]["treatment_requested"] + "\n \n"

        try:
            if len(data["medical_records"]["diagnosis"]) < 1000:
                text += data["medical_records"]["diagnosis"]
            else:
                text += "Diagnosis : None"
        except Exception as error:
            text += "Diagnosis : None"

        with open(f"{cwd}/parser/finaltext/{file_name}-final.txt", "w") as text_file:
            text_file.write(text)

    except Exception as error:
        print(error)