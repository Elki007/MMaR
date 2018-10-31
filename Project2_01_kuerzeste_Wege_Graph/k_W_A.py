from Graph_v04 import Graph

def bereche_den_weg(Graph, start, destination):
    ### Algorithm ###
    # 1.
    Seen = dict()     # seen, not visited
    Visited = dict()    # visited
    # 2.
    p = dict() # previous node
    # 3.
    d = dict() # distanse
    # 4.
    Seen[start] = start
    d[start] = 0
    # 5.
    print(Seen)
    while len(Seen)!=0:
        # for each in seen find one, which is close to destination
        d_min=99999
        u_chosen=-1
        for each in Seen:
            if d[each] < d_min:
                u_chosen=each
        print("u_chosen: ",u_chosen)
        Seen.pop(u_chosen)
        Visited[u_chosen] = u_chosen
        if u_chosen == destination:
            break
        for n in Graph.out_edges(u_chosen):
            if n not in Visited:
                if n not in Seen:
                    print("out_edge not seen: ", n)
                    Seen[n] = n
                    d[n] = d[u_chosen] + Graph.calculate_distance(u_chosen, n)
                    p[n] = u_chosen
                else:
                    print("out_edge seen: ", n)
                    d[n] = d[u_chosen] + Graph.calculate_distance(u_chosen, n)
                    p[n] = u_chosen
    if destination not in d:
        print("no path found")
    else:
        P = []
        u = destination
        P.append(u)
        while u != start:
            print(p[u])
            P.append(p[u])
            u = p[u]
        print(P)
        for i in range(len(P)//2):
            P[i],P[len(P)-1-i]=P[len(P)-1-i],P[i]
        print(P)
        print("Anzahl der Knoten:", len(P))
        return P

G = Graph("nodes.csv", "edges.csv")
start = G.nodes_list[5]
destination = G.nodes_list[7] #59442
print("Ausgehende: ",G.out_edges(start))
print(start, " ->", destination)

"""gm=0
for g in range(len(G.nodes_list)):
    if G.nodes_list[g] == 4766326273:
        gm = g

print("gm: ",gm)
G.test_print_node_number(4766326273)"""

print("\n\n\n### Algorithm ###\n\n\n")
bereche_den_weg(G,start,destination)

