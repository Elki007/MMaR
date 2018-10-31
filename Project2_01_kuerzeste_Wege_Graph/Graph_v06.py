"""
6th version of class Graph
main reason:
- dijkstra method improved with:
    - # 5.1 -> Distance to destination now matters
    - distances will be calculated just before # 5.4.1.2
"""

import csv
import numpy as np
import bisect
import math as m


class Graph:
    """
    Maybe to much lists/dictionaries?
    Maybe time to think about a class Node?
        - long-/lat-coordinates,
        - screen-coordinates,
        - neighbour nodes with an edge connection
    """
    def __init__(self, node_list='', edge_list=''):
        self.nodes_list = []  # just the sorted numbers of nodes
        self.edges_list = []  # list like "[start_node, end_node]"

        self.nodes_dict = {}  # dict like: "node_number: [x-coord, y-coord, node_value]"
        self.edges_out_dict = {}  # dict like: "start_node: [end_node1, end_node2,...]"
        self.edges_in_dict = {}  # edges_in_dict only makes sense, if there're one way edges?

        # contains only connected nodes
        self.adjacency_matrix_nodes = {}  # dict like: "(node_one, node_two) : [1, distance, edge_value]"

        # counts every node and every edge
        self.count_nodes = 0
        self.count_edges = 0
        # self.count_edges = sum(len(edge) for edge in self.edges_out_dict.values())

        # Biggest and smallest longitude/latitude
        self.smallest_lat, self.biggest_lat = 100, -100
        self.smallest_long, self.biggest_long = 200, -200

        # only reads from files and creates dicts and a list, if a node_list is given
        if node_list != '':
            self.init_nodes_dict_and_list(node_list)
            if edge_list != '':
                self.init_edges_dict(edge_list)

        # dijkstra variables
        self.seen = {}
        self.visited = {}
        self.previous = {}
        self.distances = {}
        self.distances_to_destination = {}
        self.path = []

    """
    Initializes nodes and edges of an .csv-file
    """

    # reads csv-file and creates dictionary and a list
    # list will consist of sorted numbers of nodes
    # key of dict = number of node
    # value of dict = list with x- and y-coordinate
    # e.g.: 1234: [1.234, 5.123]
    def init_nodes_dict_and_list(self, node_list, value=0):
        with open(node_list, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.set_new_node(int(row[0]), float(row[1]), float(row[2]), value)

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
    def get_all_nodes_in_list(self):
        return self.nodes_list

    def get_node_number_from_list(self, node_index):
        return self.nodes_list[node_index]

    # returns coordinates in a list [longitude, latitude]
    def get_coordinates(self, node_number):
        return [self.nodes_dict[node_number][0], self.nodes_dict[node_number][1]]

    # get_number_of_nodes
    def num_nodes(self):
        return self.count_nodes

    # get_number_of_edges
    def num_edges(self):
        return self.count_edges

    # gets distance if there's an edge (already calculated
    def get_distance_of_edge(self, node_one, node_two):
        return self.adjacency_matrix_nodes[(node_one, node_two)][1]

    # if "edge" is a list element with [start node, end node]
    # get_start_node
    @staticmethod
    def from_node(edge):
        return edge[0]

    # if "edge" is a list element with [start node, end node]
    # get_end_node
    @staticmethod
    def to_node(edge):
        return edge[1]

    # if "node" is an number of one node
    # get_out_going_edges
    def out_edges(self, node):
        return self.edges_out_dict[node]

    # if "node" is an element from self.nodes it returns a list with edges that goes to node
    # get_in_going_edges
    def in_edges(self, node):
        return self.edges_in_dict[node]

    def set_node_value(self, number, value):
        self.nodes_dict[number].append(value)

    # get_node_value
    def node_value(self, number):
        return self.nodes_dict[number][2]

    def get_smallest_latitude(self):
        return self.smallest_lat

    def get_biggest_latitude(self):
        return self.biggest_lat

    def get_smallest_longitude(self):
        return self.smallest_long

    def get_biggest_longitude(self):
        return self.biggest_long

    """
    Create new nodes or edges
    """

    # Proves if node number already exists and creates one
    # Creates:
    # - new Element for nodes_dict
    # - new Element in sorted nodes_list
    # - adds 1 to count_nodes
    def set_new_node(self, number, longitude, latitude, value, overwrite=False):
        if (number in self.nodes_dict) and not overwrite:
            print("This Node already exists and won't be overwritten.")
        else:
            self.nodes_dict[number] = [longitude, latitude]
            self.set_node_value(number, value)
            bisect.insort(self.nodes_list, number)
            self.count_nodes += 1

            if self.smallest_lat > latitude:
                self.smallest_lat = latitude
            if self.biggest_lat < latitude:
                self.biggest_lat = latitude
            if self.smallest_long > longitude:
                self.smallest_long = longitude
            if self.biggest_long < longitude:
                self.biggest_long = longitude

    # GETS: number of two nodes
    # Creates:
    # - new Element for edges_list
    # - new Element for edges_out_dict if key is new
    # - appends another sorted Element for edges_out dict if key exists
    # - same for edges_in_dict
    # - new Element for adjacency_matrix_element
    # - adds 1 to count_edges
    def set_new_edge(self, start_node, end_node, value=0):
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
        self.add_adjacency_matrix_element(start_node, end_node, value)
        self.count_edges += 1

    # node[Längengrad, Breitengrad] / [longitude, latitude]
    def calculate_distance(self, node_one, node_two):
        if node_one == node_two:
            return 0

        # calculation "inspired" by script of Frank Fischer
        beta_one, lambda_one = self.nodes_dict[node_one][1], self.nodes_dict[node_one][0]
        beta_two, lambda_two = self.nodes_dict[node_two][1], self.nodes_dict[node_two][0]

        # Translation to radian measure (Bogenmaß)
        beta_one, lambda_one = beta_one * m.pi / 180, lambda_one * m.pi / 180
        beta_two, lambda_two = beta_two * m.pi / 180, lambda_two * m.pi / 180

        step_one = m.sin(beta_one) * m.sin(beta_two)
        step_two = m.cos(beta_one) * m.cos(beta_two) * m.cos(lambda_one - lambda_two)
        #print(step_one + step_two)
        distance = 6378.388 * m.acos(step_one + step_two)

        """
        # Alternative calculation
        x = (lambda_two - lambda_one) * m.cos((beta_one + beta_two) / 2)
        y = (beta_two - beta_one)
        distance = m.sqrt(x * x + y * y) * radius_earth
        """
        return distance

    def add_adjacency_matrix_element(self, start_node, end_node, value):
        tmp_distance = self.calculate_distance(start_node, end_node)
        self.adjacency_matrix_nodes[(start_node, end_node)] = [1, tmp_distance]
        self.adjacency_matrix_nodes[(end_node, start_node)] = [1, tmp_distance]
        self.set_edge_value(start_node, end_node, value)

    def set_edge_value(self, start_node, end_node, value):
        self.adjacency_matrix_nodes[(start_node, end_node)].append(value)
        self.adjacency_matrix_nodes[(end_node, start_node)].append(value)

    # get_edge_value
    # edge = (start_node, end_node)
    def edge_value(self, edge):
        return self.adjacency_matrix_nodes[edge][2]

    def test_print_index(self, index):
        tmp_node = self.nodes_list[index]
        self.test_print_node_number(tmp_node)

    def test_print_node_number(self, node_number):
        # results will be displayed after indent_value spaces
        indent_value = 30
        print("Nummer vom Beispielknoten:".ljust(indent_value), node_number)
        print("Koordinaten vom Knoten:".ljust(indent_value), self.nodes_dict[node_number][:2])
        print("Ausgehende Kanten führen zu:".ljust(indent_value), self.out_edges(node_number))
        print("Eingehende Kanten kommen von:".ljust(indent_value), self.in_edges(node_number), "\n\n")

    # Dijkstra algorithm
    def berechne_den_weg(self, start, destination):
        ### Algorithm ###
        # 1.
        self.seen = {}  # seen, not visited
        self.visited = {}  # visited
        # 2.
        self.previous = {node: None for node in self.get_all_nodes_in_list()}  # previous node
        # 3.
        self.distances = {node: "unendlich" for node in self.get_all_nodes_in_list()}  # distance
        # 4.
        self.seen[start] = start
        self.distances[start] = 0
        # new for change in 5.1.
        self.distances_to_destination[start] = self.calculate_distance(start, destination)
        # 5.
        # print("Seen:", seen)
        while self.seen:
            # 5.1.
            # for each in seen find that one, which has the smallest (distance + distance to destination)
            u_chosen = min(self.seen, key=lambda node: self.distances[node] + self.distances_to_destination[node])

            # 5.2
            self.seen.pop(u_chosen)
            self.visited[u_chosen] = u_chosen

            # 5.3.
            if u_chosen == destination:
                break

            # 5.4
            for node in self.out_edges(u_chosen):
                if node not in self.visited:
                    # 5.4.1
                    if node not in self.seen:
                        # print("out_edge not seen: ", node)
                        # 5.4.1.1
                        self.seen[node] = node
                        # new for change in 5.1.
                        self.distances_to_destination[node] = self.calculate_distance(node, destination)
                        # 5.4.1.2
                        self.distances[node] = self.distances[u_chosen] + self.get_distance_of_edge(u_chosen, node)
                        # 5.4.1.3
                        self.previous[node] = u_chosen
                    # 5.4.2
                    elif (self.distances[u_chosen] + self.get_distance_of_edge(u_chosen, node)) < self.distances[node]:
                        # print("out_edge seen: ", node)
                        # 5.4.2.1
                        self.distances[node] = self.distances[u_chosen] + self.get_distance_of_edge(u_chosen, node)
                        # 5.4.2.2
                        self.previous[node] = u_chosen
        # 6.
        if self.distances[destination] == "unendlich":
            print("no path found")
            return -1
        # 7.
        self.path = []
        u = destination
        self.path.append(u)
        # 8.
        while u != start:
            self.path.append(self.previous[u])
            u = self.previous[u]

        self.path.reverse()
        #print(P)
        #print("Anzahl der Knoten:", len(P))
        return self.path


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
