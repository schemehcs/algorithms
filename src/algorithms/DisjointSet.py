"""class DisjointSet:
def __init__(self, n):
    self.ls = [i for i in range(n)]

def union(self, x, y):
    if x < y:
        self.ls[y] = x
    else:
        self.ls[x] = y

def find(self, x):
    while x != self.ls[x]:
        x = self.ls[x]
    return x

def dump(self):
    d = dict()
    for i in range(len(self.ls)):
        s = self.find(i)
        if not d.get(s):
            d[s] = []
        d[s].append(i)
    return list(d.values())"""


class Node:
    def __init__(self, key):
        self.key = key
        self.rank = 0
        self.p = self


class DisjointSet:
    def __init__(self, keys):
        self.kn = dict()
        for k in keys:
            self.kn[k] = Node(k)

    def union(self, ka, kb):
        a = self.find(ka)
        b = self.find(kb)
        if a.rank > b.rank:
            b.p = a
        else:
            a.p = b
            if a.rank == b.rank:
                b.rank += 1

    def find(self, ka):
        return self._find(self.kn[ka])

    def _find(self, a):
        if a is not a.p:
            a.p = self._find(a.p)
        return a.p


if __name__ == "__main__":
    s = DisjointSet(["a", "b", "c", "d"])
    s.union("a", "b")
    s.union("b", "d")
    if s.find("a") is s.find("b"):
        print("a, b unioned")
    else:
        print("a, b not union")
    if s.find("c") is s.find("d"):
        print("c, d unioned")
    else:
        print("c, d not unioned")
