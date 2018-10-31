"""
2nd version of class Graph
main reason: Using dictionaries instead of arrays
"""

import csv
import numpy as np
import bisect


class Graph:

    def __init__(self, node_list='', edge_list=''):
        self.nodes_list = []  # just the sorted indexes of nodes
        self.edges_list = []  # list like "[start_node, end_node]"

        self.nodes_dict = {}  # dict like: "index: [x-coord, y-coord]"
        self.edges_out_dict = {}  # dict like: "start_node: [end_node1, end_node2,...]"
        self.edges_in_dict = {}  # edges_in_dict only makes sense, if there're one way edges?

        self.adjacency_matrix_nodes = {}

        # counts every node and every edge
        self.count_nodes = 0
        self.count_edges = 0
        # self.count_edges = sum(len(edge) for edge in self.edges_out_dict.values())

        # only reads from files and creates dicts and a list, if a node_list is given
        if node_list != '':
            self.init_nodes_dict_and_list(node_list)
            if edge_list != '':
                self.init_edges_dict(edge_list)

    """
    Initializes nodes and edges of an .csv-file
    """

    # reads csv-file and creates dictionary and a list
    # list will consist of sorted indexes of nodes
    # key of dict = index number of node
    # value of dict = list with x- and y-coordinate
    # e.g.: 1234: [1.234, 5.123]
    def init_nodes_dict_and_list(self, node_list):
        with open(node_list, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.set_new_node(int(row[0]), float(row[1]), float(row[2]))

    # reads csv-file and creates 2 dictionaries (in- and outgoing edges) and a list
    # list: [start_node, end_node]
    # outgoing edges:
    # key of dict = start-node
    # value of dict = all end-nodes
    # e.g.: 1234: [5324, 1233, 3252]
    def init_edges_dict(self, edge_list):
        with open(edge_list, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                self.set_new_edge(int(row[0]), int(row[1]))

    """
    getter and setter
    """
    # get_number_of_nodes
    def num_nodes(self):
        return self.count_nodes

    # get_number_of_edges
    def num_edges(self):
        return self.count_edges

    # if "edge" is a list element with [start node, end node]
    # get_start_node
    @staticmethod
    def from_node(edge):
        return edge[0]

    # if "edge" is a list element with [start node, end node]
    # get_target_node
    @staticmethod
    def to_node(edge):
        return edge[1]

    # if "node" is an index of one node
    # get_out_going_edges
    def out_edges(self, node):
        """
        :param node: single node index
        :return: list of edges
        """
        return self.edges_out_dict[node]

    # if "node" is an element from self.nodes it returns a list with edges that goes to node
    # get_in_going_edges
    def in_edges(self, node):
        """
        :param node: single node from self.nodes
        :return: list of edges
        """
        return self.edges_in_dict[node]

    """
    Create new nodes or edges
    """

    # Proves if node index already exists and creates one
    # Creates:
    # - new Element for nodes_dict
    # - new Element in sorted nodes_list
    # - adds 1 to count_nodes
    def set_new_node(self, index, x_coordinate, y_coordinate, overwrite=False):
        if (index in self.nodes_dict) and not overwrite:
            print("This Node already exists and won't be overwritten.")
        else:
            self.nodes_dict[index] = [x_coordinate, y_coordinate]
            bisect.insort(self.nodes_list, index)
            self.count_nodes += 1

    # Creates:
    # - new Element for edges_list
    # - new Element for edges_out_dict if key is new
    # - appends another sorted Element for edges_out dict if key exists
    # - same for edges_in_dict
    # - new Element for adjacency_matrix_element
    # - adds 1 to count_edges
    def set_new_edge(self, start_node, end_node):
        self.edges_list.append([start_node, end_node])

        # TODO: Is it important to check, if edges are already in there?
        # if key exists, just append another end node, else create a start node
        if start_node in self.edges_out_dict:
            bisect.insort(self.edges_out_dict[start_node], end_node)
        else:
            self.edges_out_dict[start_node] = [end_node]
        # do the same the other way around
        if end_node in self.edges_in_dict:
            bisect.insort(self.edges_in_dict[end_node], start_node)
        else:
            self.edges_in_dict[end_node] = [start_node]

        # add the edge to the adjacency matrix and add 1 to the amount of edges
        self.add_adjacency_matrix_element(start_node, end_node)
        self.count_edges += 1

    def add_adjacency_matrix_element(self, start_node, end_node):
        self.adjacency_matrix_nodes[(start_node, end_node)] = 1
        self.adjacency_matrix_nodes[(end_node, start_node)] = 1

    def test_print(self, index):
        tmp_node = self.nodes_list[index]

        print("Index vom Beispielknoten:".ljust(30), tmp_node)
        print("Koordinaten vom Knoten:".ljust(30), self.nodes_dict[tmp_node])
        print("Ausgehende Kanten führen zu:".ljust(30), self.out_edges(tmp_node))
        print("Eingehende Kanten kommen von:".ljust(30), self.in_edges(tmp_node), "\n\n")


"""
Test area
"""

tmp = Graph("nodes.csv", "edges.csv")

print("Anzahl der Knoten:".ljust(30), tmp.num_nodes())
print("Anzahl der Kanten:".ljust(30), tmp.num_edges(), '\n')

tmp.test_print(110)
tmp.test_print(111)

print("Anzahl der Adjazenz-Elemente:", len(tmp.adjacency_matrix_nodes))
