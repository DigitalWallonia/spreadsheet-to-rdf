import json
import pandas as pd
from rdflib import Graph
from tqdm import tqdm
from utils.creating_triples import add_concept, add_conceptScheme, add_topConcept
from utils.data_utils import rename_columns, shacl_validation


def excel_to_rdf(excel: str, namespace: str, output_path: str):
    EXCEL_PATH = excel # r"C:\Users\ecaudron001\Downloads\2024-10-08_D4W_taxxo-complete.xlsx"
    NAMESPACE = namespace # "http://www.data4wallonia.be/Test-Taxonomy#"

    # Open and read the JSON file
    with open('excel_info.json', 'r', encoding="utf-8") as file:
        EXCEL_INFO = json.load(file)

    # Read taxonomy from excel
    taxo_excel = pd.read_excel(EXCEL_PATH)

    # Create rdf version of taxonomy
    taxo_graph = Graph()
    taxo_graph.bind("d4w", NAMESPACE)
    taxo_graph.bind("status", "http://publications.europa.eu/resource/authority/concept-status/")
    taxo_graph.bind("eurovoc", "http://publications.europa.eu/ontology/euvoc#")

    # Add categories to the rdf
    for level in range(int(EXCEL_INFO["highest level"]), int(EXCEL_INFO["lowest level"]) + 1):

        try:     
            unique_concepts = taxo_excel.drop_duplicates(subset=f"Titre Catégorie L{level}")
            
            for index in tqdm(unique_concepts.index, desc=f"Processing Level {level}"):
                if level > 3: 
                    add_concept(taxo_graph, NAMESPACE, unique_concepts.loc[index], level)
                elif level == 3: 
                    add_topConcept(taxo_graph, NAMESPACE, unique_concepts.loc[index], level)
                else: 
                    add_conceptScheme(taxo_graph, NAMESPACE, unique_concepts.loc[index], level)
        except:
            rename_columns(taxo_excel, EXCEL_INFO, level)
            unique_concepts = taxo_excel.drop_duplicates(subset=f"Titre Catégorie L{level}")
            
            for index in tqdm(unique_concepts.index, desc=f"Processing Level {level}"):
                if level > 3: 
                    add_concept(taxo_graph, NAMESPACE, unique_concepts.loc[index], level)
                elif level == 3: 
                    add_topConcept(taxo_graph, NAMESPACE, unique_concepts.loc[index], level)
                else: 
                    add_conceptScheme(taxo_graph, NAMESPACE, unique_concepts.loc[index], level)

    # Save rdf file
    taxo_graph.serialize(output_path, format="ttl")
    turtle_data = taxo_graph.serialize(format="turtle")  
    print("Shacl validation ongoing:")
    shacl_validation(turtle_data)