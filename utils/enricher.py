from rdflib import Graph
from rdflib.namespace import SKOS


def add_synonyms():

    return "synonyms"

def english_label():

    return "english"

def similarity_analysis():

    return "similar string"


def enrich_rdf(taxo_ttl_path: str):
    
    taxo_graph = Graph()
    taxo_graph.parse(taxo_ttl_path, format="ttl")
    
    return "hello"