"""
JSON PARSER
"""

import time

def peer_review(file_list):
    print("RUNNING PEER REVIEWW | ON FILE LIST")
    start_time = time.time()
    temp_index = 0
    while temp_index < len(file_list) and file_list[temp_index] != "Medical Records:":
        temp_index += 1

    preview = file_list[0 : temp_index]
    request_form = {}

    try:
        for i in preview:
            data = i.split(":")
            if "Date Submitted" in data[0]:
                if data[1].split(" ")[0] == "":
                    request_form["date_submitted"] = data[1].split(" ")[1]
                    request_form["due_date"] = data[2].split(" ")[1]
                else:
                    request_form["date_submitted"] = data[1].split(" ")[0]
                    request_form["due_date"] = data[2].split(" ")[0]

            if "Client Contact" in data[0]:
                client_contact = ""
                for i in data[1].split(" "):
                    if i == "Peer" or i == "Vendor":
                        continue
                    client_contact += i + " "

                request_form["client_contact"] = client_contact

            if "Email" in data[0]:
                request_form["email"] = data[-1]

            if "Claimant" in data[0]:
                claiment = ""
                for i in data[1].split(" "):
                    if i == "Employer":
                        continue
                    else:
                        claiment += i+" "

                request_form["claiment"] = claiment
                request_form["employer"] = data[-1]

            if "Claim #" in data[0]:
                claim = ""
                for i in data[1].split(" "):
                    if i == "Carrier":
                        continue
                    else:
                        claim += i + " "

                request_form["claim no."] = claim

            if "DOI" in data[0]:
                doi = ""
                for i in data[1].split(" "):
                    if i == "Claims" or i == "Examiner":
                        continue
                    else:
                        doi += i
                doidata = doi
                request_form["DOI"] = doidata
                examiner = data[-1]
                request_form["examiner"] = examiner

            if "DOB" in data[0]:
                dob_data = ""
                for i in data[1].split(" "):
                    if i == "Review" or i == "#":
                        continue
                    else:
                        dob_data += i + " "
                request_form["DOB"] = dob_data
                review = data[-1]
                request_form["review no."] = review

            if "Provider" in data[0]:
                providerdata = ""
                try :
                    for i in data[1].replace("  ", "").split(' '):
                        providerdata += i + " "
                except:
                    providerdata = ""
                request_form["provider"] = providerdata

            if "phone" in data[0].lower():
                phonedata = ""
                for i in data[1].split(" "):
                    if i == "Jurisdiction":
                        continue
                    else:
                        phonedata += i + " "
                for i in phonedata:
                    if i not in str([1,2,3,4,5,6,7,8,9,0]) or i not in ["\')\'"]:
                        continue
                    else:
                        request_form["phone no."] = phonedata
                        request_form["jurisdiction"] = data[-1]

            if "Specialty" in data[0]:
                speciality_data = ""
                for i in data[1].split(" "):
                    if i == "Review" or i == "Level":
                        continue
                    else:
                        speciality_data += i + " "
                request_form["speciality"] = speciality_data
                request_form["review_level"] = data[-1]

            if "Review Type" in data[0]:
                request_form["review_type"] = data[1]

    except Exception as error:
        request_form = {}

    finally:
        end_time = time.time()
        print(f"SUCCESSFULLY RAN PEER REVIEW | TIMING : {round(end_time - start_time, 2)}")
        return request_form

