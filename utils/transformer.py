import json
import logging
import pandas as pd
from rdflib import Graph
from tqdm import tqdm
from utils.creating_triples import add_concept, add_conceptScheme, add_topConcept, ENGLISH_LABELS
from utils.data_utils import rename_columns, shacl_validation, CHANGED_LABELS

def adding_triples(taxo_excel: pd, taxo_graph: Graph, level: int, highest_level: str, prefLabel: str, D4W_NAMESPACE: str, rules: list, default_language: str, default_version: str, create_english_labels: str, creation_date: str, default_status: str, checkmispell: str) -> None:
    """
    Adds RDF triples to a given RDF graph based on taxonomy data from an Excel file.  
  
    This function processes a specific level of taxonomy data from an Excel DataFrame to generate RDF triples. Depending on the level, it adds different types of RDF triples to the RDF graph, such as concepts, top concepts, or concept schemes.  
  
    Parameters:  
    -----------  
    taxo_excel : pd.DataFrame  
        The DataFrame containing taxonomy data extracted from the Excel file.  
    taxo_graph : Graph  
        The RDFLib Graph object to which RDF triples are added.  
    level : int  
        The current level of taxonomy being processed. Determines the type of RDF triples added.  
    EXCEL_INFO : dict  
        A dictionary containing metadata and configuration information about the Excel file, including the highest and lowest taxonomy levels.  
    D4W_NAMESPACE : str  
        The namespace URI used for RDF triples, ensuring they are correctly scoped within the RDF graph.
    rules: list
        Series of changes to make to the labels of the taxonomy elements.
  
    Returns:  
    --------  
    None

    """
    unique_concepts = taxo_excel.drop_duplicates(subset=f"{prefLabel}{level}")
    # Loop over concepts by level
    for index in tqdm(unique_concepts.index, desc=f"Processing Level {level}", colour="green"):
        if level > int(highest_level) + 1: 
            add_concept(taxo_graph, D4W_NAMESPACE, unique_concepts.loc[index], level, rules, default_language, default_version, create_english_labels, default_status, checkmispell)
        elif level == int(highest_level) + 1: 
            add_topConcept(taxo_graph, D4W_NAMESPACE, unique_concepts.loc[index], level, rules, default_language, default_version, create_english_labels, default_status, checkmispell)
        else: 
            add_conceptScheme(taxo_graph, D4W_NAMESPACE, unique_concepts.loc[index], level, rules, default_language, default_version, create_english_labels, creation_date)


def excel_to_rdf(config: dict) -> None:
    """
    Converts an Excel file containing taxonomy data to an RDF file and validates the RDF using a SHACL API.  
  
    This function reads an Excel file specified by the user, processes its contents to generate an RDF graph, and then serializes the graph to a Turtle file format. After serialization, the RDF content is validated against a SHACL API.   
  
    Parameters:  
    -----------  
    excel : str  
        The file path to the Excel file containing taxonomy data.  
    namespace : str  
        The RDF namespace to be used for the generated RDF triples.  
    output_path : str  
        The file path where the resulting RDF file will be saved.
    output_format : str  
        The format of the resulting rdf.
    validation_server : str  
        The API endpoint used for validating the resulting RDF file.
    rules: list
        Series of changes to make to the labels of the taxonomy elements.

    Returns:  
    -------  
    None  

    """
    excel_path = config['input']['default_file'] 
    highest_level = config['input']['highest_level']
    lowest_level = config['input']['lowest_level']
    prefLabel = config['input']['information_by_level']['prefLabel']
    concept = config['input']['information_by_level']['Concept']
    definition = config['input']['information_by_level']['Definition'] 
    altLabel = config['input']['information_by_level']['altLabel']
    namespace = config['transformation']['namespace']
    create_english_labels = config['transformation']['create_english_labels']
    creation_date = config['transformation']['creation_date']
    output_path = config['output']['default_file']
    output_format = config['output']['default_format']
    validation_server = config['validation']['server']
    validation_version = config['validation']['version']
    rules = config['transformation']['rules']['changes']
    default_language = config['transformation']['default_language']
    default_version = config['transformation']['default_version']
    default_status = config['transformation']['default_status']
    checkmispell = config['transformation']['check_mispell']
    # Defining static variables
    EXCEL_PATH = excel_path 
    
    D4W_NAMESPACE = namespace
    EUROVOC_NS = "http://publications.europa.eu/ontology/euvoc#"
    STATUS_NS = "http://publications.europa.eu/resource/authority/concept-status/"

    for rule in rules:
        for rule_label in rule: 
            CHANGED_LABELS[rule_label] = []

    # Read taxonomy from excel
    taxo_excel = pd.read_excel(EXCEL_PATH)

    # Create rdf version of taxonomy
    taxo_graph = Graph()
    taxo_graph.bind("d4w", D4W_NAMESPACE)
    taxo_graph.bind("status", STATUS_NS)
    taxo_graph.bind("eurovoc", EUROVOC_NS)

    # Add triples to the rdf by level of the taxonomy
    for level in range(int(highest_level), int(lowest_level) + 1):

        try:     
            adding_triples(taxo_excel, taxo_graph, level, highest_level, prefLabel, D4W_NAMESPACE, rules, default_language, default_version, create_english_labels, creation_date, default_status, checkmispell) 
        except:
            rename_columns(taxo_excel, prefLabel, concept, definition, altLabel, level) # If the excel columns does not respect the naming convention rename those
            adding_triples(taxo_excel, taxo_graph, level, highest_level, prefLabel, D4W_NAMESPACE, rules, default_language, default_version, create_english_labels, creation_date, default_status, checkmispell)
    
    for rule in rules:
        for rule_label in rule: 
            logging.info(f"Labels changed based on rule {rule_label}: {CHANGED_LABELS[rule_label]}")

    logging.info(f"English labels {ENGLISH_LABELS}")
    #print(len(ENGLISH_LABELS))
    # Save rdf file
    taxo_graph.serialize(output_path, format=output_format)
    turtle_data = taxo_graph.serialize(format=output_format)  
    
    # Validate rdf file
    shacl_validation(turtle_data, validation_server, output_format, validation_version)