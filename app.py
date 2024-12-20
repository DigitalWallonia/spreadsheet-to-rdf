import argparse  
from tqdm import tqdm
from utils.transformer import excel_to_rdf

# Main execution  
if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='Convert an Excel taxonomy to RDF format and validate it using a SHACL API.')  
  
    parser.add_argument('-e', '--excel', type=str, required=True, help='Path to the Excel file containing taxonomy data.')  
    parser.add_argument('-n', '--namespace', type=str, required=True, help='Namespace to be used in the RDF output.')  
    parser.add_argument('-o', '--output', type=str, required=True, help='File path to save the resulting RDF file.')  
  
    args = parser.parse_args()  
  
    try:  
        excel_to_rdf(args.excel, args.namespace, args.output)  
    except Exception as e:  
        print(f"An error occurred: {e}")