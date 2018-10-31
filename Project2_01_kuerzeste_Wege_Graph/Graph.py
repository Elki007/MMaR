import csv
import numpy as np


class Graph:

    def __init__(self, node_list = '', edge_list = ''):
        self.nodes = []
        self.edges = []

        if node_list != '':
            self.init_nodes(node_list)
            if edge_list != '':
                self.init_edges(edge_list)

        self.nodes.sort()
        self.edges.sort()

        self.count_nodes = len(self.nodes)
        self.count_edges = len(self.edges)

    """
    Initializes nodes and edges of an .csv-file
    """

    # reads csv-file and saves the number and floats to self.nodes in a list of lists
    def init_nodes(self, node_list):
        with open(node_list, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # TODO: vlt. schneller mit numpy-arrays oder tuples (beides?)
                self.nodes.append([int(row[0]), float(row[1]), float(row[2])])

    # reads csv-file and saves the start and end node to self.edges in a list of lists
    def init_edges(self, edge_list):
        with open(edge_list, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                # TODO: vlt. schneller mit numpy-arrays oder tuples (beides?)
                self.edges.append([int(row[0]), int(row[1])])

    """
    getter and setter
    """
    # TODO: Renaming getter and setter

    def num_nodes(self):
        return self.count_nodes

    def num_edges(self):
        return self.count_edges

    # if "edge" is the list with start and end node
    @staticmethod
    def from_node(edge):
        return edge[0]

    # if "edge" is the list with start and end node
    @staticmethod
    def to_node(edge):
        return edge[1]

    # if "node" is an element from self.nodes it returns a list with edges that start from node
    def out_edges(self, node):
        """
        :param node: single node from self.nodes
        :return: list of edges
        """
        out_going = []
        for i in range(self.num_edges()):
            if self.edges[i][0] == node[0]:
                out_going.append(self.edges[i])
        return out_going

    # if "node" is an element from self.nodes it returns a list with edges that goes to node
    def in_edges(self, node):
        """
        :param node: single node from self.nodes
        :return: list of edges
        """
        in_going = []
        for i in range(self.num_edges()):
            if self.edges[i][1] == node[0]:
                in_going.append(self.edges[i])
        return in_going

    def set_new_node(self, number, x_coordinate, y_coordinate):
        # TODO: Testing, if node or position is already taken
        self.nodes.append([number, x_coordinate, y_coordinate])
        self.count_nodes += 1

    def set_new_edge(self, start_node, end_node):
        # TODO: Testing, if edge already exists
        self.edges.append([start_node, end_node])
        self.count_edges += 1

    def create_adjacency_matrix(self):
        #matrix = [[0 for i in range(self.num_nodes())] for j in range(self.num_nodes())]
        matrix = np.zeros((self.num_nodes(), self.num_nodes()), dtype=int)
        print(matrix)
        for i in range(10):
            connection = self.out_edges(self.nodes[i])
            print(connection)
            for edge in connection:
                for j in range(self.num_nodes()):
                    if edge[1] == self.nodes[j][0]:
                        matrix[i][j] = 1
                        break
        print(matrix.sum())

    def create_adjacency_matrix2(self):
        #matrix = [[0 for i in range(self.num_nodes())] for j in range(self.num_nodes())]
        matrix = np.zeros((self.num_nodes(), self.num_nodes()), dtype=np.bool)
        print(matrix)
        for i in range(10):
            connection = self.out_edges(self.nodes[i])
            #print(connection)
            for edge in connection:
                #index = self.nodes.index([edge[1]])
                #print(index)
                for j in range(self.num_nodes()):
                    if edge[1] == self.nodes[j][0]:
                        matrix[i][j] = 1
                        break
        #print(matrix.sum())




"""
Test area
"""

tmp_test = Graph("nodes.csv", "edges.csv")

print(tmp_test.nodes[0])

tmp_test_edges = tmp_test.out_edges(tmp_test.nodes[11112])
print(len(tmp_test_edges))

tmp_test.create_adjacency_matrix2()