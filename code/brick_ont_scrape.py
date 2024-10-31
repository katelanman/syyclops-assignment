import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def remove_deprecated(s, tag, deprecated_class):
    """
    find and remove all ontologies marked as deprecated
    :param s: source html
    :param tag: tag of items to search for deprecated
    :param deprecated_class: class name indicating deprecated
    :return: list of items with tag that are not deprecated
    """
    tagged = s.find_all(tag)
    deprecated = s.find_all(tag, class_=deprecated_class)
    for item in deprecated:
        if item in tagged:
            tagged.remove(item)

    return tagged


def get_ontologies(s):
    """
    get labels and names for all ontologies
    :param s: source html
    :return: dataframe mapping prefixes to class names
    """
    s = remove_deprecated(s, 'a', 'rdf-deprecated')
    labels = [label.text for label in [a.find('span', class_='rdf-iri-prefixlabel') for a in s]]
    names = [name.text for name in [a.find('span', class_='rdf-iri-localname') for a in s]]

    return pd.DataFrame({'labels':labels, 'name':names})


def main():
    """
    gets brick ontology class and property names
    :return: dataframes for class and property names
    """
    # get brick schema ontology documentation
    r = requests.get('https://ontology.brickschema.org/1289125569.html')

    soup = BeautifulSoup(r.content, 'html.parser')
    schema_definitions = soup.find_all('ul', class_='schema-columns')

    # get and save class and property definitions
    classes = get_ontologies(schema_definitions[0])
    properties = get_ontologies(schema_definitions[1])
    
    # Determine the path where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script

    # Create output directory if it doesn't exist
    output_dir = os.path.join(script_dir, '..', 'brick_ontologies')
    os.makedirs(output_dir, exist_ok=True)
    
    classes.to_csv(os.path.join(output_dir, 'brick_ontology_classes.csv'), index=False)
    properties.to_csv(os.path.join(output_dir, 'brick_ontology_properties.csv'), index=False)



if __name__ == "__main__":
    main()
