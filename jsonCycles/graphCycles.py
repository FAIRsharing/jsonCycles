from collections import defaultdict
from copy import copy


class Graph:
    """ The Graph class will run the searches and hold the results in self.results
    Inspired by https://www.geeksforgeeks.org/detect-cycle-in-a-graph/

    :param vertices: the number of vertices in the graph
    :type vertices: int
    :return:
    """

    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices
        self.results = []

    def add_edge(self, u, v):
        """ Adds an edge between two vertices

        :param u: node at the origin of the edge
        :type u: int
        :param v: target node of the edge
        :type v: int
        :return:
        """
        self.graph[u].append(v)

    def is_cyclic_runner(self, v, visited, rec_stack, path):
        """ Looks through the graph starting with node v

        :param v: the node to start with
        :type v: int
        :param visited: the stack of visited nodes
        :type visited: list
        :param rec_stack: the recursive stack to find circularity
        :type rec_stack: list
        :param path: the current path of node leading to circularity
        :param path: str
        """
        # Mark current node as visited and adds to recursion stack
        visited[v] = True
        rec_stack[v] = True
        found = []

        # For each neighbour
        for neighbour in self.graph[v]:

            # Get the current local path and add the neighbour to it
            local_path = copy(path)
            local_path.append(neighbour)

            if not visited[neighbour]:
                self.is_cyclic_runner(neighbour, visited, rec_stack, local_path)
            elif rec_stack[neighbour]:
                # Found when the neighbour has been visited and in recStack
                found = local_path

        # The node needs to be popped out the recursion stack before function ends
        rec_stack[v] = False
        if len(found) > 0:
            self.results.append(found)

    # Returns true if graph is cyclic else false
    def get_cycles(self):
        """ Method to run the search for each entry point in the graph

        :return: False or result list
        """
        visited = [False] * self.V
        rec_stack = [False] * self.V

        for node in range(self.V):
            current_path = [node]

            # If node hasn't already been visited
            if not visited[node]:
                self.is_cyclic_runner(node, visited, rec_stack, current_path)

        if len(self.results) > 0:
            return self.results
        return False
