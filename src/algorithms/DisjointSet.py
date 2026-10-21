class DisjointSet:
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
        return list(d.values())

class Node:
    def __init__(self, key):
        self.key = key
        self.rank = 0
        self.p = self

def union(a, b):
    if a.rank > b.rank:
        b.p = a
    else:
        a.p = b
        if a.rank == b.rank:
            b.rank += 1

def find(n):
    if n is not n.p:
        n.p = find(n.p)
    return n.p

if __name__ == '__main__':
    ds = DisjointSet(10)
    ds.union(1, 2)
    ds.union(3, 4)
    ds.union(4, 8)
    ds.union(2, 9)
    print(ds.dump())






