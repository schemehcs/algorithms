from pqdict import pqdict
from .graph import WGraph


def init_graph(G, s):
    ss = G.vertex_map[s]
    for v in G.vertices:
        v.p = None
        if v is ss:
            v.d = 0
        else:
            v.d = float("inf")


def relax(G, u, v):
    if v.d > u.d + G.weights[u, v]:
        v.d = u.d + G.weights[u, v]
        v.p = u


# constraint: all edges must be positive
def dijkstra(G, s):
    pq = pqdict()
    init_graph(G, s)
    for v in G.vertices:
        pq.additem(v, v.d)
    while pq:
        (u, dist) = pq.popitem()
        u.d = dist
        for e in G.adjacency_edges[u]:
            if e.v in pq:
                if e.relax():
                    pq[e.v] = e.v.d


def bellman_ford(G, s):
    init_graph(G, s)
    for _ in range(len(G.vertices) - 1):
        for e in G.edges:
            e.relax()
    for e in G.edges:
        if e.v.d > e.u.d + e.w:
            return False
    return True


if __name__ == "__main__":
    G = WGraph(
        ["s", "t", "x", "z", "y"],
        [
            ("s", "t", 3),
            ("s", "y", 5),
            ("t", "x", 6),
            ("t", "y", 2),
            ("x", "z", 2),
            ("z", "x", 7),
            ("z", "s", 3),
            ("y", "z", 6),
            ("y", "x", 4),
            ("y", "t", 1),
        ],
    )
    bellman_ford(G, "s")
    for v in G.vertices:
        print("{}, {}, {}".format(v.key, v.d, v.p and v.p.key))
