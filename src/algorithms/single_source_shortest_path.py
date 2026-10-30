from pqdict import pqdict
from .graph import WGraph


# O(V) time and O(1) extra space.
def init_graph(G, s):
    ss = G.vertex_map[s]
    for v in G.vertices:
        v.p = None
        if v is ss:
            v.d = 0
        else:
            v.d = float("inf")


# O((V + E) log V) time and O(V) space with an indexed priority queue.
# Requires non-negative edge weights.
def dijkstra(G, s):
    pq = pqdict()
    if any(edge.w < 0 for edge in G.edges):
        raise ValueError("Dijkstra requires non-negative edge weights")
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


# O(VE) time and O(V) extra space.
def bellman_ford(G, s):
    init_graph(G, s)
    for _ in range(len(G.vertices) - 1):
        changed = False
        for e in G.edges:
            changed = e.relax() or changed
        if not changed:
            break
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
