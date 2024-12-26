import argparse  
import logging
from tqdm import tqdm
from utils.transformer import excel_to_rdf
import yaml  

def setup_logging(logfile):  
    logging.basicConfig(  
        filename=logfile,  
        level=logging.INFO,  
        format='%(asctime)s - %(levelname)s - %(message)s'  
    )  

def load_config(config_path):
    with open(config_path, 'r') as file:  
        config = yaml.safe_load(file)  
    return config 

# Main execution  
if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='Convert an Excel taxonomy to RDF format and validate it using a SHACL API.')  
    parser.add_argument('-c', '--config', type=str, required=True, help='Path to the config.yaml file.')  
    args = parser.parse_args() 
    config = load_config(args.config) 

    setup_logging(config['transformation']['rules']['logfile'])
    try:  
        excel_to_rdf(config['input']['default_file'], config['input']['highest_level'], config['input']['lowest_level'], config['transformation']['namespace'], config['transformation']['create_english_labels'], config['transformation']['creation_date'], config['output']['default_file'], config['output']['default_format'], config['validation']['server'], config['validation']['version'], config['transformation']['rules']['changes'], config['transformation']['default_language'], config['transformation']['default_version'], config['transformation']['default_status'])  
    except Exception as e:  
        print(f"An error occurred: {e}")