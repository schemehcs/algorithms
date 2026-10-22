from Graph import WGraph
from DisjointSet import DisjointSet

def kruskal(WG):
    ds = DisjointSet(WG.V)
    sorted_edges = sorted(WG.E, key=lambda e: e.w)
    edges = []
    for e in sorted_edges:
        if not ds.find(e.u) is ds.find(e.v):
            ds.union(e.u, e.v)
            edges.append(e)
    return edges
        
if __name__ == '__main__':
    G = WGraph(vertices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
               edges=[
                   ('a', 'b', 4),
                   ('b', 'c', 8),
                   ('c', 'd', 7),
                   ('d', 'e', 9),
                   ('e', 'f', 10),
                   ('f', 'g', 2),
                   ('g', 'h', 1),
                   ('h', 'a', 8),
                   ('b', 'h', 11),
                   ('h', 'i', 7),
                   ('i', 'c', 2),
                   ('i', 'g', 6),
                   ('c', 'f', 4),
                   ('d', 'f', 14)
               ]
               )
    edges = kruskal(G)
    for e in edges:
        print(e)

