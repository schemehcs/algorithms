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

if __name__ == '__main__':
    ds = DisjointSet(10)
    ds.union(1, 2)
    ds.union(3, 4)
    ds.union(4, 8)
    ds.union(2, 9)

    print(ds.dump())






