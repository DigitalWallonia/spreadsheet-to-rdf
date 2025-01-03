# Excel Taxonomy to RDF Converter  
  
This application converts taxonomy data from an Excel file into RDF format, accordingly to the [D4WTA-AP model](https://digitalwallonia.github.io/D4WTA-AP/releases/1.0.0/).
  
## Features  
  
- Converts taxonomy data from Excel files into RDF format.
- Evaluates the languages of labels to add the English labels and find potential typos in the definitions. 
- Validates RDF content against SHACL shape.

## Instructions

### Prerequisites  
  
Make sure you have the following installed:  
  
- Python 3.10.13  
- pip (Python package installer)  
  
### Installation  
  
1. Clone the repository:  
  
    ```bash  
    git clone https://github.com/yourusername/taxonomy-to-rdf.git  
    cd taxonomy-to-rdf  
    ```  
  
2. Install the required dependencies:  
  
    ```bash  
    pip install -r requirements.txt  
    ```  

3. Create a yaml config file: 
    
    ```bash
    input:  
    default_file: file\path\to\taxonomy.xlsx  
    
    transformation:  
    namespace: namespace\of\taxonomy  
    rules:  
        logfile: changes.log  
        changes:  
        - changelabel:  
            from: "charactersToExcludeFromPrefLabels"  
            to: " "  
    
    output:  
    default_file: file\path\to\output.ttl 
    default_format: turtle  
    
    validation:  
    server: url\to\shacl\validator\api 
    ``` 
  
## Usage  
  
### Command-Line Interface (CLI)  
  
This application uses a command-line interface for input and output. Here’s how to use it:  
  
```bash  
python app.py -c path/to/yaml/file  
```
- -c, --config: Path to the yaml file containing the configuration.

For example: 

```bash 
python app.py -c config.yaml  
```

For easyness, the end user can click on the app.bat that runs the python script directly without typing the command line.

### Execution

When executing, there will be a progress bar for each level of hierarchy and 1 progress bar for the validation.
The output file will be created, as specified in the configuration file.

![Execution](/doc/execution.jpg)

### Example input / output

![Example](/doc/example.jpg)

In the above example, the Slug Categorie L5 "acces-au-wifi" is transformed in the below RDF:

```
d4w:acces-au-wifi a skos:Concept ;
    eurovoc:status status:CURRENT ;
    dcterms:identifier "6tO7kpywpnel6H2Z7BHqUf" ;
    owl:versionInfo "0.0.1" ;
    skos:broader d4w:accompagnement-citoyen ;
    skos:definition "Avoir accès à une connection Internet."@fr ;
    skos:inScheme d4w:digital-wallonia ;
    skos:prefLabel "Accéder à du WiFi"@fr .
```

Note the link to the broader concept "accompagnement-citoyen" created below:

```
d4w:accompagnement-citoyen a skos:Concept ;
    eurovoc:status status:CURRENT ;
    dcterms:identifier "5q6qx1SKaGMlPJeyGpe1zJ" ;
    owl:versionInfo "0.0.1" ;
    skos:broader d4w:services ;
    skos:definition "Ensemble des accompagnements disponibles et mis à disposition du citoyen."@fr ;
    skos:inScheme d4w:digital-wallonia ;
    skos:prefLabel "Accompagnement citoyen"@fr .
```

## Structure
![Structure](/doc/structure.jpg)

The application takes 2 input (spreadsheet of the taxonomy and configuration file) and generates 2 output (taxonomy in RDF and log file).

The application is composed by App.py which passes the configuration file to the Transformer.py via the function excel_to_rdf() .

The Transformer.py, open the spreadsheet indicated in the configuration file and it invokes functions (add_concept(), add_topConcept() and add_ConceptScheme()) to create the SKOS Concept and ConceptScheme with labels, definitions, etc. coming from the spreadsheet.

When creating these concepts, URI need to be created and labels need to be changed via the functions get_uri() and cleaning_label() defined in data_utils.py.

At the end of the creation of the taxonomy in RDF, the Transformer.py calls the shacl_validation() function, defined in the data_utils.py to validate against the ITB Shacl Validator instance.

### Functions
Transformer.py
- excel_to_rdf(config): Main function that orchestrates the conversion of an Excel file to RDF format and validates it using a SHACL API having as input the configuration file object.
- adding_triples(taxo_excel, taxo_graph, level, highest_level, column_names, D4W_NAMESPACE, rules, default_language, default_version, create_english_labels, creation_date, default_status, checkmispell): Processes taxonomy data and adds RDF triples to the graph based on the level of taxonomy, calling the functions add_concept(), add_topConcept() and add_conceptScheme().

Create_triples.py
- add_concept(taxonomy, namespace, concept, level, rules, default_language, default_version, create_english_labels, default_status, checkmispell): Adds RDF triples representing a concept to the graph. 
- add_topConcept(taxonomy, namespace, concept, level, rules, default_language, default_version, create_english_labels, default_status, checkmispell): Adds RDF triples for a top-level concept and links it to the taxonomy scheme.
- add_conceptScheme(taxonomy, namespace, concept, level, rules, default_language, default_version, create_english_labels, creation_date): Adds RDF triples representing a concept scheme, including metadata like creation date.

These functions rely on [lingua-language-detector](https://github.com/pemistahl/lingua-py) library; which is configured with English and French language detectors, to see if a label is in English or French (default).
By default all the labels have French suffix (@fr). If the label is detected to be English, the label is also added with English suffix (@en).
For example:
```
skos:prefLabel "Access Management"@en,
        "Access Management"@fr .
or
skos:prefLabel "AdTech"@en,
        "AdTech"@fr .
```

Data_utils.py
- ensure_first_letter_capitalized(text): Ensures the first letter of a string is capitalized.
- cleaning_label(label, uri, rules): Cleans a label by replacing special characters with spaces and capitalizing the first letter.
- check_mispell(definition): Find typos in the definitions. This function relies on [phunspell](https://github.com/dvwright/phunspell) library, in turn based on [spylls](https://github.com/zverok/spylls), searching on the [French](https://github.com/dvwright/phunspell/tree/main/phunspell/data/dictionary/fr_FR) and [English](https://github.com/dvwright/phunspell/tree/main/phunspell/data/dictionary/en) vocabularies. As there are many nouns, not really typos, the potential mispells are inserted in the [log file](https://github.com/DigitalWallonia/spreadsheet-to-rdf/blob/main/changes.log).
- get_uri(namespace, concept, level): Constructs a URI for a concept within a specified namespace and level.
- shacl_validation(turtle_data, validation_server, output_format, validation_version): Validates RDF data using the ITB Shacl Validator.

## Validation
After generating the RDF file, the application validates it against a SHACL API endpoint at http://localhost:8080/shacl/d4wta-ap/api/validate, specified in the configuration file. Ensure this endpoint is accessible and configured to process validation requests.

### Error Handling
If the validation fails or the API returns an error, the application will log the status code and error message. Ensure the API service is running and accessible.
