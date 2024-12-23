from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import SKOS, RDF, DCTERMS, OWL, XSD
from rdflib import Literal as LiteralRDF
from utils.data_utils import get_uri, cleaning_label

def add_concept(taxonomy: Graph, namespace: str, concept:dict, level: int, rules: dict) -> None:
    """  
    Adds RDF triples to a graph representing a concept within a taxonomy.  
  
    This function creates RDF triples for a specific concept in a taxonomy. It defines a concept's metadata, including its broader category, definition, identifier, and preferred label, and links it to a concept scheme.  
  
    Parameters:  
    -----------  
    taxonomy : Graph  
        The RDFLib Graph object to which RDF triples representing the concept will be added.  
    namespace : str  
        The base namespace used to construct URIs for the RDF triples.  
    concept : dict  
        A dictionary containing details about the concept, extracted from the taxonomy.  
    level : int  
        The level of the concept in the taxonomy, used to differentiate hierarchical relationships.  
    rules: dict
        Series of changes to make to the labels of the taxonomy elements.
  
    Returns:  
    --------  
    None  
    """
    uri = get_uri(namespace, concept, level)

    # Concept
    taxonomy.add((URIRef(uri), RDF.type, SKOS.Concept)) 

    #taxonomy.add((URIRef(uri), SKOS.altLabel, LiteralRDF("altLabel", lang="fr")))
    taxonomy.add((URIRef(uri), SKOS.broader, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), SKOS.definition, LiteralRDF(concept[f"Description Catégorie L{level}"], lang="fr")))
    taxonomy.add((URIRef(uri), DCTERMS.identifier, LiteralRDF(concept[f"ID catégorie L{level}"])))
    taxonomy.add((URIRef(uri), SKOS.inScheme, URIRef(get_uri(namespace, concept, 2))))
    #taxonomy.add((URIRef(uri), DCTERMS.isReplacedBy, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaning_label(concept[f"Titre Catégorie L{level}"], uri, rules["from"], rules["to"]), lang="fr")))
    #taxonomy.add((URIRef(uri), DCTERMS.replaces, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), URIRef("http://publications.europa.eu/ontology/euvoc#status"), URIRef("http://publications.europa.eu/resource/authority/concept-status/CURRENT")))
    taxonomy.add((URIRef(uri), OWL.versionInfo, LiteralRDF("0.0.1")))

def add_topConcept(taxonomy: Graph, namespace: str, concept:dict, level: int, rules: dict) -> None:
    """
    Adds RDF triples to a graph representing a top-level concept within a taxonomy.  
  
    This function creates RDF triples for a top-level concept, including its metadata such as definition, identifier, and preferred label. It also establishes the top concept relationship within the taxonomy scheme.  
  
    Parameters:  
    -----------  
    taxonomy : Graph  
        The RDFLib Graph object to which RDF triples representing the top-level concept will be added.  
    namespace : str  
        The base namespace used to construct URIs for the RDF triples.  
    concept : dict  
        A dictionary containing details about the top-level concept, extracted from the taxonomy.  
    level : int  
        The level of the concept in the taxonomy, typically the level at which it is considered a top concept.
    rules: dict
        Series of changes to make to the labels of the taxonomy elements.  
  
    Returns:  
    --------  
    None  
    """
    uri = get_uri(namespace, concept, level)
    # Concept
    taxonomy.add((URIRef(uri), RDF.type, SKOS.Concept)) 

    #taxonomy.add((URIRef(uri), SKOS.altLabel, LiteralRDF("", lang="fr")))
    taxonomy.add((URIRef(uri), SKOS.definition, LiteralRDF(concept[f"Description Catégorie L{level}"], lang="fr")))
    taxonomy.add((URIRef(uri), DCTERMS.identifier, LiteralRDF(concept[f"ID catégorie L{level}"])))
    taxonomy.add((URIRef(uri), SKOS.inScheme, URIRef(get_uri(namespace, concept, 2))))
    #taxonomy.add((URIRef(uri), DCTERMS.isReplacedBy, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaning_label(concept[f"Titre Catégorie L{level}"], uri, rules["from"], rules["to"]), lang="fr")))
    #taxonomy.add((URIRef(uri), DCTERMS.replaces, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), URIRef("http://publications.europa.eu/ontology/euvoc#status"), URIRef("http://publications.europa.eu/resource/authority/concept-status/CURRENT")))
    taxonomy.add((URIRef(uri), SKOS.topConceptOf, URIRef(get_uri(namespace, concept, 2))))
    taxonomy.add((URIRef(uri), OWL.versionInfo, LiteralRDF("0.0.1")))

    taxonomy.add((URIRef(get_uri(namespace, concept, 2)), SKOS.hasTopConcept, URIRef(uri)))

def add_conceptScheme(taxonomy: Graph, namespace: str, concept:dict, level: int, rules: dict) -> None:
    """
    Adds RDF triples to a graph representing a concept scheme within a taxonomy.  
  
    This function defines RDF triples for a concept scheme, including metadata such as creation date, identifier, and title. It establishes the scheme as a collection or organization of concepts.  
  
    Parameters:  
    -----------  
    taxonomy : Graph  
        The RDFLib Graph object to which RDF triples representing the concept scheme will be added.  
    namespace : str  
        The base namespace used to construct URIs for the RDF triples.  
    concept : dict  
        A dictionary containing details about the concept scheme, extracted from the taxonomy.  
    level : int  
        The level of the concept scheme in the taxonomy hierarchy.  
    rules: dict
        Series of changes to make to the labels of the taxonomy elements.
        
    Returns:  
    --------  
    None  
    """
    uri = get_uri(namespace, concept, level)

    # Concept
    taxonomy.add((URIRef(uri), RDF.type, SKOS.ConceptScheme))
    
    taxonomy.add((URIRef(uri), DCTERMS.created, LiteralRDF("2024-12-18", datatype=XSD.date)))
    #taxonomy.add((URIRef(uri), DCTERMS.issued, LiteralRDF("")))
    #taxonomy.add((URIRef(uri), DCTERMS.modified, LiteralRDF("")))
    taxonomy.add((URIRef(uri), DCTERMS.identifier, LiteralRDF(concept[f"ID catégorie L{level}"])))
    #taxonomy.add((URIRef(uri), DCTERMS.isReplacedBy, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaning_label(concept[f"Titre Catégorie L{level}"], uri, rules["from"], rules["to"]), lang="fr")))
    #taxonomy.add((URIRef(uri), DCTERMS.replaces, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), DCTERMS.title, LiteralRDF(concept[f"Titre Catégorie L{level}"], lang="fr")))
    taxonomy.add((URIRef(uri), OWL.versionInfo, LiteralRDF("0.0.1")))