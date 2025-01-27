from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import SKOS, RDF, DCTERMS, OWL, XSD
from rdflib import Literal as LiteralRDF
from utils.data_utils import get_uri, cleaning_label, check_mispell
from lingua import Language, LanguageDetectorBuilder

ENGLISH_LABELS = []
languages = [Language.ENGLISH, Language.FRENCH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

def add_concept(taxonomy: Graph, namespace: str, concept:dict, level: int, rules: dict, default_language: str, default_version: str, create_english_labels: str, default_status: str, checkmispell: str, column_names: dict) -> None:
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
    default_language : str    
        The default language code for labeling the concepts.  
    default_version : str    
        The version of the concept being added.  
    create_english_labels : str    
        Flag indicating whether to create English labels for the concepts.  
    default_status : str    
        The default status URI for the concept.  
    checkmispell : str    
        Flag indicating whether to check for misspellings in the concept's definition.  
    column_names: dict    
        The column names prefix used in the Excel file.

  
    Returns:  
    --------  
    None  
    """
    uri = get_uri(namespace, concept, level, column_names)

    # Concept
    taxonomy.add((URIRef(uri), RDF.type, SKOS.Concept)) 

    if concept[f"{column_names['popTitle']}{level}"] != "":
        taxonomy.add((URIRef(uri), DCTERMS.title, LiteralRDF(concept[f"{column_names['popTitle']}{level}"], lang=f"{default_language}")))
    taxonomy.add((URIRef(uri), SKOS.broader, URIRef(get_uri(namespace, concept, level-1, column_names))))
    definition = concept[f"{column_names['Definition']}{level}"]
    if definition != "":
        if(checkmispell == True):
            check_mispell(definition)
        taxonomy.add((URIRef(uri), SKOS.definition, LiteralRDF(definition, lang=f"{default_language}")))
    taxonomy.add((URIRef(uri), DCTERMS.identifier, LiteralRDF(concept[f"{column_names['ID']}{level}"])))
    taxonomy.add((URIRef(uri), SKOS.inScheme, URIRef(get_uri(namespace, concept, 2, column_names))))
    #taxonomy.add((URIRef(uri), DCTERMS.isReplacedBy, URIRef(get_uri(namespace, concept, level-1))))
    cleaned_label = cleaning_label(concept[f"{column_names['prefLabel']}{level}"], uri, rules)
    if cleaned_label != "":
        language = detector.detect_language_of(cleaned_label) 
        if(language.iso_code_639_1.name == 'EN'):
            ENGLISH_LABELS.append(cleaned_label)
            if(create_english_labels == True):
                taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaned_label, "en")))
        taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaned_label, f"{default_language}")))
    #taxonomy.add((URIRef(uri), DCTERMS.replaces, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), URIRef("http://publications.europa.eu/ontology/euvoc#status"), URIRef(f"{default_status}")))
    taxonomy.add((URIRef(uri), OWL.versionInfo, LiteralRDF(f"{default_version}")))

def add_topConcept(taxonomy: Graph, namespace: str, concept:dict, level: int, rules: dict, default_language: str, default_version: str, create_english_labels: str, default_status: str, checkmispell: str, column_names: dict) -> None:
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
    default_language : str    
        The default language code for labeling the concepts.  
    default_version : str    
        The version of the concept being added.  
    create_english_labels : str    
        Flag indicating whether to create English labels for the concepts.  
    default_status : str    
        The default status URI for the concept.  
    checkmispell : str    
        Flag indicating whether to check for misspellings in the concept's definition.
    column_names: dict    
        The column names prefix used in the Excel file.  
  
  
    Returns:  
    --------  
    None  
    """
    uri = get_uri(namespace, concept, level, column_names)
    # Concept
    taxonomy.add((URIRef(uri), RDF.type, SKOS.Concept)) 

    if concept[f"{column_names['popTitle']}{level}"] != "":
        taxonomy.add((URIRef(uri), DCTERMS.title, LiteralRDF(concept[f"{column_names['popTitle']}{level}"], lang=f"{default_language}")))
    definition = concept[f"{column_names['Definition']}{level}"]
    if definition != "":
        if(checkmispell == True):
            check_mispell(definition)
        taxonomy.add((URIRef(uri), SKOS.definition, LiteralRDF(definition, lang=f"{default_language}")))
    taxonomy.add((URIRef(uri), DCTERMS.identifier, LiteralRDF(concept[f"{column_names['ID']}{level}"])))
    taxonomy.add((URIRef(uri), SKOS.inScheme, URIRef(get_uri(namespace, concept, 2, column_names))))
    #taxonomy.add((URIRef(uri), DCTERMS.isReplacedBy, URIRef(get_uri(namespace, concept, level-1))))
    cleaned_label = cleaning_label(concept[f"{column_names['prefLabel']}{level}"], uri, rules)
    if cleaned_label != "":
        language = detector.detect_language_of(cleaned_label) 
        if(language.iso_code_639_1.name == 'EN'):
            ENGLISH_LABELS.append(cleaned_label)
            if(create_english_labels == True):
                taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaned_label, "en")))
        taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaned_label, f"{default_language}")))
    #taxonomy.add((URIRef(uri), DCTERMS.replaces, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), URIRef("http://publications.europa.eu/ontology/euvoc#status"), URIRef(f"{default_status}")))
    taxonomy.add((URIRef(uri), SKOS.topConceptOf, URIRef(get_uri(namespace, concept, 2, column_names))))
    taxonomy.add((URIRef(uri), OWL.versionInfo, LiteralRDF(f"{default_version}")))

    taxonomy.add((URIRef(get_uri(namespace, concept, 2, column_names)), SKOS.hasTopConcept, URIRef(uri)))

