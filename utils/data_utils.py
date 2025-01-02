import json
import logging
import pandas as pd 
import re 
import requests
from tqdm import tqdm

CHANGED_LABELS = {}

def ensure_first_letter_capitalized(text):
    """  
    Ensures that the first letter of a given string is capitalized.  
  
    This function checks if the input string is empty and returns it unchanged if so. Otherwise, it capitalizes the first letter while leaving the rest of the string unchanged.  
  
    Parameters:  
    -----------  
    text : str  
        The input string to be processed.  
  
    Returns:  
    --------  
    str  
        The input string with the first letter capitalized, if applicable.  
    """    
    if not text:  
        return text  # Return the original text if it's empty  
    return text[0].upper() + text[1:]  

def cleaning_label(label: str, uri: str, rules: list):
    """  
    Cleans a label by replacing specific special characters with spaces and capitalizing the first letter.  
  
    This function uses a regular expression to replace a set of special characters in the input label with spaces. It then ensures the first letter of the resulting string is capitalized.  
  
    Parameters:  
    -----------  
    label : str  
        The input label string to be cleaned.
    uri : str  
        The uri of input label string to be cleaned. 
    rules: list
        Series of changes to make to the labels of the taxonomy elements.

    Returns:  
    --------  
    str  
        The cleaned label with special characters replaced and the first letter capitalized.  
    """ 
    for rule in rules:    
        for rule_label in rule:
            # Escape each character for regex use  
            _from = rule[rule_label]["from"]
            escaped_chars = [re.escape(char) for char in _from]  
            
            # Join them into a string with no separator  
            char_class = ''.join(escaped_chars)  
            
            # Build the regex pattern with negation  
            pattern = f'[{char_class}]'
            regex = re.compile(pattern)

            _to = rule[rule_label]["to"]
            _exceptions = rule[rule_label]["exceptions"]
            if regex.findall(label):
                if(label in _exceptions):
                    logging.info(f"Label excluded: \"{label}\"")
                else:
                    CHANGED_LABELS[rule_label].append(label)
                    # Replace them with a space  
                    label = re.sub(pattern, _to, label)

    return ensure_first_letter_capitalized(label)

def get_uri(namespace: str, concept:dict, level: int) -> str:
    """  
    Constructs a URI for a concept within a specified namespace and level.  
  
    This function creates a URI by concatenating a namespace with a slug derived from the concept's name. The slug is generated by converting the concept's name to lowercase and replacing spaces with underscores.  
  
    Parameters:  
    -----------  
    namespace : str  
        The base namespace for constructing the URI.  
    concept : dict  
        A dictionary containing the concept's details, including its name.  
    level : int  
        The level of the concept in the taxonomy, used to access the appropriate field in the concept dictionary.  
  
    Returns:  
    --------  
    str  
        The constructed URI for the concept.  
    """  
    slug = concept[f"Slug Catégorie L{level}"].lower().replace(" ", "_")
    uri = namespace + slug

    return uri

def rename_columns(excel: pd.DataFrame, prefLabel: str, concept: str, definition: str, altLabel: str, level: int) -> None:
    """  
    Renames columns in a DataFrame based on taxonomy information for a specific level.  
  
    This function updates the column names of a DataFrame to standardized names using configuration details from a JSON structure. It ensures that the taxonomy data is accessible with consistent column names.  
  
    Parameters:  
    -----------  
    excel : pd.DataFrame  
        The DataFrame containing taxonomy data from an Excel file.  
    excel_info : json  
        A JSON object containing metadata and configuration details for renaming columns.  
    level : int  
        The level of taxonomy data to process, influencing which columns are renamed.  
  
    Returns:  
    --------  
    None  
    """
    if altLabel == "":
        excel.rename(columns={concept + str(level): f"Slug Catégorie L{level}", 
                            prefLabel + str(level): f"Titre Catégorie L{level}", 
                            definition + str(level): f"Definition Catégorie L{level}"}, inplace=True)
    else:
        excel.rename(columns={concept + str(level): f"Slug Catégorie L{level}", 
                            prefLabel + str(level): f"Titre Catégorie L{level}", 
                            definition + str(level): f"Definition Catégorie L{level}",
                            altLabel + str(level): f"Autre Titre Catégorie L{level}"}, inplace=True)
        
def shacl_validation(turtle_data: str, validation_server: str, output_format: str, validation_version: str):
    """  
    Validates RDF data in Turtle format using a SHACL API.  
  
    This function sends a POST request to a SHACL validation API with the RDF data. It checks the API response to determine if the RDF conforms to the SHACL shapes and prints validation results.  
  
    Parameters:  
    -----------  
    turtle_data : str  
        The RDF data in Turtle format to be validated. 
    validation_server : str  
        The API endpoint used for validating the resulting RDF file. 
    output_format : str  
        The format of the resulting rdf to be validated.
  
    Returns:  
    --------  
    None  
  
    Side Effects:  
    -------------  
    - Sends an HTTP POST request to a SHACL API.  
    - Prints validation results to the console, indicating success or failure and any errors detected.  
  
    Raises:  
    -------  
    Exception  
        If the HTTP request fails or the API returns an error response.  
    """  
    # Prepare the API request payload  
    payload = {  
        "contentToValidate": turtle_data,  
        "contentSyntax": f"{output_format}",  
        "validationType": f"{validation_version}"  
    }  


    # Send the POST request 
    for index in tqdm([1], desc="SHACL validation"): 
        response = requests.post(validation_server, json=payload)  

    # Check the response  
    if response.status_code == 200:  
        if response.json().get("sh:conforms"):
            print("Validation successful: No errors in the taxonomy")
            #print("No error in the taxonomy")
        else: 
            print("Validation failed: Errors detected:\n" + response.text) 
            #print("Errors detected:\n" + response.text)
    else:  
        print("Error with the API call to ITB validator:" + response.status_code + response.text)