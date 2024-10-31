import pandas as pd
import os


IFC_REL_NAMING = {
        'IfcRelContainedInSpatialStructure':
            {'source': 'RelatingStructure', 'target': 'RelatedElements', 'type': 'hasPart'},
        'IfcRelFillsElement':
            {'source': 'RelatingOpeningElement', 'target': 'RelatedBuildingElement', 'type': 'hasPart'},
        'IfcRelSequence':
            {'source': 'RelatingProcess', 'target': 'RelatedProcess', 'type': 'feeds'},
        'IfcRelSpaceBoundary':
            {'source': 'RelatingSpace', 'target': 'RelatedBuildingElement', 'type': 'hasPart'},
        'IfcRelAdheresToElement':
            {'source': 'RelatingElement', 'target': 'RelatedSurfaceFeatures', 'type': 'hasPart'},
        'IfcRelAggregates':
            {'source': 'RelatingObject', 'target': 'RelatedObjects', 'type': 'hasPart'},
        'IfcRelNests':
            {'source': 'RelatingObject', 'target': 'RelatedObjects', 'type': 'hasPart'},
        'IfcRelProjectsElement':
            {'source': 'RelatingElement', 'target': 'RelatedFeatureElement', 'type': 'hasPart'},
        'IfcRelVoidsElement':
            {'source': 'RelatingBuildingElement', 'target': 'RelatedOpeningElement', 'type': 'hasPart'}
    }
    
BRICK_CLASSES = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'brick_ontologies', 'brick_ontology_classes.csv'))
BRICK_PROPS = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'brick_ontologies', 'brick_ontology_properties.csv'))


def extract_quantities(ifc_property):
    """
    get property dictionary for ifc property of type quantity
    :param ifc_property: property to extract
    :return: property dictionary. {<property_name>: {<property_info>}} (includes unit and value)
    """
    out = {}
    for quantity in ifc_property.Quantities:
        out[quantity.Name] = quantity.get_info()
        value_key = [k for k in out[quantity.Name].keys() if 'value' in k.lower()][0]

        out[quantity.Name]['value'] = out[quantity.Name][value_key]
        del out[quantity.Name][value_key]
    return out


def extract_single_value(ifc_property):
    """
    get property dictionary for ifc property of type single value
    :param ifc_property: property to extract
    :return: property dictionary. {<property_name>: {<property_info>}} (includes unit and value)
    """
    out = {ifc_property.Name: ifc_property.get_info()}
    del out[ifc_property.Name]['NominalValue']

    out[ifc_property.Name]['value'] = ifc_property.NominalValue.wrappedValue
    return out


def map_properties(ifc_property):
    """
    maps an ifc (qunatitative) property to a dictionary
    :param property: ifc property to extract data from
    :return: dictionary of properties with structure {name: value, ...}
    """
    property_map = {}

    # set of properties
    if ifc_property.is_a('IfcPropertySet'):
        for set_property in ifc_property.HasProperties:
            property_map.update(map_properties(set_property))

    # only one property to map
    elif ifc_property.is_a('IfcPropertySingleValue'):
        value = ifc_property.NominalValue.wrappedValue
        if type(value) == float or type(value) == int: # make sure value is numeric
            property_map.update(extract_single_value(ifc_property))

    # set of quantities
    elif ifc_property.is_a('IfcElementQuantity'):
        property_map.update(extract_quantities(ifc_property))

    else:
        return

    return property_map


def get_properties(ifc_object):
    """
    gets a dictionary of all properties for a given ifc object
    :param ifc_object: ifc object to get properties from
    :return: dictionary of properties with structure {name: value, ...}
    """
    properties = {}
    for definition in ifc_object.IsDefinedBy:
        if definition.is_a('IfcRelDefinesByProperties'):
            properties.update(map_properties(definition.RelatingPropertyDefinition))

    return properties


def replace_all(string, to_replace, replacement):
    """
    replace all given characters in a string
    :param string: string to replace characters from
    :param to_replace: characters to replace
    :param replacement: character to replace with
    :return: string with characters replaced
    """
    for rep in to_replace:
        string = string.replace(rep, replacement)

    return string


def get_brick_from_ifc_type(ifc_type, defined_map={}, base_case=None, class_ont=True, strict=True):
    """
    attempts to get the associated brick class from an ifc type. checks in three steps:
        1. use pre-defined brick type if it is given
        2. use matched brick type
            a. if strict, only match when ifc type matches a brick type exactly
            b. else match when a brick type is contained in an ifc type (ex: wall in wallStandardCase)
        3. use catchall case if given
    :param ifc_type (str):      type to map
    :param defined_map (dict):  predefined mapping of {<ifc_type>: <brick_type>}. default is None
    :param base_case (str):     brick type to assign if no other brick type is found. default is None
    :param class_ont (boolean): whether to use brick class ontology. if false, brick properties will be used.
                                default is True.
    :param strict (boolean):    if match step is hit, whether to match exactly. default is True
    :return: str representation of matched brick type
    """
    # if ifc type is already defined
    if ifc_type in defined_map:
        return defined_map[ifc_type]

    # if ifc type maps exactly to brick ontology
    brick_names = BRICK_CLASSES['name'] if class_ont else BRICK_PROPS['name']
    for name in brick_names:
        clean_name = replace_all(name.lower(),' _.', '')
        clean_ifc = ifc_type.lower().replace('ifc', '')
        if (strict and clean_name == clean_ifc) or (not strict and clean_name in clean_ifc):
            return name

    return base_case