def add_conceptScheme(taxonomy: Graph, namespace: str, concept:dict, level: int, rules: dict, default_language: str, default_version: str, create_english_labels: str, creation_date: str, column_names: dict) -> None:
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
    default_language : str    
        The default language code for labeling the concept scheme.  
    default_version : str    
        The version of the concept scheme being added.  
    create_english_labels : str    
        Flag indicating whether to create English labels for the concept scheme.  
    creation_date : str    
        The creation date of the concept scheme.
    column_names: dict    
        The column names prefix used in the Excel file.
        
    Returns:  
    --------  
    None  
    """
    uri = get_uri(namespace, concept, level, column_names)

    # Concept
    taxonomy.add((URIRef(uri), RDF.type, SKOS.ConceptScheme))
    
    taxonomy.add((URIRef(uri), DCTERMS.created, LiteralRDF(f"{creation_date}", datatype=XSD.date)))
    #taxonomy.add((URIRef(uri), DCTERMS.issued, LiteralRDF("")))
    #taxonomy.add((URIRef(uri), DCTERMS.modified, LiteralRDF("")))
    taxonomy.add((URIRef(uri), DCTERMS.identifier, LiteralRDF(concept[f"{column_names['ID']}{level}"])))
    #taxonomy.add((URIRef(uri), DCTERMS.isReplacedBy, URIRef(get_uri(namespace, concept, level-1))))
    cleaned_label = cleaning_label(concept[f"{column_names['prefLabel']}{level}"], uri, rules)
    if cleaned_label != "":
        language = detector.detect_language_of(cleaned_label) 
        if(language.iso_code_639_1.name == 'EN'):
            ENGLISH_LABELS.append(cleaned_label)
            if(create_english_labels == True):
                taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaned_label, "en")))
        taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaned_label, f"{default_language}")))
    #taxonomy.add((URIRef(uri), DCTERMS.replaces, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), DCTERMS.title, LiteralRDF(concept[f"{column_names['prefLabel']}{level}"], lang=f"{default_language}")))
    taxonomy.add((URIRef(uri), OWL.versionInfo, LiteralRDF(f"{default_version}")))
