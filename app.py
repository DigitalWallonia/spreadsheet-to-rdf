import argparse  
from tqdm import tqdm
from utils.transformer import excel_to_rdf
import yaml  


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

    try:  
        excel_to_rdf(config['input']['default_file'], config['transformation']['namespace'], config['output']['default_file'], config['output']['default_format'], config['validation']['server'], config['transformation']['rules']['changes'][0]["changelabel"])  
    except Exception as e:  
        print(f"An error occurred: {e}")