import heapq
from functools import total_ordering

from .disjointset import DisjointSet
from .graph import Color, WGraph


# O(E log E) time and O(V + E) space.
def kruskal(WG):
    ds = DisjointSet(WG.vertices)
    sorted_edges = sorted(WG.edges)
    edges = []
    for e in sorted_edges:
        if ds.find(e.u) is not ds.find(e.v):
            ds.union(e.u, e.v)
            edges.append(e)
    return edges


@total_ordering
class PriorityNode:
    def __init__(self, e):
        self.e = e

    def __eq__(self, other):
        return self.e.w == other.e.w

    def __lt__(self, other):
        return self.e.w < other.e.w


# O(E log E) time and O(E) space with a binary heap.
def prim(WG):
    WG.reset()
    if not WG.vertices:
        return set()
    heap = []
    s = WG.vertices[0]
    v_cnt = 1
    s.color = Color.BLACK
    edges = set()
    for e in WG.adjacency_edges[s]:
        heapq.heappush(heap, PriorityNode(e))
    while heap:
        n = heapq.heappop(heap)
        if n.e.v.color == Color.WHITE:
            n.e.v.color = Color.BLACK
            edges.add(n.e)
            v_cnt += 1
            if v_cnt == len(WG.vertices):
                break
            for ve in WG.adjacency_edges[n.e.v]:
                if ve.v.color == Color.WHITE:
                    heapq.heappush(heap, PriorityNode(ve))
    return edges


if __name__ == "__main__":
    G = WGraph(
        vertices=["a", "b", "c", "d", "e", "f", "g", "h", "i"],
        edges=[
            ("a", "b", 4),
            ("b", "c", 8),
            ("c", "d", 7),
            ("d", "e", 9),
            ("e", "f", 10),
            ("f", "g", 2),
            ("g", "h", 1),
            ("h", "a", 8),
            ("b", "h", 11),
            ("h", "i", 7),
            ("i", "c", 2),
            ("i", "g", 6),
            ("c", "f", 4),
            ("d", "f", 14),
        ],
    )
    edges = kruskal(G)
    p_edges = prim(G)
    for e in edges:
        print(e)
    print("--------------")
    for e in p_edges:
        print(e)
