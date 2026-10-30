class Node:
    # O(1) time.
    def __init__(self, key):
        self.key = key
        self.rank = 0
        self.p = self


class DisjointSet:
    # O(n) time and space for n keys.
    # O(1) time.
    def __init__(self, keys):
        self.kn = dict()
        for k in keys:
            self.kn[k] = Node(k)

    # Amortized O(alpha(n)) time with path compression and union by rank.
    def union(self, ka, kb):
        a = self.find(ka)
        b = self.find(kb)
        if a is b:
            return
        if a.rank > b.rank:
            b.p = a
        else:
            a.p = b
            if a.rank == b.rank:
                b.rank += 1

    # Amortized O(alpha(n)) time with path compression and union by rank.
    def find(self, ka):
        return self._find(self.kn[ka])

    # O(alpha(n)) amortized time with path compression and union by rank.
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
