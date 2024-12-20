import json
import logging
import pandas as pd 
import re 
import requests

def ensure_first_letter_capitalized(text):  
    if not text:  
        return text  # Return the original text if it's empty  
    return text[0].upper() + text[1:]  

def cleaning_label(label):
    pattern = r"[&\-\(\)\\/]"  
    # Replace them with a space  
    label = re.sub(pattern, ' ', label)

    return ensure_first_letter_capitalized(label)

def get_uri(namespace: str, concept:dict, level: int) -> str:
    slug = concept[f"Slug Catégorie L{level}"].lower().replace(" ", "_")
    uri = namespace + slug

    return uri

def rename_columns(excel: pd.DataFrame, excel_info: json, level: int) -> None:

    if excel_info["Information by level"]["altLabel"] == "":
        excel.rename(columns={excel_info["Information by level"]["Concept"] + str(level): f"Slug Catégorie L{level}", 
                            excel_info["Information by level"]["prefLabel"] + str(level): f"Titre Catégorie L{level}", 
                            excel_info["Information by level"]["Definition"] + str(level): f"Definition Catégorie L{level}"}, inplace=True)
    else:
        excel.rename(columns={excel_info["Information by level"]["Concept"] + str(level): f"Slug Catégorie L{level}", 
                            excel_info["Information by level"]["prefLabel"] + str(level): f"Titre Catégorie L{level}", 
                            excel_info["Information by level"]["Definition"] + str(level): f"Definition Catégorie L{level}",
                            excel_info["Information by level"]["altLabel"] + str(level): f"Autre Titre Catégorie L{level}"}, inplace=True)
        
def shacl_validation(turtle_data: str):
    # Prepare the API request payload  
    payload = {  
        "contentToValidate": turtle_data,  
        "contentSyntax": "text/turtle",  
        "validationType": "v1.0.0"  
    }  

    # Send the POST request  
    response = requests.post("http://localhost:8080/shacl/d4wta-ap/api/validate", json=payload)  

    # Check the response  
    if response.status_code == 200:  
        print("Validation successful")
        
        if response.json().get("sh:conforms"):
            print("No errors in the taxonomy")
            #print("No error in the taxonomy")
        else: 
            print("Errors detected:\n" + response.text) 
            #print("Errors detected:\n" + response.text)
    else:  
        print("Validation failed:" + response.status_code + response.text)