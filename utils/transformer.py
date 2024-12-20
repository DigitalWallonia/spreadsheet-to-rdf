import json
import pandas as pd
from rdflib import Graph
from tqdm import tqdm
from utils.creating_triples import add_concept, add_conceptScheme, add_topConcept
from utils.data_utils import rename_columns, shacl_validation

def adding_triples(taxo_excel: pd, taxo_graph: Graph, level: int, EXCEL_INFO: dict, D4W_NAMESPACE: str) -> None:
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
  
    Returns:  
    --------  
    None

    """
    unique_concepts = taxo_excel.drop_duplicates(subset=f"Titre Catégorie L{level}")
            
    # Loop over concepts by level
    for index in tqdm(unique_concepts.index, desc=f"Processing Level {level}"):
        if level > int(EXCEL_INFO["highest level"]) + 1: 
            add_concept(taxo_graph, D4W_NAMESPACE, unique_concepts.loc[index], level)
        elif level == int(EXCEL_INFO["highest level"]) + 1: 
            add_topConcept(taxo_graph, D4W_NAMESPACE, unique_concepts.loc[index], level)
        else: 
            add_conceptScheme(taxo_graph, D4W_NAMESPACE, unique_concepts.loc[index], level)


def excel_to_rdf(excel_path: str, namespace: str, output_path: str) -> None:
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

    Returns:  
    -------  
    None  

    """
    # Defining static variables
    EXCEL_PATH = excel_path 
    EXCEL_INFO_PATH = 'excel_info.json'
    
    D4W_NAMESPACE = namespace
    EUROVOC_NS = "http://publications.europa.eu/ontology/euvoc#"
    STATUS_NS = "http://publications.europa.eu/resource/authority/concept-status/"

    # Open and read a JSON file containing excel metadata
    with open(EXCEL_INFO_PATH, 'r', encoding="utf-8") as file:
        EXCEL_INFO = json.load(file)

    # Read taxonomy from excel
    taxo_excel = pd.read_excel(EXCEL_PATH)

    # Create rdf version of taxonomy
    taxo_graph = Graph()
    taxo_graph.bind("d4w", D4W_NAMESPACE)
    taxo_graph.bind("status", STATUS_NS)
    taxo_graph.bind("eurovoc", EUROVOC_NS)

    # Add triples to the rdf by level of the taxonomy
    for level in range(int(EXCEL_INFO["highest level"]), int(EXCEL_INFO["lowest level"]) + 1):

        try:     
            adding_triples(taxo_excel, taxo_graph, level, EXCEL_INFO, D4W_NAMESPACE) 
        except:
            rename_columns(taxo_excel, EXCEL_INFO, level) # If the excel columns does not respect the naming convention rename those
            adding_triples(taxo_excel, taxo_graph, level, EXCEL_INFO, D4W_NAMESPACE)

    # Save rdf file
    taxo_graph.serialize(output_path, format="ttl")
    turtle_data = taxo_graph.serialize(format="turtle")  
    
    # Validate rdf file
    shacl_validation(turtle_data)