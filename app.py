import argparse  
import logging
from tqdm import tqdm
from utils.transformer import excel_to_rdf
import yaml  

def setup_logging(logfile):  
    logging.basicConfig(  
        filename=logfile,  
        level=logging.INFO,  
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding="utf-8"
    )  

def load_config(config_path):
    with open(config_path, 'r', encoding='utf8') as file:  
        config = yaml.safe_load(file)  
    return config 

# Main execution  
if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='Convert an Excel taxonomy to RDF format and validate it using a SHACL API.')  
    parser.add_argument('-c', '--config', type=str, required=True, help='Path to the config.yaml file.')  
    args = parser.parse_args() 
    config = load_config(args.config) 

    setup_logging(config['logfile'])
    try:  
        excel_to_rdf(config)  
    except Exception as e:  
        logging.info(f"An error occurred: {e}")