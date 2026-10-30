from collections import deque
from enum import Enum, auto
from functools import total_ordering


class Color(Enum):
    WHITE = auto()
    GREY = auto()
    BLACK = auto()


class Vertex:
    # O(1) time.
    def __init__(self, key):
        self.key = key
        self.reset()

    # O(1) time.
    def reset(self):
        self.color = Color.WHITE
        self.d = None
        self.f = None
        self.p = None

    def __repr__(self) -> str:
        return "({}:c={}, d={}, f={}, p={})".format(
            self.key, self.color, self.d, self.f, self.p
        )


class Graph:
    # O(V + E) time and space.
    def __init__(self, vertices, edges):
        self.vertex_map = dict()
        self.vertices = set()
        self.edges = edges
        self.adjacency = dict()
        for vk in vertices:
            vv = Vertex(vk)
            self.vertex_map[vk] = vv
            self.vertices.add(vv)
            self.adjacency[vv] = set()
        for uk, vk in edges:
            u = self.vertex_map[uk]
            v = self.vertex_map[vk]
            self.adjacency[u].add(v)

    # O(V) time.
    def reset(self):
        for v in self.vertices:
            v.reset()

    # O(V + E) time and space.
    def transpose(self):
        return Graph(
            self.vertex_map,
            [(v, u) for (u, v) in self.edges],
        )


@total_ordering
class Edge:
    # O(1) time.
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    # O(1) time.
    def relax(self):
        if self.v.d > self.u.d + self.w:
            self.v.d = self.u.d + self.w
            self.v.p = self.u
            return True
        return False

    def __repr__(self) -> str:
        return f"({self.u.key}, {self.v.key}, {self.w})"

    # 1. Let total_ordering sort by weight for sorted in Kruskal and heapq in Prim.
    def __lt__(self, other):
        return self.w < other.w

    # 2. Edges are equal only when source, destination, and weight match.
    # For undirected graphs with both directions in the adjacency lists, strict
    # comparison is still the safest choice.
    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return (self.u, self.v, self.w) == (other.u, other.v, other.w)

    # 3. Implement __hash__ to match __eq__ so Edge instances are hashable.
    def __hash__(self):
        return hash((self.u, self.v, self.w))


class WGraph:
    # O(V^2 + E) time and O(V^2 + E) space, including the adjacency matrix.
    def __init__(self, vertices, edges):
        self.vertex_map = dict()
        self.vertex_sequence = dict()
        self.edge_map = dict()
        self.vertices = list()
        self.edges = list()
        self.adjacency = dict()
        self.adjacency_edges = dict()
        self.weights = dict()
        v_cnt = len(vertices)
        self.matrix = [[float("inf")] * v_cnt for _ in range(v_cnt)]
        for vi, vk in enumerate(vertices):
            vv = Vertex(vk)
            self.vertex_map[vk] = vv
            self.vertices.append(vv)
            self.adjacency[vv] = set()
            self.adjacency_edges[vv] = set()
            self.vertex_sequence[vk] = vi
            self.matrix[vi][vi] = 0
        for uk, vk, w in edges:
            u = self.vertex_map[uk]
            v = self.vertex_map[vk]
            self.adjacency[u].add(v)
            edge = Edge(u, v, w)
            self.edges.append(edge)
            self.adjacency_edges[u].add(edge)
            if (u, v) not in self.edge_map or w < self.edge_map[(u, v)].w:
                self.edge_map[(u, v)] = edge
            self.weights[u, v] = min(self.weights.get((u, v), w), w)
            row = self.vertex_sequence[uk]
            column = self.vertex_sequence[vk]
            self.matrix[row][column] = min(self.matrix[row][column], w)

    # O(V) time.
    def reset(self):
        for v in self.vertices:
            v.reset()


# O(V + E) time and space; computes unweighted shortest-path distances.
def bfs(G, s):
    G.reset()
    s.color = Color.GREY
    s.d = 0
    s.p = None
    # process s
    Q = deque()
    Q.append(s)
    while Q:
        u = Q.popleft()
        # process u
        for v in G.adjacency[u]:
            if v.color == Color.WHITE:
                v.color = Color.GREY
                v.d = u.d + 1
                v.p = u
                # process v
                Q.append(v)
        u.color = Color.BLACK


class Counter:
    # O(1) time.
    def __init__(self, start=0):
        self.counter = start

    # O(1) time.
    def next(self):
        c = self.counter
        self.counter += 1
        return c


# O(V + E) time and O(V) recursion space.
def dfs(G, vertices=None):
    G.reset()
    counter = Counter(0)
    circular = False
    vertex_list = G.vertices if vertices is None else vertices
    for u in vertex_list:
        if u.color == Color.WHITE:
            circular = dfs_visit(G, u, counter) or circular
    return circular


# O(V + E) time and O(V) recursion space.
def dfs_visit(G, u, counter):
    u.d = counter.next()
    u.color = Color.GREY
    # process u
    circular = False
    for v in G.adjacency[u]:
        if v.color == Color.WHITE:
            v.p = u
            circular = dfs_visit(G, v, counter) or circular
        elif v.color == Color.GREY:
            circular = True
    u.color = Color.BLACK
    u.f = counter.next()
    return circular


# O(V + E) time and O(V) extra space.
def dfs_iter(G):
    G.reset()
    counter = Counter(0)
    has_cycle = False
    for u in G.vertices:
        if u.color == Color.WHITE:
            has_cycle = dfs_visit_iter(G, u, counter) or has_cycle
    return has_cycle


# O(V + E) time and O(V) extra space.
def dfs_visit_iter(G, u, counter):
    u.d = counter.next()
    u.color = Color.GREY
    stack = [(u, iter(G.adjacency[u]))]
    has_cycle = False
    while stack:
        vertex, neighbors = stack[-1]
        try:
            neighbor = next(neighbors)
        except StopIteration:
            vertex.color = Color.BLACK
            vertex.f = counter.next()
            stack.pop()
            continue

        if neighbor.color is Color.WHITE:
            neighbor.p = vertex
            neighbor.d = counter.next()
            neighbor.color = Color.GREY
            stack.append((neighbor, iter(G.adjacency[neighbor])))
        elif neighbor.color is Color.GREY:
            has_cycle = True
    return has_cycle


# O(V log V + E) time due to sorting finish times; O(V) extra space.
def topological_sort(G):
    if dfs(G):
        return None
    return list(sorted(G.vertices, key=lambda u: u.f, reverse=True))


if __name__ == "__main__":
    G = Graph(
        vertices=["v", "s", "w", "q", "t", "x", "z", "y", "r", "u"],
        edges=[
            ("s", "v"),
            ("v", "w"),
            ("w", "s"),
            ("q", "s"),
            ("q", "w"),
            ("q", "t"),
            ("t", "y"),
            ("t", "x"),
            ("x", "z"),
            ("z", "x"),
            ("y", "q"),
            ("r", "y"),
            ("r", "u"),
            ("u", "y"),
        ],
    )

    G2 = Graph(
        vertices=[
            "undershorts",
            "socks",
            "pants",
            "shoes",
            "watch",
            "belt",
            "shirt",
            "tie",
            "jacket",
        ],
        edges=[
            ("undershorts", "shoes"),
            ("undershorts", "pants"),
            ("pants", "belt"),
            ("pants", "shoes"),
            ("socks", "shoes"),
            ("shirt", "belt"),
            ("shirt", "tie"),
            ("tie", "jacket"),
            ("belt", "jacket"),
        ],
    )

    ts = topological_sort(G2)
    if ts:
        for t in ts:
            print(t)
