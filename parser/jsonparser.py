"""
TEXT TO JSON this is a test
"""
from text_to_json.txt_to_json import *

def json_parser(file_list, location):
    """
    JSON PARSER
    """

    try :
        print(f"START JSON SERIALISATION FOR PREVIEW | location : {location}")
        data_file = {}

        peer_review_json = peer_review(file_list)
        medical_records_json = medical_records(file_list)
        nmr_data = nmr_parser(file_list)
        prior_auth = prior_auth_req(file_list)


        data_file["peer_review"] = peer_review_json
        data_file["medical_records"] = medical_records_json
        data_file['nmr_pre_refferal'] = nmr_data
        data_file["prior_auth_request"] = prior_auth
        return data_file

    except Exception as error:
        return error





