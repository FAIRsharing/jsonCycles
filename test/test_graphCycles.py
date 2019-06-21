from jsonCycles.graphCycles import Graph
import unittest


class GraphTestCase(unittest.TestCase):

    def setUp(self):
        self.graph = Graph(4)

    def test_get_cycles(self):
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)
        self.graph.add_edge(2, 0)
        self.graph.add_edge(3, 0)
        self.graph.add_edge(1, 0)
        expected_output = [[0, 1, 2, 3, 0], [0, 1, 2, 0], [0, 1, 0]]
        self.assertTrue(expected_output == self.graph.get_cycles())

    def test_get_cycles_reverse(self):
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)
        expected_output = False
        self.assertTrue(self.graph.get_cycles() == expected_output)

    def test_is_cyclic_runner(self):
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)
        self.graph.add_edge(3, 0)
        expected_output = [[0, 1, 2, 3, 0]]

        visited = [False] * 4
        rec_stack = [False] * 4
        path = [0]
        self.graph.is_cyclic_runner(0, visited, rec_stack, path)
        self.assertTrue(expected_output == self.graph.results)
