import multiprocessing
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
    :param cpu: the number of threads to use. All by default
    :type cpu: int
    """

    def __init__(self, schema, file_type, cpu=multiprocessing.cpu_count()):

        self.cpu_count = cpu
        if self.cpu_count >= 2:
            self.cpu_count -= 1
        self.main_schema = {}
        self.schemas = []
        self.file_type = file_type.upper()
        self.main_schema_name = self.get_name(schema)
        self.base_url = self.get_base_url(schema)
        self.output = {}

        if self.file_type == "URL":
            self.main_schema = self._get_schema_from_url(schema)
            references = self.find_references(self.main_schema)
            self.output[self.main_schema_name] = references
            self._get_schemas_from_url(references)

        if self.file_type == "PATH":
            self.main_schema = self._get_schema_from_file(schema)
            references = self.find_references(self.main_schema)
            self.output[self.main_schema_name] = references
            self._get_schemas_from_url(references)
            # TODO: extend to resolve also from files

    @staticmethod
    def _get_schema_from_url(schema_url):
        try:
            return json.loads(get(schema_url).text)
        except Exception as e:
            raise Exception(e)

    def _get_schemas_from_url(self, schema_locations):
        processes = []

        for schema in schema_locations:
            if schema not in self.output.keys():
                processes.append(self.base_url + '/' + schema)

        results = []
        if len(processes) > 0:
            if self.file_type == 'URL':
                p = multiprocessing.Pool(processes=self.cpu_count)
                for url in processes:
                    pp = p.apply_async(self._get_schema_from_url, [url])
                    results.append(pp)
                sub_schemas = [pp.get() for pp in results]
            if self.file_type == 'PATH':
                for url in processes:
                    pp = self._get_schema_from_file(url)
                    results.append(pp)
                sub_schemas = results

            for sub_schema in sub_schemas:
                sub_schema_name = self.get_name(sub_schema['id'])
                local_references = self.find_references(sub_schema)
                self.output[sub_schema_name] = local_references
                self._get_schemas_from_url(local_references)

    @staticmethod
    def _get_schema_from_file(schema_path):
        try:
            with open(schema_path, "r") as schemaFile:
                return json.load(schemaFile)
        except Exception as e:
            raise Exception(e)

    def find_references(self, schema):
        schemas_to_load = []

        if SchemaKey.properties in schema:
            for k, val in schema[SchemaKey.properties].items():
                loader = self.find_references(val)
                if len(loader) > 0:
                    for schema in loader:
                        if schema not in schemas_to_load:
                            schemas_to_load.append(schema)

        for pattern in SchemaKey.sub_patterns:
            if pattern in schema:
                for val in schema[pattern]:
                    loader = self.find_references(val)
                    if len(loader) > 0:
                        for schema in loader:
                            if schema not in schemas_to_load:
                                schemas_to_load.append(schema)

        if SchemaKey.items in schema:
            loader = self.find_references(schema['items'])
            if len(loader) > 0:
                for schema in loader:
                    if schema not in schemas_to_load:
                        schemas_to_load.append(schema)

        # TODO: handle ['definitions']

        if SchemaKey.ref in schema and not schema[SchemaKey.ref].startswith('#'):
            schemas_to_load.append(schema['$ref'].replace('#', ''))

        return schemas_to_load

    @staticmethod
    def get_name(schema_url):
        """ Extract the item name from it's URL
        :param schema_url: the URL of the schema
        :return name: the name of the schema (eg: 'item_schema.json')
        """
        return schema_url.split("/")[-1].replace("#", '')

    @staticmethod
    def get_base_url(schema_url):
        return '/'.join(schema_url.split("/")[:-1])

    def schemas_to_graph(self):
        vertices = len(self.output)
        graph = Graph(vertices)

        for node in self.output.keys():
            x = list(self.output.keys()).index(node)
            for node_neighbour in self.output[node]:
                y = list(self.output.keys()).index(node_neighbour)
                graph.add_edge(x, y)

        return graph.get_cycles()


if __name__ == '__main__':
    schema_URL = "https://datatagsuite.github.io/schema/study_schema.json"
    schema_paths = 'schemas/dats/study_schema.json'

    # test_from_url = SchemaResolver(schema_paths, 'path')
    schema_from_url = SchemaResolver(schema_URL, 'url')
    raw_cycles = schema_from_url.schemas_to_graph()
    item_positions = list(schema_from_url.output.keys())
    for cycle in raw_cycles:
        local_cycle = []
        for item in cycle:
            local_cycle.append(item_positions[item])
        print(local_cycle)
