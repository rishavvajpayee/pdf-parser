"""
JSON PARSER
"""

def peer_review(file_list):
        temp_index = 0
        while temp_index < len(file_list) and file_list[temp_index] != "Medical Records:":
            temp_index += 1

        preview = file_list[0 : temp_index]
        request_form = {}

        for i in preview:
            data = i.split(":")
            if 'Employer' in data[0]:
                request_form["employer"] = data[1]

            if "Claimant" in data[0]:
                request_form["claiment"] = data[1]

            if "Claim #" in data[0]:
                data = data[1].replace("  ","").split(" ")
                request_form["claim no."] = data[0]

            if "DOI" in data[0]:
                doidata = data[1].replace("  ","").split(" ")
                request_form["DOI"] = doidata[0]
                examiner = data[2]
                request_form["examiner"] = examiner

            if "DOB" in data[0]:
                dob_data = data[1].replace("  ","").split(" ")
                request_form["DOB"] = dob_data[0]
                review = data[2]
                request_form["review no."] = review

            if "Provider" in data[0]:
                providerdata = data[1].replace("  ", "").split(',')
                request_form["provider"] = providerdata[0]
                request = data[2]
                request_form["no. of requests"] = request

            if "phone" in data[0].lower():
                phonedata = data[1].split(" ")
                request_form["phone no."] = phonedata[1] + " " + phonedata[2]
                request_form["jurisdiction"] = data[2]

            if "Special" in data[0]:
                speciality_data = data[1].split(" ")
                request_form["speciality"] = speciality_data[1]
                request_form["level"] = data[2]

            if "Review" in data[0]:
                request_form["review_type"] = data[1]

        return request_form

def medical_records(file_list):
    """
    MEDICAL RECORDS
    """
    medical_records = {}

    """ TREATMENT REQUESTED """
    for i in range(len(file_list)):
        if "Requested" in file_list[i]:
            start_index = i
            break
    end_index = start_index
    while end_index < len(file_list) and "Diagnosis" not in file_list[end_index]:
        end_index += 1
    treatment = file_list[start_index : end_index]

    treatment_data = ''
    for i in treatment:
        treatment_data += i
    medical_records["treatment_requested"] = treatment_data


    """ DIAGNOSIS """
    for i in range(len(file_list)):
        if "Diagnosis" in file_list[i]:
            start_index = i
            print(start_index)
            break
    end_index = start_index
    while end_index < len(file_list) and  file_list[end_index] != "Conclusion:":
        end_index += 1
    diagnosis = file_list[start_index : end_index]

    diagnosis_data = ''
    for i in diagnosis:
        if "Diagnosis" in i:
            pass
        else:
            diagnosis_data += i
    medical_records["diagnosis"] = diagnosis_data


    """ CONCLUSION """
    for i in range(len(file_list)):
        if "Conclusion:" in file_list[i]:
            start_index = i
            print(start_index)
    end_index = start_index
    while end_index < len(file_list) and "Treatment Request Details:" not in  file_list[end_index]:
        end_index += 1

    conclusion = file_list[start_index : end_index]
    conclusion_data = ''
    for i in conclusion:
        if "Conclusion" in i:
            pass
        else:
            conclusion_data += i
    medical_records["conclusion"] = conclusion_data

    """ CLIENT INSTRUCTIONS """
    for i in range(len(file_list)):
        if "Client Instructions" in file_list[i]:
            start_index = i
            print(start_index)
    end_index = start_index
    while end_index < len(file_list) and  "Treatment Request Details:" not in  file_list[end_index]:
        end_index += 1

    instructions = file_list[start_index : end_index]
    instruction_data = ''
    for i in instructions:
        if "Client Instructions" in i:
            pass
        else:
            instruction_data += i
    medical_records["client_instructions"] = instruction_data

    return medical_records
