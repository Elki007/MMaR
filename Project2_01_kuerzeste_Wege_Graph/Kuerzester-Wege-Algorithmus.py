from Graph_v04 import Graph

def bereche_den_weg(Graph,start, destination):
    G = Graph
    V = dict() # all nodes
    a = start
    U = dict() # visited
    d = dict() # shortest path
    p = dict() # shortest path to node U = p[u]

    # fill V with all nodes
    # set all distances to infinity
    for each in G.nodes_list:
        V[each] = each
        d[each] = 9999

    d[a]=0
    p[a]=0

    print(d)

    # while there is unvisited node
    while len(U)!=len(V):
        d_min= 9999
        v_chosen= -1
        for v in V:
            if v not in U:
                if d[v]<d_min:
                    d_min=d[v]
                    v_chosen=v
        if v_chosen !=-1:
            U[v_chosen]=v_chosen
            #print("v_chosen",v_chosen)
            if len(U)%100==0 or len(V)==len(U):
                print("len(V):",len(V)," len(U):",len(U))
            for u in G.out_edges(v_chosen):
                if u not in U:
                    if d[u]>d[v_chosen]+ G.get_distance(v_chosen,u):
                        d[u]=d[v_chosen]+ G.get_distance(v_chosen,u)
                        p[u]=(p[v_chosen],u)
    return p[destination]

G = Graph("nodes.csv", "edges.csv")
start = G.nodes_list[5]
destination = G.nodes_list[55] #59442
print("Ausgehende: ",G.out_edges(start))
print(start, " ->", destination)

"""gm=0
for g in range(len(G.nodes_list)):
    if G.nodes_list[g] == 4766326273:
        gm = g

print("gm: ",gm)
G.test_print_node_number(4766326273)"""

print("\n\n\n### Algorithm ###\n\n\n")
print(bereche_den_weg(G,start,destination))

