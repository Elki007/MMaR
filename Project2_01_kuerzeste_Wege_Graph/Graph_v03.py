"""
3rd version of class Graph
main reason: start creating other attributes to nodes and edges
"""

import csv
import numpy as np
import bisect
import math as m


class Graph:

    def __init__(self, node_list='', edge_list=''):
        self.nodes_list = []  # just the sorted numbers of nodes
        self.edges_list = []  # list like "[start_node, end_node]"

        self.nodes_dict = {}  # dict like: "node_number: [x-coord, y-coord]"
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
    # list will consist of sorted numbers of nodes
    # key of dict = number of node
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

    def get_distance(self, node_one, node_two):
        if (node_one, node_two) in self.adjacency_matrix_nodes:
            return self.adjacency_matrix_nodes[node_one, node_two][1]
        else:
            print("No edge between those two nodes.")
            return 0

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

    # if "node" is an number of one node
    # get_out_going_edges
    def out_edges(self, node):
        """
        :param node: single node number
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

    # Proves if node number already exists and creates one
    # Creates:
    # - new Element for nodes_dict
    # - new Element in sorted nodes_list
    # - adds 1 to count_nodes
    def set_new_node(self, number, x_coordinate, y_coordinate, overwrite=False):
        if (number in self.nodes_dict) and not overwrite:
            print("This Node already exists and won't be overwritten.")
        else:
            self.nodes_dict[number] = [x_coordinate, y_coordinate]
            bisect.insort(self.nodes_list, number)
            self.count_nodes += 1

    # GETS: number of two nodes
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

    # node[Längengrad, Breitengrad]
    def calculate_distance(self, node_one, node_two):
        beta_one, lambda_one = self.nodes_dict[node_one][1], self.nodes_dict[node_one][0]
        beta_two, lambda_two = self.nodes_dict[node_two][1], self.nodes_dict[node_two][0]

        # Translation to radian measure (Bogenmaß)
        beta_one, lambda_one = beta_one * m.pi / 180, lambda_one * m.pi / 180
        beta_two, lambda_two = beta_two * m.pi / 180, lambda_two * m.pi / 180

        step_one = m.sin(beta_one) * m.sin(beta_two)
        step_two = m.cos(beta_one) * m.cos(beta_two) * m.cos(lambda_one - lambda_two)
        distance = 6378.388 * m.acos(step_one + step_two)

        """
        # Alternative calculation
        x = (lambda_two - lambda_one) * m.cos((beta_one + beta_two) / 2)
        y = (beta_two - beta_one)
        distance = m.sqrt(x * x + y * y) * radius_earth
        """
        return distance

    def add_adjacency_matrix_element(self, start_node, end_node):
        tmp_distance = self.calculate_distance(start_node, end_node)
        self.adjacency_matrix_nodes[(start_node, end_node)] = [1, tmp_distance]
        self.adjacency_matrix_nodes[(end_node, start_node)] = [1, tmp_distance]

    def test_print_index(self, index):
        tmp_node = self.nodes_list[index]
        self.test_print_node_number(tmp_node)

    def test_print_node_number(self, node_number):
        print("Index vom Beispielknoten:".ljust(30), node_number)
        print("Koordinaten vom Knoten:".ljust(30), self.nodes_dict[node_number])
        print("Ausgehende Kanten führen zu:".ljust(30), self.out_edges(node_number))
        print("Eingehende Kanten kommen von:".ljust(30), self.in_edges(node_number), "\n\n")


"""
Test area
"""

"""
tmp = Graph("nodes.csv", "edges.csv")

print("Anzahl der Knoten:".ljust(30), tmp.num_nodes())
print("Anzahl der Kanten:".ljust(30), tmp.num_edges(), '\n')

tmp.test_print_index(60)
tmp.test_print_node_number(2388159)

print("Distanz von den 2 Punkten:".ljust(30), tmp.get_distance(tmp.nodes_list[60], 2388159))

print("Anzahl der Adjazenz-Elemente:", len(tmp.adjacency_matrix_nodes))
"""
