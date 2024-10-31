import argparse

import ifcopenshell
from BrickAPI import BrickAPI
from collections import defaultdict
from utils import *

# predefined brick classes for given ifc classes
IFC_BRICK = {'IfcWallStandardCase': 'Wall',
             'IfcBuildingStorey': 'Level',
             'IfcFurnishingElement': 'Furniture'}


def get_relationships(model):
    """
    get brick relationships for an ifc model
    :param model: ifc model
    :return: dictionary with structure {source_id: {relationship: [target_id1, target_id2, ...], ...}, ...}
    """
    rels = {}
    for rel in model.by_type('IfcRelationship'):
        # relationship delineation depends on type
        rel_type = rel.is_a()
        if rel_type in IFC_REL_NAMING:
            scheme = IFC_REL_NAMING[rel_type]
            source_info = getattr(rel, scheme['source']).get_info()
            source_id = source_info['type'] + str(source_info['id'])

            targets = getattr(rel, scheme['target'])
            brick_type = scheme['type']

            # add source to relationship dictionary if not already exists
            if source_id not in rels:
                rels[source_id] = defaultdict(set)  # set of targets defined by rel type

            if targets is None:
                continue

            # if multiple targets, add all. else add one
            if not isinstance(targets, ifcopenshell.entity_instance):
                for target in targets:
                    target_info = target.get_info()
                    target_id = target_info['type'] + str(target_info['id'])
                    rels[source_id][brick_type].add(target_id)
            else:
                target_info = targets.get_info()
                target_id = target_info['type'] + str(target_info['id'])
                rels[source_id][brick_type].add(target_id)

    return rels


def entity_relationship_map(model):
    """
    extract entity and relationship information for a given ifc model
    :param model: ifc model
    :return: dictionary with entities and relationships.
        {'entities': [{<entity info>, "properties": {<properties>}, ...],
         'relationships': {source_id: {relationship: [target_id1, target_id2, ...], ...}, ...}}
    """
    data = {
        'entities': [],
        'relationships': None
    }

    # map spaces
    for ifc_object in model.by_type('IfcSpatialStructureElement'):
        entity = ifc_object.get_info()
        entity["properties"] = get_properties(ifc_object)
        data["entities"].append(entity)

    # map physical elements
    for ifc_object in model.by_type('IfcElement'):
        entity = ifc_object.get_info()
        entity["properties"] = get_properties(ifc_object)
        data["entities"].append(entity)

    # map relationships
    relationships = get_relationships(model)
    data['relationships'] = relationships

    return data


def main(ifc_file, namespace, write_path):
    # open model and extract information for brick mapping
    model = ifcopenshell.open(ifc_file)
    brick_data = entity_relationship_map(model)

    # create rdf graph using brick ontology
    rdf_graph = BrickAPI(namespace)
    for entity in brick_data['entities']:
        # add nodes
        ent_id = entity['type'] + str(entity['id'])
        brick_class = get_brick_from_ifc_type(entity['type'], IFC_BRICK, 'BuildingElement', True)
        rdf_graph.add_node(ent_id, brick_class)

        # add properties
        for property_name, props in entity['properties'].items():
            brick_prop = get_brick_from_ifc_type(property_name, class_ont=False, strict=True)
            if brick_prop is None:
                continue

            props_id = property_name + str(props['id'])

            # property node (property: [brick:value brick:unit])
            rdf_graph.add_node(props_id, 'Quantity')
            rdf_graph.add_property(props_id, props['value'], 'value')
            rdf_graph.add_property(props_id, props['Unit'], 'hasUnit')

            # connect entity to property
            rdf_graph.add_edge(ent_id, props_id, brick_prop)

    # add relationships between site elements
    for source, relationship in brick_data['relationships'].items():
        for relationship_type, targets in relationship.items():
            for target in targets:
                rdf_graph.add_edge(source, target, relationship_type)

    rdf_graph.write_ttl(write_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process IFC files and generate RDF graphs.")
    parser.add_argument('--ifc_file', type=str, required=True, help='Path to the IFC file')
    parser.add_argument('--namespace', type=str, required=True, help='Namespace for the RDF graph')
    parser.add_argument('--write_path', type=str, required=True, help='Path to save the output TTL file')

    args = parser.parse_args()

    main(args.ifc_file, args.namespace, args.write_path)
