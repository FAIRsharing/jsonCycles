import unittest
import os
import json
from jsonCycles.schemaResolver import SchemaResolver
from jsonCycles.schemaResolver import SchemaKey


class SchemaKeyTestCase(unittest.TestCase):

    def setUp(self):
        self.SchemaKey = SchemaKey

    def test_constructor(self):
        self.assertTrue(self.SchemaKey.ref == "$ref")
        self.assertTrue(self.SchemaKey.items == "items")
        self.assertTrue(self.SchemaKey.properties == "properties")
        self.assertTrue(self.SchemaKey.definitions == 'definitions')
        self.assertTrue(self.SchemaKey.pattern_properties == "patternProperties")
        self.assertTrue(self.SchemaKey.sub_patterns == ['anyOf', 'oneOf', 'allOf'])


class SchemaResolverTestCase4Path(unittest.TestCase):

    def setUp(self):
        schema = os.path.join(os.path.dirname(__file__), "schemas/dats/study_schema.json")
        self.SchemaResolver = SchemaResolver(schema, 'path')

    def test_constructor(self):
        self.assertTrue(self.SchemaResolver.file_type == 'PATH')
        self.assertTrue(self.SchemaResolver.main_schema_name == 'study_schema.json')

    def test_resolve_network(self):
        resolved_network_path = os.path.join(os.path.dirname(__file__),
                                             'schemas/resolvedNetwork.json')
        with open(resolved_network_path) as file:
            expected_resolved_network = json.load(file)
        file.close()
        self.SchemaResolver.resolve_network()
        self.assertTrue(self.SchemaResolver.output == expected_resolved_network)

    def test_schemas_to_graph(self):
        self.SchemaResolver.resolve_network()
        raw_cycles = self.SchemaResolver.schemas_to_graph()
        expected_cycles = [
            [0, 10, 11, 11],
            [0, 10, 17, 18, 17],
            [0, 10, 17, 10],
            [0, 10, 24, 25, 10],
            [0, 10, 26, 27, 26],
            [0, 10, 26, 28, 29, 28],
            [0, 10, 26, 28, 26],
            [0, 10, 26, 10],
            [0, 10, 30, 32, 10],
            [0, 10, 10]]
        self.assertTrue(raw_cycles == expected_cycles)


class SchemaResolverTestCase4URL(unittest.TestCase):

    def setUp(self):
        schema = "https://datatagsuite.github.io/schema/study_schema.json"
        self.SchemaResolver = SchemaResolver(schema, 'URL')

    def test_schemas_to_graph(self):
        self.SchemaResolver.resolve_network()
        raw_cycles = self.SchemaResolver.schemas_to_graph()
        expected_cycles = [
            [0, 10, 11, 11],
            [0, 10, 17, 18, 17],
            [0, 10, 17, 10],
            [0, 10, 24, 25, 10],
            [0, 10, 26, 27, 26],
            [0, 10, 26, 28, 29, 28],
            [0, 10, 26, 28, 26],
            [0, 10, 26, 10],
            [0, 10, 30, 32, 10],
            [0, 10, 10]]
        self.assertTrue(raw_cycles == expected_cycles)
