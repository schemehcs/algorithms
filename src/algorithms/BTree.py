from collections import deque


class Node:
    def __init__(self, t, leaf=True, keys=None, children=None):
        assert t > 1, "node t must be greater than 1"
        self.p = None
        self.t = t
        self.t2 = 2 * t
        self.leaf = leaf
        self.keys = keys or []
        self.children = children or []
        for c in self.children:
            c.p = self

    def n(self):
        return len(self.keys)

    def should_split(self):
        return self.n() == self.t2 - 1

    def split_child(self, i):
        y = self.children[i]
        keys = y.keys[y.t : y.t2]
        if y.leaf:
            children = None
        else:
            children = y.children[y.t : y.t2 + 1]
        z = Node(self.t, y.leaf, keys, children)
        z.p = self
        self.keys.insert(i, y.keys[y.t - 1])
        del y.keys[y.t - 1 :]
        if not y.leaf:
            del y.children[y.t :]
        self.children.insert(i + 1, z)

    # return i where self.keys[i-1] <= k < self.keys[i]
    def search_local(self, k):
        i = self.n() - 1
        while i >= 0 and k < self.keys[i]:
            i -= 1
        return i + 1

    def insert_nonfull(self, k):
        i = self.search_local(k)
        if self.leaf:
            self.keys.insert(i, k)
        else:
            if self.children[i].should_split():
                self.split_child(i)
                if k > self.keys[i]:
                    i += 1
            self.children[i].insert_nonfull(k)

    def min_key(self):
        nd = self
        while not nd.leaf:
            nd = nd.children[0]
        return nd.keys[0]

    def max_key(self):
        nd = self
        while not nd.leaf:
            nd = nd.children[-1]
        return nd.keys[-1]

    def merge_child(self, i):
        y = self.children[i]
        z = self.children[i + 1]
        y.keys.append(self.keys.pop(i))
        y.keys.extend(z.keys)
        if not y.leaf:
            for c in z.children:
                c.p = y
            y.children.extend(z.children)
        del self.children[i + 1]

    def borrow_from_prev(self, i):
        c, s = self.children[i], self.children[i - 1]
        c.keys.insert(0, self.keys[i - 1])
        self.keys[i - 1] = s.keys.pop()
        if not c.leaf:
            ch = s.children.pop()
            ch.p = c
            c.children.insert(0, ch)

    def borrow_from_next(self, i):
        c, s = self.children[i], self.children[i + 1]
        c.keys.append(self.keys[i])
        self.keys[i] = s.keys.pop(0)
        if not c.leaf:
            ch = s.children.pop(0)
            ch.p = c
            c.children.append(ch)

    def fill_child(self, i):
        if i > 0 and self.children[i - 1].n() >= self.t:
            self.borrow_from_prev(i)
            return i
        if i < self.n() and self.children[i + 1].n() >= self.t:
            self.borrow_from_next(i)
            return i
        if i < self.n():
            self.merge_child(i)
            return i
        self.merge_child(i - 1)
        return i - 1

    def delete(self, k):
        i = 0
        while i < self.n() and k > self.keys[i]:
            i += 1
        if i < self.n() and self.keys[i] == k:
            if self.leaf:
                del self.keys[i]
                return True
            y, z = self.children[i], self.children[i + 1]
            if y.n() >= self.t:
                pred = y.max_key()
                self.keys[i] = pred
                return y.delete(pred)
            elif z.n() >= self.t:
                succ = z.min_key()
                self.keys[i] = succ
                return z.delete(succ)
            else:
                self.merge_child(i)
                return self.children[i].delete(k)
        if self.leaf:
            return False
        if self.children[i].n() < self.t:
            i = self.fill_child(i)
        return self.children[i].delete(k)

    def __repr__(self) -> str:
        return "keys:{}".format(self.keys)


class BTree:
    def __init__(self, t):
        assert t > 1, "t must be greater than 1"
        self.t = t
        self.t2 = t * 2
        self.root = Node(t)

    def search(self, k):
        nd = self.root
        while True:
            i = 0
            while i < nd.n() and k > nd.keys[i]:
                i += 1
            if i < nd.n() and k == nd.keys[i]:
                return (nd, i)
            elif nd.leaf:
                return (None, -1)
            else:
                nd = nd.children[i]

    def split_root(self):
        s = Node(self.t, leaf=False, children=[self.root])
        self.root = s
        self.root.split_child(0)
        return self.root

    def insert(self, k):
        if self.root.should_split():
            self.split_root()
        self.root.insert_nonfull(k)

    def delete(self, k):
        ok = self.root.delete(k)
        if self.root.n() == 0 and not self.root.leaf:
            self.root = self.root.children[0]
            self.root.p = None
        return ok

    def dump(self):
        lv = dict()
        q = deque()
        q.append((self.root, 0))
        while q:
            (n, l) = q.popleft()
            if not lv.get(l):
                lv[l] = []
            lv[l].append(n)
            for c in n.children:
                q.append((c, l + 1))
        for k in sorted(lv.keys()):
            vs = lv[k]
            for v in vs:
                print(v, end="|")
            print("")


if __name__ == "__main__":
    t = BTree(2)
    for i in [
        "F",
        "S",
        "Q",
        "K",
        "C",
        "L",
        "H",
        "T",
        "V",
        "W",
        "M",
        "R",
        "N",
        "P",
        "A",
        "B",
        "X",
        "Y",
        "D",
        "Z",
        "E",
    ]:
        t.insert(i)
    for i in [
        "F",
        "S",
        "Q",
        "K",
        "C",
        "L",
        "H",
        "T",
        "V",
        "W",
        "M",
        "R",
        "N",
        "P",
        "A",
        "B",
        "X",
        "Y",
        "D",
        "Z",
        "E",
    ]:
        t.delete(i)
    t.dump()
