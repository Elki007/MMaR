from Projekt1_Datenstrukturen_und_kuerzeste_Wege.Graph_v03 import Graph

tmp = Graph("nodes.csv", "edges.csv")

print("Anzahl der Knoten:".ljust(30), tmp.num_nodes())
print("Anzahl der Kanten:".ljust(30), tmp.num_edges(), '\n')

tmp.test_print_index(60)
tmp.test_print_node_number(2388159)

print("Distanz von den 2 Punkten:".ljust(30), tmp.get_distance(tmp.nodes_list[60], 2388159))

print("Anzahl der Adjazenz-Elemente:", len(tmp.adjacency_matrix_nodes))