def medical_records(file_list):
    """
    MEDICAL RECORDS
    """
    print("RUNNING MEDICAL RECORDS | ON FILE LIST")

    start_time = time.time()
    medical_records = {}

    try:
        """ TREATMENT REQUESTED """
        for i in range(len(file_list)):
            try:
                if "Requested" in file_list[i]:
                    start_index = i
                    break
            except:
                pass
        end_index = start_index
        while end_index < len(file_list) and "Criteria" not in file_list[end_index]:
            end_index += 1
        treatment = file_list[start_index : end_index]

        treatment_data = ''
        try:
            for i in treatment:
                treatment_data += i
        except:
            treatment_data = ""
        medical_records["treatment_requested"] = treatment_data


        """ DIAGNOSIS """
        # for i in range(len(file_list)):
        #     try:
        #         if "Diagnosis" in file_list[i]:
        #             start_index = i
        #             break
        #     except:
        #         pass
        # end_index = start_index
        # while end_index < len(file_list) and  file_list[end_index] != "Conclusion:":
        #     end_index += 1
        # diagnosis = file_list[start_index : end_index]

        # diagnosis_data = ''
        # for i in diagnosis:
        #     try:
        #         if "Diagnosis" in i:
        #             pass
        #         else:
        #             diagnosis_data += i
        #     except:
        #         diagnosis_data = ''

        # medical_records["diagnosis"] = diagnosis_data

        """ CONCLUSION """

        for i in range(len(file_list)):
            try:
                if "Conclusion:" in file_list[i]:
                    start_index = i
            except:
                pass
        end_index = start_index
        while end_index < len(file_list) and "Treatment Request Details:" not in  file_list[end_index]:
            end_index += 1

        conclusion = file_list[start_index : end_index]
        conclusion_data = ''
        try:
            for i in conclusion:
                if "Conclusion" in i:
                    pass
                else:
                    conclusion_data += i
        except:
            conclusion_data = ""
        medical_records["conclusion"] = conclusion_data

    except Exception as error:
        medical_records = {}

    finally:
        end_time = time.time()
        print(f"SUCCESSFULLY RAN MEDICAL RECORDS | TIMING : {round(end_time - start_time, 2)}")
        return medical_records

def nmr_parser(file_list):

    print("RUNNING NMR SUMMARY | FILE LIST")
    start_time = time.time()

    try:
        for i in range(len(file_list)):
            if "NMR" in file_list[i]:
                start_index = i

        end_index = start_index
        while end_index < len(file_list) and "Attachments" not in file_list[end_index]:
            end_index += 1

        nmr_data = file_list[start_index : end_index]

        nmr = {}

        for i in range(len(nmr_data)):
            data = nmr_data
            if 'Client Due Date' in data[i]:
                nmr["client_due_date"] = data[i + 35]

            if 'Referrer' in data[i] and "Referrer Phone" not in data[i] and "Referrer Email" not in data[i]:
                nmr["referrer"] = data[i+35]

            if 'Referrer Phone' in data[i]:
                nmr["referrer_phone"] = data[i+35]

            if "Referrer Email" in data[i] and "Referrer Phone" not in data[i]:
                nmr['referrer_email'] =data[i+35]

            if 'Client' in data[i] and "Client Due Date" not in data[i] and len(data) > 3:
                    nmr["client_data"] =  data[i+35]

            if "Turnaround" in data[i]:
                nmr["turn_around_type"] = data[i+35]

            if "Date Created" in data[i]:
                nmr["date_created"] = data[i+35]

            if "Referral Type" in data[i]:
                nmr['referral_type'] = data[i+35]

            if "Line of" in data[i]:
                nmr["line_of_business"] = data[i+35]

            if "Review Type" in data[i]:
                nmr["review_type"] = data[i+35]

            if "Review Level" in data[i]:
                nmr["review_level"] = data[i+35]

            if "Review Timing" in data[i]:
                nmr["review_timing"] = data[i+35]

            if "State of Jurisdiction" in data[i]:
                nmr["state_of_jurisdiction"] = data[i+35]

            if "Last Name" in data[i]:
                nmr["lastname"] = data[i+35]

            if "First Name" in data[i]:
                nmr["firstname"] = data[i+35]

            if "Claim Number" in data[i]:
                nmr["claim_number"] = data[i+35]

            if "Gender" in data[i]:
                nmr["gender"] = data[i+35]

            if "Date of Birth" in data[i]:
                nmr["DOB"] = data[i+35]

            if "Date of Disability" in data[i]:
                nmr["date_of_disability/injury"] = data[i+35]

            if "Diagnosis" in data[i]:
                diagnosis_data = ''
                try:
                    for i in data:
                        i = i.replace(",","")
                        i = i.replace(";", "")
                        if "Diagnosis" in i:
                            d = i.split("(es)")
                            diagnosis_data += d[-1]
                        else:
                            diagnosis_data += " " + i
                except:
                    nmr["diagnosis"] = data[i+35]

        """ CASE SUMMARY """
        for i in range(len(file_list)):
            if "CaseSummaryGuideline" in file_list[i]:
                start_index = i
                break
        end_index = start_index
        while end_index < len(file_list) and "Location" not in file_list[end_index]:
            end_index += 1
        summary = file_list[start_index : end_index]

        summary_data = ''
        try:
            for i in summary:
                if "CaseSummaryGuideline" in i:
                    split_data = i.split(" ")
                    main_data = ""
                    for i in range(len(split_data)):
                        if "CaseSummaryGuideline" in split_data[i]:
                            continue
                        if "Variance" in split_data[i]:
                            continue
                        else:
                            main_data += split_data[i] + " "
                            summary_data += main_data
                else:
                    summary_data += i
        except:
            summary_data = ""
        nmr["case_summary"] = summary_data

    except Exception as error:
        nmr = {}

    finally:
        end_time = time.time()
        print(f"SUCCESSFULLY RAN NMR SUMMARY | TIMING : {round(end_time - start_time, 2)}")
        return nmr

