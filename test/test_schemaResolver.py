import unittest
import multiprocessing
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
        self.assertTrue(self.SchemaKey.sub_patterns ==['anyOf', 'oneOf', 'allOf'])


class SchemaResolverTestCase(unittest.TestCase):

    def setUp(self):
        schema = "https://datatagsuite.github.io/schema/resolvedNetwork.json"
        self.SchemaResolver = SchemaResolver(schema, 'url')

    def test_constructor(self):
        cpu = multiprocessing.cpu_count()
        cpu_count = cpu if cpu < 2 else cpu - 1
        self.assertTrue(self.SchemaResolver.cpu_count == cpu_count)
        self.assertTrue(self.SchemaResolver.file_type == 'URL')
        self.assertTrue(self.SchemaResolver.main_schema_name == 'resolvedNetwork.json')
        self.assertTrue(self.SchemaResolver.base_url == 'https://datatagsuite.github.io/schema')
        self.assertTrue(self.SchemaResolver.schema == "https://datatagsuite.github.io/schema/resolvedNetwork.json")

    def test_resolve_network(self):
        self.SchemaResolver.resolve_network()
        print(self.SchemaResolver.output)
        self.assertTrue(self.SchemaResolver == 123)