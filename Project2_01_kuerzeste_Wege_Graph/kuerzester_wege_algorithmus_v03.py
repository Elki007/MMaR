"""
Variablennamen und Struktur orientiert sich an den Hinweisen vom Skript, Aufgabe 4: Kürzester-Wege-Algorithmus
"""

from Graph_v04 import Graph


def berechne_den_weg(Graph, start, destination):
    ### Algorithm ###
    # 1.
    seen = {}  # seen, not visited
    visited = {}  # visited
    # 2.
    previous = {node: None for node in Graph.get_all_nodes_in_list()}  # previous node
    # 3.
    distances = {node: "unendlich" for node in Graph.get_all_nodes_in_list()}  # distance
    # 4.
    seen[start] = start
    distances[start] = 0
    # 5.
    # print("Seen:", seen)
    while seen:
        # 5.1.
        # for each in seen find that one, which has the smallest distance
        u_chosen = min(seen, key=lambda node: distances[node])

        # 5.2
        seen.pop(u_chosen)
        visited[u_chosen] = u_chosen

        # 5.3.
        if u_chosen == destination:
            break

        # 5.4
        for node in Graph.out_edges(u_chosen):
            if node not in visited:
                # 5.4.1
                if node not in seen:
                    # print("out_edge not seen: ", node)
                    # 5.4.1.1
                    seen[node] = node
                    # 5.4.1.2
                    distances[node] = distances[u_chosen] + Graph.get_distance_of_edge(u_chosen, node)
                    # 5.4.1.3
                    previous[node] = u_chosen
                # 5.4.2
                elif (distances[u_chosen] + Graph.get_distance_of_edge(u_chosen, node)) < distances[node]:
                    # print("out_edge seen: ", node)
                    # 5.4.2.1
                    distances[node] = distances[u_chosen] + Graph.calculate_distance(u_chosen, node)
                    # 5.4.2.2
                    previous[node] = u_chosen
    # 6.
    if distances[destination] == "unendlich":
        print("no path found")
        return -1
    # 7.
    P = []
    u = destination
    P.append(u)
    # 8.
    while u != start:
        P.append(previous[u])
        u = previous[u]

    P.reverse()
    #print(P)
    #print("Anzahl der Knoten:", len(P))
    return P

"""
G = Graph("nodes.csv", "edges.csv")
start = G.get_node_number_from_list(5)
destination = G.get_node_number_from_list(7)  #59442

print("Ausgehende: ", G.out_edges(start))
print(start, " ->", destination)
"""


# deactivated
"""gm=0
for g in range(len(G.nodes_list)):
    if G.nodes_list[g] == 4766326273:
        gm = g

print("gm: ",gm)
G.test_print_node_number(4766326273)"""

"""
print("\n\n\n### Algorithm ###\n\n\n")
berechne_den_weg(G, start, destination)
"""
