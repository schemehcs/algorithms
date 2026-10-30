from collections import deque
from enum import Enum, auto
from functools import total_ordering


class Color(Enum):
    WHITE = auto()
    GREY = auto()
    BLACK = auto()


class Vertex:
    def __init__(self, key):
        self.key = key
        self.reset()

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

    def reset(self):
        for v in self.vertices:
            v.reset()

    def transpose(self):
        return Graph(self.vertices, [(v, u) for (u, v) in self.edges])


@total_ordering
class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def relax(self):
        if self.v.d > self.u.d + self.w:
            self.v.d = self.u.d + self.w
            self.v.p = self.u
            return True
        return False

    def __repr__(self) -> str:
        return f"({self.u.key}, {self.v.key}, {self.w})"

    # 1. 让 total_ordering 依据权重进行大小排序（完美适配 Kruskal 的 sorted 和 Prim 的 heapq）
    def __lt__(self, other):
        return self.w < other.w

    # 2. 只有当起点、终点和权重完全一致时，才算同一条边（有向边逻辑）
    # 如果是无向边，且邻接表 AdjE 里存了双向，直接严格对比也最安全
    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return (self.u, self.v, self.w) == (other.u, other.v, other.w)

    # 3. 伴随严格的 __eq__，实现对应的 __hash__，彻底解决 Unhashable 问题
    def __hash__(self):
        return hash((self.u, self.v, self.w))


class WGraph:
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
            self.edge_map[(u, v)] = edge
            self.weights[u, v] = w
            self.matrix[self.vertex_sequence[uk]][self.vertex_sequence[vk]] = w

    def reset(self):
        for v in self.vertices:
            v.reset()


# time O(V + E)
# attributes
## 1. find shortest path from s to any other vertices
## 2. bfs tree rooted at s
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
    def __init__(self, start=0):
        self.counter = start

    def next(self):
        c = self.counter
        self.counter += 1
        return c


def dfs(G, vertices=None):
    G.reset()
    counter = Counter(0)
    circular = False
    vertex_list = vertices or G.vertices
    for u in vertex_list:
        if u.color == Color.WHITE:
            circular = dfs_visit(G, u, counter) or circular
            if circular:
                print("True here")
    return circular


def dfs_visit(G, u, counter):
    u.d = counter.next()
    u.color = Color.GREY
    # process u
    circular = False
    for v in G.adjacency[u]:
        if v.color == Color.WHITE:
            v.p = u
            dfs_visit(G, v, counter)
        elif v.color == Color.GREY:
            circular = True
    u.color = Color.BLACK
    u.f = counter.next()
    return circular


def dfs_iter(G):
    G.reset()
    counter = Counter(0)
    for u in G.vertices:
        if u.color == Color.WHITE:
            dfs_visit_iter(G, u, counter)


def dfs_visit_iter(G, u, counter):
    stack = []
    stack.append(u)
    while stack:
        u = stack.pop()
        if u.color == Color.WHITE:
            u.d = counter.next()
            u.color = Color.GREY
            stack.append(u)
            for v in G.adjacency[u]:
                if v.color == Color.WHITE:
                    v.p = u
                    stack.append(v)
        else:
            u.color = Color.BLACK
            u.f = counter.next()


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
