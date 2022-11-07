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

            # if 'Employer' in data[0]:
            #     request_form["employer"] = data[1]

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
                doidata = data[1].replace("  ","").split(" ")
                request_form["DOI"] = doidata[0]
                examiner = data[2]
                request_form["examiner"] = examiner

            if "DOB" in data[0]:
                dob_data = data[1].split(" ")
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
                for i in phonedata:
                    if i not in str([1,2,3,4,5,6,7,8,9,0]) or i not in ["\')\'"]:
                        continue
                    else:
                        request_form["phone no."] = phonedata[1] + " " + phonedata[2]
                        request_form["jurisdiction"] = data[2]

            if "Special" in data[0]:
                speciality_data = data[1].split(" ")
                request_form["speciality"] = speciality_data[1]
                request_form["level"] = data[2]

            if "Review" in data[0]:
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
        while end_index < len(file_list) and "SSN" not in file_list[end_index]:
            end_index += 1

        nmr_data = file_list[start_index : end_index]

        nmr = {}

        for i in nmr_data:
            data = i.split(" ")
            if 'ClientDueDate' in data[0] and len(data) <= 3:
                nmr["client_due_date"] = data[1 :]

            if 'Referrer' in data[0]:
                nmr["referrer"] = data[-1]

            if 'ReferrerPhone' in data[0]:
                nmr["referrer_phone"] = data[-1]

            if "ReferrerEmail" in data[0]:
                nmr['referrer_email'] = data[-1]

            if 'Client' in data[0] and "ClientDueData" not in data[0] and len(data) > 3:
                client_data = ''
                for i in data[1:]:
                    client_data += i
                print(client_data)
                nmr["client_data"] =  client_data

            if "Turnaround" in data[0]:
                nmr["turn_around_type"] = data[-1]

            if "DateCreated" in data[0]:
                nmr["date_created"] = data[1:]

            if "ReferralType" in data[0]:
                nmr['referral_type'] = data[-1]

            if "Lineof" in data[0]:
                nmr["line_of_business"] = data[-1]

            if "ReviewType" in data[0]:
                nmr["review_type"] = data[-1]

            if "ReviewLevel" in data[0]:
                nmr["review_level"] = data[-1]

            if "ReviewTiming" in data[0]:
                nmr["review_timing"] = data[-1]

            if "StateofJurisdiction" in data[0]:
                nmr["state_of_jurisdiction"] = data[-1]

            if "LastName" in data[0]:
                nmr["lastname"] = data[-1]

            if "Firstname" in data[0]:
                nmr["firstname"] = data[-1]

            if "ClaimNumber" in data[0]:
                nmr["claim_number"] = data[-1]

            if "Gender" in data[0]:
                nmr["gender"] = data[-1]

            if "DateofBirth" in data[0]:
                nmr["DOB"] = data[-1]

            if "DateofDisability" in data[0]:
                nmr["date_of_disability/injury"] = data[-1]

            if "Diagnosis" in data[0]:
                diagnosis_data = ''
                for i in data:
                    i = i.replace(",","")
                    i = i.replace(";", "")
                    if "Diagnosis" in i:
                        d = i.split("(es)")
                        diagnosis_data += d[-1]
                    else:
                        diagnosis_data += " " + i
                nmr["diagnosis"] = diagnosis_data

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
        nmr["case_summary"] = summary_data

    except Exception as error:
        nmr = {}

    finally:
        end_time = time.time()
        print(f"SUCCESSFULLY RAN NMR SUMMARY | TIMING : {round(end_time - start_time, 2)}")
        return nmr

def prior_auth_req(file_list):
    print("RUNNING PEER REVIEWW | ON FILE LIST")
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
            for i in preview_patient_data:
                data = i.split(" ")
                if "Patient" in data[0]:
                    claim_information["patient_name"] = data[-2] + " " + data[-1]

                if "Address" in data[0]:
                    address = ""
                    for i in range(len(data)):
                        address += data[i]+ " "
                    claim_information["address"] = address

        except:
            claim_information = {}

        """ Employer """
        start_index =  end_index
        while end_index < len(file_list) and "Insurer" not in file_list[end_index]:
            end_index += 1

        employer_data = file_list[start_index : end_index]
        employer = {}
        try:
            for i in range(len(employer_data)):
                data = employer_data[i].split(" ")

                if "Employer" in data[0]:
                    name = ""
                    for i in range(len(data)):
                        if i == 0 or i == 1:
                            continue
                        name += data[i] + " "
                    employer["name"] = name

                if "Address" in data[0]:
                    address = ""
                    for i in range(len(data)):
                        if i == 0:
                            continue
                        address += data[i]+ " "
                    employer["address"] = address

                if  "Type" in data[0]:
                    type = ''
                    for i in range(len(data)):
                        if i == 0:
                            continue
                        type += data[i] + " "
                    employer["type"] = type

                if "Insurer" in data[0]:
                    insurer = ""
                    for i in range(len(data)):
                        insurer += data[i] + " "
                    employer["insurer"] = insurer

        except:
            employer = {}

        prior_auth_form["claim_information"] = claim_information
        prior_auth_form["employer_data"] = employer

    except:
        prior_auth_form = {}

    finally:
        end_time = time.time()
        print(f"SUCCESSFULLY RAN PEER REVIEW | TIMING : {round(end_time - start_time, 2)}")
        return prior_auth_form