def prior_auth_req(file_list):
    print("RUNNING PRIOR AUTH REVIEWW | ON FILE LIST")
    start_time = time.time()
    try:
        """ Patient data """
        for i in range(len(file_list)):
            if "Patient Name" in file_list[i]:
                start_index = i
                break
        end_index = start_index
        while end_index < len(file_list) and "Employer Name " not in  file_list[end_index]:
            end_index += 1

        preview_patient_data = file_list[start_index : end_index]

        prior_auth_form = {}
        claim_information = {}

        try:
            for i in range(len(preview_patient_data)):
                data = preview_patient_data[i].replace("_", "").split(" ")
                if "Patient" in data[0]:
                    patient_name = ""
                    leave = ["Patient","Name"]
                    for i in data:
                        if i in leave:
                            pass
                        else:
                            patient_name += i + " "

                    claim_information["patient_name"] = data[-2] + " " + data[-1]

                elif "Address" in data[0]:
                    address = ""
                    curr = 0
                    for i in range(len(data)):
                        leave = ["Address"]
                        if i in leave:
                            pass
                        else:
                            address += data[i]+ " "

                elif "SSN" in data[0]:
                    for i in data:
                        while "DOB" not in i:
                            ssn = ""
                            ssn += i + " "
                    for i in data:
                        dob = ""
                        if "DOB" not in i:
                            pass
                        elif "Gender" in i:
                            break
                        else:
                            dob += i + " "

                    claim_information["DOB"] = dob



                else:
                    for i in data:
                        address += i + " "

                    claim_information["address"] = address

        except Exception as error:
            claim_information = {}

        """ Employer """
        start_index =  end_index
        while end_index < len(file_list) and "Insurer Name" not in file_list[end_index]:
            end_index += 1

        employer_data = file_list[start_index : end_index]
        employer = {}
        try:
            for i in range(len(employer_data)):

                if "Employer" in employer_data[i]:
                    data = employer_data[i].split("=")
                    name = ""
                    for i in range(len(data)):
                        if i == 0:
                            continue
                        name += data[i] + " "
                    employer["name"] = name

                if "Address" in employer_data[i]:
                    data = employer_data[i].split(" ")
                    address = ""
                    for j in range(len(data)):
                        if j == 0:
                            continue
                        address += data[j] + " "

                else:
                    data = employer_data[i].split(" ")
                    for i in data:
                        address += i + " "
                    employer["address"] = address

        except:
            employer = {}

        """ Insurer Name """
        start_index =  end_index
        while end_index < len(file_list) and "Claim Admin" not in file_list[end_index]:
            end_index += 1

        insurer_data = file_list[start_index : end_index]
        insurer = {}
        try:
            for i in range(len(insurer_data)):
                if "Insurer Name" in insurer_data[i]:
                    leave = ["__", "_"]
                    data = insurer_data[i].split(" ")
                    insurer_name = ""
                    for i in range(len(data)):
                        if i == 0:
                            continue
                        if data[i] == "Insurer":
                            break
                        else:
                            if data[i] in leave:
                                pass
                            else:
                                insurer_name += data[i] + " "
                    insurer["insurer_name"] = insurer_name
                    insurer["insurer_id"] = data[-1]

        except:
            insurer = {}


    except:
        prior_auth_form = {}

    finally:
        prior_auth_form["claim_information"] = claim_information
        prior_auth_form["employer_data"] = employer
        prior_auth_form["insurer"] = insurer
        end_time = time.time()
        print(f"SUCCESSFULLY RAN PEER REVIEW | TIMING : {round(end_time - start_time, 2)}")
        return prior_auth_form
