from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import SKOS, RDF, DCTERMS, OWL, XSD
from rdflib import Literal as LiteralRDF
from utils.data_utils import get_uri, cleaning_label
import logging
from lingua import Language, LanguageDetectorBuilder
import phunspell
import re

pspell_fr = phunspell.Phunspell('fr_FR')
pspell_en = phunspell.Phunspell('en_GB')
ENGLISH_LABELS = []
languages = [Language.ENGLISH, Language.FRENCH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

def check_mispell(definition):
    res = re.findall( r'\w+|[^\s\w]+', definition)
    #res = re.findall( r'\b\S+\b', definition)
    b = ["," , ";" , "." , '"' , "(" , ")." , ")" , ":" , "?)," , ".)" , ")," , "/" , ");" , ".)." , "\"." , ".)," , "?." , "?" , "\"," , "%" , "#" , "!" , "&" , ".;", ",…." , "…." , "»" , "«" , "…)," , "…)" , "...)." , "@" , ".:" , "…)." , "…" , "'" , "€," , "”," , "'”" , ")-", '?".' , '?",' , '?"']
    result = list(set(res) - set(b))
    mispelled_fr = pspell_fr.lookup_list(result)
    mispelled_en = pspell_en.lookup_list(mispelled_fr)
    if(len(mispelled_en) > 0):
        logging.info(f" mispelled: {mispelled_en} in {definition}")

def add_concept(taxonomy: Graph, namespace: str, concept:dict, level: int, rules: dict, default_language: str, default_version: str, create_english_labels: str, default_status: str, checkmispell: str) -> None:
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
    definition = concept[f"Description Catégorie L{level}"]
    if(checkmispell == True):
        check_mispell(definition)
    taxonomy.add((URIRef(uri), SKOS.definition, LiteralRDF(definition, lang=f"{default_language}")))
    taxonomy.add((URIRef(uri), DCTERMS.identifier, LiteralRDF(concept[f"ID catégorie L{level}"])))
    taxonomy.add((URIRef(uri), SKOS.inScheme, URIRef(get_uri(namespace, concept, 2))))
    #taxonomy.add((URIRef(uri), DCTERMS.isReplacedBy, URIRef(get_uri(namespace, concept, level-1))))
    cleaned_label = cleaning_label(concept[f"Titre Catégorie L{level}"], uri, rules)
    #lang = detect(cleaned_label)
    #if(lang == "en"):
    #    ENGLISH_LABELS.append(cleaned_label) 
    #langs = detect_langs(cleaned_label)[0]
    #if(langs.lang == "en" and langs.prob >= 0.86):
    #    ENGLISH_LABELS.append(cleaned_label)  
    #else:
    #    if(langs.lang == "en"):
    #        logging.info(f"label excluded {cleaned_label} - {langs.prob}")
    language = detector.detect_language_of(cleaned_label) 
    if(language.iso_code_639_1.name == 'EN'):
        ENGLISH_LABELS.append(cleaned_label)
        if(create_english_labels == True):
            taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaned_label, "en")))
    taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaned_label, f"{default_language}")))
    #taxonomy.add((URIRef(uri), DCTERMS.replaces, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), URIRef("http://publications.europa.eu/ontology/euvoc#status"), URIRef(f"{default_status}")))
    taxonomy.add((URIRef(uri), OWL.versionInfo, LiteralRDF(f"{default_version}")))

def add_topConcept(taxonomy: Graph, namespace: str, concept:dict, level: int, rules: dict, default_language: str, default_version: str, create_english_labels: str, default_status: str, checkmispell: str) -> None:
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

    #taxonomy.add((URIRef(uri), SKOS.altLabel, LiteralRDF("", lang="fr")))^
    definition = concept[f"Description Catégorie L{level}"]
    if(checkmispell == True):
        check_mispell(definition)
    taxonomy.add((URIRef(uri), SKOS.definition, LiteralRDF(definition, lang=f"{default_language}")))
    taxonomy.add((URIRef(uri), DCTERMS.identifier, LiteralRDF(concept[f"ID catégorie L{level}"])))
    taxonomy.add((URIRef(uri), SKOS.inScheme, URIRef(get_uri(namespace, concept, 2))))
    #taxonomy.add((URIRef(uri), DCTERMS.isReplacedBy, URIRef(get_uri(namespace, concept, level-1))))
    cleaned_label = cleaning_label(concept[f"Titre Catégorie L{level}"], uri, rules)
    language = detector.detect_language_of(cleaned_label) 
    if(language.iso_code_639_1.name == 'EN'):
        ENGLISH_LABELS.append(cleaned_label)
        if(create_english_labels == True):
            taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaned_label, "en")))
    taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaned_label, f"{default_language}")))
    #taxonomy.add((URIRef(uri), DCTERMS.replaces, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), URIRef("http://publications.europa.eu/ontology/euvoc#status"), URIRef(f"{default_status}")))
    taxonomy.add((URIRef(uri), SKOS.topConceptOf, URIRef(get_uri(namespace, concept, 2))))
    taxonomy.add((URIRef(uri), OWL.versionInfo, LiteralRDF(f"{default_version}")))

    taxonomy.add((URIRef(get_uri(namespace, concept, 2)), SKOS.hasTopConcept, URIRef(uri)))

def add_conceptScheme(taxonomy: Graph, namespace: str, concept:dict, level: int, rules: dict, default_language: str, default_version: str, create_english_labels: str, creation_date: str) -> None:
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
    
    taxonomy.add((URIRef(uri), DCTERMS.created, LiteralRDF(f"{creation_date}", datatype=XSD.date)))
    #taxonomy.add((URIRef(uri), DCTERMS.issued, LiteralRDF("")))
    #taxonomy.add((URIRef(uri), DCTERMS.modified, LiteralRDF("")))
    taxonomy.add((URIRef(uri), DCTERMS.identifier, LiteralRDF(concept[f"ID catégorie L{level}"])))
    #taxonomy.add((URIRef(uri), DCTERMS.isReplacedBy, URIRef(get_uri(namespace, concept, level-1))))
    cleaned_label = cleaning_label(concept[f"Titre Catégorie L{level}"], uri, rules)
    language = detector.detect_language_of(cleaned_label) 
    if(language.iso_code_639_1.name == 'EN'):
        ENGLISH_LABELS.append(cleaned_label)
        if(create_english_labels == True):
            taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaned_label, "en")))
    taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaned_label, f"{default_language}")))
    #taxonomy.add((URIRef(uri), DCTERMS.replaces, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), DCTERMS.title, LiteralRDF(concept[f"Titre Catégorie L{level}"], lang=f"{default_language}")))
    taxonomy.add((URIRef(uri), OWL.versionInfo, LiteralRDF(f"{default_version}")))