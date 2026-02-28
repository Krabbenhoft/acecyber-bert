import requests
import os
from pathlib import Path

#list of label files
hundred_words = 100

#Function to call GLiNER
def query(input_to_scan):
    API_URL = "https://router.huggingface.co/hf-inference/models/OpenMed/OpenMed-PII-SuperClinical-Large-434M-v1"
    headers = {
        "Authorization": f"Bearer {open("hf_key.txt", "r").read().strip("!@#$%^&*()_+ ,")}",
    }
    payload = {
    "inputs": input_to_scan
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

#Break string into shorter bits
def get_substrings(single_string, word_count):
    word_list = single_string.split()
    ret_array = []
    current_string = ""
    reset_iter = 0
    for word in word_list:
        current_string += word + " "
        reset_iter += 1

        if reset_iter == word_count:
            ret_array.append(current_string)
            reset_iter = 0
            current_string = ""

    return ret_array

def put_redacted_to_file(base_string, detections_json_list, output_file):
    #Extremely basic way of verifying there were no detections
    if len(str(detections_json_list)) < 3:
        file_handle = Path('.')
        if os.path.exists(Path(output_file)):
            file_handle = open(output_file, 'a')
        else:
            file_handle = open(output_file, 'w')
        file_handle.write(base_string)
        file_handle.close()


input_files = [f.path for f in os.scandir("1firstdocs")]
for curr_file in input_files:

    #Get the current file
    curr_text = open(curr_file, "r").read()

    #Get substrings
    curr_substrings = get_substrings(curr_text, hundred_words)

    #Loop over all the chunks
    for curr_substring in curr_substrings:
        json_response = query(curr_substring)
        print(str(json_response))
        print(len(str(json_response)))
        print("/1firstcleaned/" + str(os.path.basename(Path(curr_file))))
        put_redacted_to_file(curr_substring, json_response, "1firstcleaned/" + str(os.path.basename(Path(curr_file))))