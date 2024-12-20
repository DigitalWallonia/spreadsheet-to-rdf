from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import SKOS, RDF, DCTERMS, OWL, XSD
from rdflib import Literal as LiteralRDF
from utils.data_utils import get_uri, cleaning_label

def add_concept(taxonomy: Graph, namespace: str, concept:dict, level: int) -> None:
    uri = get_uri(namespace, concept, level)

    # Concept
    taxonomy.add((URIRef(uri), RDF.type, SKOS.Concept)) 

    #taxonomy.add((URIRef(uri), SKOS.altLabel, LiteralRDF("altLabel", lang="fr")))
    taxonomy.add((URIRef(uri), SKOS.broader, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), SKOS.definition, LiteralRDF(concept[f"Description Catégorie L{level}"], lang="fr")))
    taxonomy.add((URIRef(uri), DCTERMS.identifier, LiteralRDF(concept[f"ID catégorie L{level}"])))
    taxonomy.add((URIRef(uri), SKOS.inScheme, URIRef(get_uri(namespace, concept, 2))))
    #taxonomy.add((URIRef(uri), DCTERMS.isReplacedBy, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaning_label(concept[f"Titre Catégorie L{level}"]), lang="fr")))
    #taxonomy.add((URIRef(uri), DCTERMS.replaces, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), URIRef("http://publications.europa.eu/ontology/euvoc#status"), URIRef("http://publications.europa.eu/resource/authority/concept-status/CURRENT")))
    taxonomy.add((URIRef(uri), OWL.versionInfo, LiteralRDF("0.0.1")))

def add_topConcept(taxonomy: Graph, namespace: str, concept:dict, level: int) -> None:
    uri = get_uri(namespace, concept, level)
    # Concept
    taxonomy.add((URIRef(uri), RDF.type, SKOS.Concept)) 

    #taxonomy.add((URIRef(uri), SKOS.altLabel, LiteralRDF("", lang="fr")))
    taxonomy.add((URIRef(uri), SKOS.definition, LiteralRDF(concept[f"Description Catégorie L{level}"], lang="fr")))
    taxonomy.add((URIRef(uri), DCTERMS.identifier, LiteralRDF(concept[f"ID catégorie L{level}"])))
    taxonomy.add((URIRef(uri), SKOS.inScheme, URIRef(get_uri(namespace, concept, 2))))
    #taxonomy.add((URIRef(uri), DCTERMS.isReplacedBy, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaning_label(concept[f"Titre Catégorie L{level}"]), lang="fr")))
    #taxonomy.add((URIRef(uri), DCTERMS.replaces, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), URIRef("http://publications.europa.eu/ontology/euvoc#status"), URIRef("http://publications.europa.eu/resource/authority/concept-status/CURRENT")))
    taxonomy.add((URIRef(uri), SKOS.topConceptOf, URIRef(get_uri(namespace, concept, 2))))
    taxonomy.add((URIRef(uri), OWL.versionInfo, LiteralRDF("0.0.1")))

    taxonomy.add((URIRef(get_uri(namespace, concept, 2)), SKOS.hasTopConcept, URIRef(uri)))

def add_conceptScheme(taxonomy: Graph, namespace: str, concept:dict, level: int) -> None:
    uri = get_uri(namespace, concept, level)

    # Concept
    taxonomy.add((URIRef(uri), RDF.type, SKOS.ConceptScheme))
    
    taxonomy.add((URIRef(uri), DCTERMS.created, LiteralRDF("2024-12-18", datatype=XSD.date)))
    #taxonomy.add((URIRef(uri), DCTERMS.issued, LiteralRDF("")))
    #taxonomy.add((URIRef(uri), DCTERMS.modified, LiteralRDF("")))
    taxonomy.add((URIRef(uri), DCTERMS.identifier, LiteralRDF(concept[f"ID catégorie L{level}"])))
    #taxonomy.add((URIRef(uri), DCTERMS.isReplacedBy, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), SKOS.prefLabel, LiteralRDF(cleaning_label(concept[f"Titre Catégorie L{level}"]), lang="fr")))
    #taxonomy.add((URIRef(uri), DCTERMS.replaces, URIRef(get_uri(namespace, concept, level-1))))
    taxonomy.add((URIRef(uri), DCTERMS.title, LiteralRDF(concept[f"Titre Catégorie L{level}"], lang="fr")))
    taxonomy.add((URIRef(uri), OWL.versionInfo, LiteralRDF("0.0.1")))