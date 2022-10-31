import json

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