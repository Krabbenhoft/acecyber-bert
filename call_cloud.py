import os
import requests

def query(payload):
    API_URL = "https://router.huggingface.co/hf-inference/models/OpenMed/OpenMed-PII-SuperClinical-Large-434M-v1"
    headers = {
        "Authorization": f"Bearer {open("hf_key.txt", "r").read().strip("!@#$%^&*()_+ ,")}",
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

output = query({
    "inputs": "My name is Sarah Jessica Parker but you can call me Jessica",
})

print(output)