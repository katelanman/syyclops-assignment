from rdflib import RDF, Namespace, Graph, Literal


class BrickAPI:
    def __init__(self, namespace, brick_namespace="https://brickschema.org/schema/Brick#"):
        """
        instantiates rdf graph for a building site
        :param namespace: unique namespace to use for the graph
        :param brick_namespace: brick ontology
        """
        self.g = Graph()

        self.SITE = Namespace(namespace)
        self.BRICK = Namespace(brick_namespace)

        self.add_namespace('bldg', self.SITE)
        self.add_namespace('brick', self.BRICK)

    def add_namespace(self, prefix, namespace):
        """
        bind new namespace to graph
        :param prefix: prefix of namespace
        :param namespace: namespace uri
        :return:
        """
        new_namespace = Namespace(namespace)
        self.g.bind(prefix, new_namespace)

    def get_tag(self, tag):
        """
        returns SPARQL query result for given tag if it exists in the graph
        :param tag: tag to get
        """
        query = "SELECT ?tag WHERE { bldg:" + \
                tag + \
                " rdf:type brick:Tag}"
        return self.g.query(query)

    def add_node(self, node, node_class):
        """
        add graph node
        :param node: node to add
        :param node_class: brick class to assign node
        """
        self.g.add((self.SITE[node], RDF.type, self.BRICK[node_class]))

    def add_tag(self, node, tag):
        """
        add tag to given node
        :param node: node to tag
        :param tag: tag to add
        """
        # add tag to graph if doesn't exist
        if len(self.get_tag(tag)) == 0:
            self.add_node(tag, 'brick:Tag')
        self.g.add((self.SITE[node], self.BRICK.hasTag, self.SITE[tag]))

    def add_edge(self, source, target, type):
        """
        add graph edge
        :param source: source node
        :param target: target node
        :param type: type of relationship
        """
        self.g.add((self.SITE[source], getattr(self.BRICK, type), self.SITE[target]))

    def add_property(self, source, property, type):
        """
        add property to graph node
        :param source: node to add property to
        :param property: property to add
        :param type: type of property
        """
        self.g.add((self.SITE[source], getattr(self.BRICK, type), Literal(property)))

    def write_ttl(self, path_to_write):
        """
        save graph as a turtle file
        :param path_to_write: path to save to
        """
        self.g.serialize(destination=path_to_write, format="ttl")
