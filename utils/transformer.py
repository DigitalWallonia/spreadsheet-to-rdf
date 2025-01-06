import json
import logging
import pandas as pd
from rdflib import Graph
from tqdm import tqdm
from utils.creating_triples import add_concept, add_conceptScheme, add_topConcept, ENGLISH_LABELS
from utils.data_utils import shacl_validation, CHANGED_LABELS, find_duplicate_values, taxonomy_size_validation

def adding_triples(taxo_excel: pd, taxo_graph: Graph, level: int, highest_level: str, column_names: dict, D4W_NAMESPACE: str, rules: list, default_language: str, default_version: str, create_english_labels: str, creation_date: str, default_status: str, checkmispell: str) -> None:
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
    highest_level : str    
        The highest level in the taxonomy hierarchy that requires special processing.  
    column_names: dict    
        The column names prefix used in the Excel file.  
    D4W_NAMESPACE : str    
        The namespace URI used for RDF triples, ensuring they are correctly scoped within the RDF graph.  
    rules: list    
        Series of changes to make to the labels of the taxonomy elements.  
    default_language : str    
        The default language code for labeling the concepts.  
    default_version : str    
        The version of the concept being added.  
    create_english_labels : str    
        Flag indicating whether to create English labels for the concepts.  
    creation_date : str    
        The creation date of the concept scheme.  
    default_status : str    
        The default status URI for the concept.  
    checkmispell : str    
        Flag indicating whether to check for misspellings in the concept's definition.  

  
    Returns:  
    --------  
    None

    """
    unique_concepts = taxo_excel.drop_duplicates(subset=f"{column_names['Concept']}{level}")
    # Loop over concepts by level
    for index in tqdm(unique_concepts.index, desc=f"Processing Level {level}", colour="green"):
        if level > int(highest_level) + 1: 
            add_concept(taxo_graph, D4W_NAMESPACE, unique_concepts.loc[index], level, rules, default_language, default_version, create_english_labels, default_status, checkmispell, column_names)
        elif level == int(highest_level) + 1: 
            add_topConcept(taxo_graph, D4W_NAMESPACE, unique_concepts.loc[index], level, rules, default_language, default_version, create_english_labels, default_status, checkmispell, column_names)
        else: 
            add_conceptScheme(taxo_graph, D4W_NAMESPACE, unique_concepts.loc[index], level, rules, default_language, default_version, create_english_labels, creation_date, column_names)

def validation(count: int, taxo_graph: Graph, taxo_size: int, turtle_data: str, validation_server: str, output_format: str, validation_version: str):

        if count == 1: 
            taxonomy_size_validation(taxo_graph, taxo_size)
        else: 
            shacl_validation(turtle_data, validation_server, output_format, validation_version)

def excel_to_rdf(config: dict) -> None:
    """
    Converts an Excel file containing taxonomy data to an RDF file and validates the RDF using a SHACL API.  
  
    This function reads an Excel file specified by the user, processes its contents to generate an RDF graph, and then serializes the graph to a Turtle file format. After serialization, the RDF content is validated against a SHACL API.   
  
    Parameters:  
    -----------  
    config: dict
        Dictionary containing the configuration of the app

    Returns:  
    -------  
    None  

    """
    excel_path = config['input']['default_file'] 
    highest_level = config['input']['highest_level']
    lowest_level = config['input']['lowest_level']
    column_names = config['input']['information_by_level']
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

        adding_triples(taxo_excel, taxo_graph, level, highest_level, column_names, D4W_NAMESPACE, rules, default_language, default_version, create_english_labels, creation_date, default_status, checkmispell) 
            
    for rule in rules:
        for rule_label in rule: 
            logging.info(f"Labels changed based on rule {rule_label}: {CHANGED_LABELS[rule_label]}")

    logging.info(f"English labels {ENGLISH_LABELS}")
    
    duplicates = find_duplicate_values(taxo_graph)
    logging.info(f"Duplicate values in 'prefLabel': {duplicates}")  



    # Save rdf file
    taxo_graph.serialize(output_path, format=output_format)
    turtle_data = taxo_graph.serialize(format=output_format)  
    
    # Validate rdf file (number of concepts, shacl shapes)
    taxo_size = 0

    for level in range(int(highest_level), int(lowest_level) + 1):
        taxo_size += taxo_excel.drop_duplicates(subset=f"{column_names['Concept']}{level}")[f"{column_names['Concept']}{level}"].count()

    for index in tqdm([1, 2], desc="SHACL and size validation"):
        validation(index, taxo_graph, taxo_size, turtle_data, validation_server, output_format, validation_version)
        # taxonomy_size_validation(taxo_graph, taxo_size)
        # shacl_validation(turtle_data, validation_server, output_format, validation_version)