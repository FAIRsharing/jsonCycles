from requests import get
import json
from jsonCycles.graphCycles import Graph


class SchemaKey:
    """ Simple class that provides the attributes we need to iterate over
    """
    ref = "$ref"
    items = "items"
    properties = "properties"
    definitions = 'definitions'
    pattern_properties = "patternProperties"
    sub_patterns = ['anyOf', 'oneOf', 'allOf']


class SchemaResolver:
    """ A class that relies on multiprocessing to load all schemas in memory in order to
    build the graph

    :param schema: URL or path to the schema
    :type schema: str
    :param file_type: the type of str pointing to the schema (URL or PATH)
    :type file_type: str
    """

    def __init__(self, schema, file_type):

        self.file_type = file_type.upper()  # URL or PATH
        self.main_schema_name = self._get_name(schema)  # Get the name of the main schema
        self.base_url = self._get_base_url(schema)  # get the base URL to retrieve IDs
        self.schema = schema

        self.output = {}
        self.main_schema = {}
        self.schemas = []
        self.raw_cycles = []

    def resolve_network(self):
        if self.file_type == 'URL':
            self.main_schema = self._get_schema_from_url(self.schema)
        elif self.file_type == 'PATH':
            self.main_schema = self._get_schema_from_file(self.schema)

        references = self._find_references(self.main_schema)
        self.output[self.main_schema_name] = references
        self._get_schemas(references)

    def set_resolved_schemas(self, resolved_network):
        """

        :param resolved_network: a dictionary of all schemas in the network (keys)
        and their references (values)
        :return:
        """
        self.output = resolved_network

    @staticmethod
    def _get_schema_from_url(schema_url):
        try:
            return json.loads(get(schema_url).text)
        except Exception:
            raise Exception('Please verify your URL or your schema')

    @staticmethod
    def _get_schema_from_file(schema_path):
        with open(schema_path, "r") as schemaFile:
            schema = json.load(schemaFile)
        schemaFile.close()
        return schema

    def _get_schemas(self, schema_locations):
        processes = []

        for schema in schema_locations:
            if schema not in self.output.keys():
                processes.append(self.base_url + '/' + schema)

        sub_schemas = []
        if len(processes) > 0:

            for url in processes:
                sub_schema = ""
                if self.file_type == 'URL':
                    sub_schema = self._get_schema_from_url(url)
                elif self.file_type == 'PATH':
                    sub_schema = self._get_schema_from_file(url)
                sub_schemas.append(sub_schema)

            for sub_schema in sub_schemas:
                sub_schema_name = self._get_name(sub_schema['id'])
                local_references = self._find_references(sub_schema)
                self.output[sub_schema_name] = local_references
                self._get_schemas(local_references)

    def _find_references(self, schema):
        schemas_to_load = []

        if SchemaKey.properties in schema:
            for k, val in schema[SchemaKey.properties].items():
                loader = self._find_references(val)
                if len(loader) > 0:
                    for schema in loader:
                        if schema not in schemas_to_load:
                            schemas_to_load.append(schema)

        for pattern in SchemaKey.sub_patterns:
            if pattern in schema:
                for val in schema[pattern]:
                    loader = self._find_references(val)
                    if len(loader) > 0:
                        for schema in loader:
                            if schema not in schemas_to_load:
                                schemas_to_load.append(schema)

        if SchemaKey.items in schema:
            loader = self._find_references(schema['items'])
            if len(loader) > 0:
                for schema in loader:
                    if schema not in schemas_to_load:
                        schemas_to_load.append(schema)

        # TODO: handle ['definitions']

        if SchemaKey.ref in schema and not schema[SchemaKey.ref].startswith('#'):
            schemas_to_load.append(schema['$ref'].replace('#', ''))

        return schemas_to_load

    @staticmethod
    def _get_name(schema_url):
        """ Extract the item name from it's URL
        :param schema_url: the URL of the schema
        :return name: the name of the schema (eg: 'item_schema.json')
        """
        return schema_url.split("/")[-1].replace("#", '')

    @staticmethod
    def _get_base_url(schema_url):
        return '/'.join(schema_url.split("/")[:-1])

    def schemas_to_graph(self):
        vertices = len(self.output)
        graph = Graph(vertices)

        for node in self.output.keys():
            x = list(self.output.keys()).index(node)
            for node_neighbour in self.output[node]:
                y = list(self.output.keys()).index(node_neighbour)
                graph.add_edge(x, y)

        self.raw_cycles = graph.get_cycles()
        # return graph.get_cycles()
