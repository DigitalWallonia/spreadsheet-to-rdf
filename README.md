# Excel Taxonomy to RDF Converter  
  
This application converts taxonomy data from an Excel file into RDF format and validates the RDF using a SHACL API. It processes the taxonomy data, generates RDF triples, and checks for conformance with SHACL shapes.  
  
## Features  
  
- Converts taxonomy data from Excel files into RDF format.  
- Supports RDF serialization in Turtle format.  
- Validates RDF content using a SHACL API.  
- Provides detailed logging of validation results.  
  
## Prerequisites  
  
Make sure you have the following installed:  
  
- Python 3.10.13  
- pip (Python package installer)  
  
## Installation  
  
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

#### Example
```bash 
python app.py -c config.yaml  
```

## Functions
- excel_to_rdf(excel, namespace, output_path): Main function that orchestrates the conversion of an Excel file to RDF format and validates it using a SHACL API.

Generation of triples: 
- add_concept(taxonomy, namespace, concept, level): Adds RDF triples representing a concept to the graph.
- add_topConcept(taxonomy, namespace, concept, level): Adds RDF triples for a top-level concept and links it to the taxonomy scheme.
- add_conceptScheme(taxonomy, namespace, concept, level): Adds RDF triples representing a concept scheme, including metadata like creation date.
- adding_triples(taxo_excel, taxo_graph, level, EXCEL_INFO, D4W_NAMESPACE): Processes taxonomy data and adds RDF triples to the graph based on the level of taxonomy.

Validation: 
- shacl_validation(turtle_data): Validates RDF data in Turtle format using a SHACL API.

Some data_utils: 
- ensure_first_letter_capitalized(text): Ensures the first letter of a string is capitalized.
- cleaning_label(label): Cleans a label by replacing special characters with spaces and capitalizing the first letter.
- get_uri(namespace, concept, level): Constructs a URI for a concept within a specified namespace and level.
- rename_columns(excel, excel_info, level): Renames columns in a DataFrame based on taxonomy information.

## Validation
After generating the RDF file, the application validates it against a SHACL API endpoint at http://localhost:8080/shacl/d4wta-ap/api/validate. Ensure this endpoint is accessible and configured to process validation requests.

### Error Handling
If the validation fails or the API returns an error, the application will log the status code and error message. Ensure the API service is running and accessible.