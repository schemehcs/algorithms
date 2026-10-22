from enum import Enum, auto


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
        self.Vmap = dict()
        self.V = set()
        self.E = edges
        self.Adj = dict()
        for vk in vertices:
            vv = Vertex(vk)
            self.Vmap[vk] = vv
            self.V.add(vv)
            self.Adj[vv] = set()
        for uk, vk in edges:
            u = self.Vmap[uk]
            v = self.Vmap[vk]
            self.Adj[u].add(v)

    def reset(self):
        for v in self.V:
            v.reset()

    def transpose(self):
        return Graph(self.V, [(v, u) for (u, v) in self.E])


class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def __repr__(self) -> str:
        return "({}, {}, {})".format(self.u.key, self.v.key, self.w)


class WGraph:
    def __init__(self, vertices, edges):
        self.Vmap = dict()
        self.Emap = dict()
        self.V = set()
        self.E = list()
        self.Adj = dict()
        for vk in vertices:
            vv = Vertex(vk)
            self.Vmap[vk] = vv
            self.V.add(vv)
            self.Adj[vv] = set()
        for uk, vk, w in edges:
            u = self.Vmap[uk]
            v = self.Vmap[vk]
            self.Adj[u].add(v)
            edge = Edge(u, v, w)
            self.E.append(edge)
            self.Emap[(u, v)] = edge

    def reset(self):
        for v in self.V:
            v.reset()


# time O(V + E)
# attributes
## 1. find shortest path from s to any other vertices
## 2. bfs tree rooted at s
def bfs(G, s):
    from collections import deque

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
        for v in G.Adj[u]:
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
    V = vertices or G.V
    for u in V:
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
    for v in G.Adj[u]:
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
    for u in G.V:
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
            for v in G.Adj[u]:
                if v.color == Color.WHITE:
                    v.p = u
                    stack.append(v)
        else:
            u.color = Color.BLACK
            u.f = counter.next()


def topological_sort(G):
    if dfs(G):
        return None
    return list(sorted(G.V, key=lambda u: u.f, reverse=True))


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
