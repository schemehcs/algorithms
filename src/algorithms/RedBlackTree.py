BLACK = 0
RED = 1


class Node:
    def __init__(self, key, color=BLACK):
        self.size = 1
        self.key = key
        self.color = color
        self.p = None
        self.left = None
        self.right = None


NIL = Node(None)
NIL.size = 0


class RbTree:
    def __init__(self, callback=None):
        self.root = NIL
        self.callback = callback

    def search(self, key):
        x = self.root
        while x is not NIL:
            if x.key == key:
                return x
            elif x.key > key:
                x = x.left
            else:
                x = x.right
        return None

    def insert(self, z: Node):
        x = self.root
        y = NIL
        while x is not NIL:
            y = x
            x.size += 1
            if x.key > z.key:
                x = x.left
            else:
                x = x.right
        if y is NIL:
            self.root = z
        elif y.key > z.key:
            y.left = z
        else:
            y.right = z
        z.p = y
        z.left = NIL
        z.right = NIL
        z.color = RED
        if self.callback:
            while y is not NIL:
                self.callback(y)
                y = y.p
        self.insert_fixup(z)

    def insert_fixup(self, z: Node):
        while z.p.color is RED:
            if z.p is z.p.p.left:
                y = z.p.p.right  # uncle node
                if y.color is RED:
                    z.p.color = BLACK
                    y.color = BLACK
                    z.p.p.color = RED
                    z = z.p.p
                else:
                    if z is z.p.right:
                        z = z.p
                        self.left_rotate(z)
                    z.p.color = BLACK
                    z.p.p.color = RED
                    self.right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.color is RED:
                    z.p.color = BLACK
                    y.color = BLACK
                    z.p.p.color = RED
                    z = z.p.p
                else:
                    if z is z.p.left:
                        z = z.p
                        self.right_rotate(z)
                    z.p.color = BLACK
                    z.p.p.color = RED
                    self.left_rotate(z.p.p)
        self.root.color = BLACK

    def delete(self, z):
        y = z
        y_original_color = y.color
        if z.left is NIL:
            x = z.right
            self.transplant(z, z.right)
            p = z.p
        elif z.right is NIL:
            x = z.left
            self.transplant(z, z.left)
            p = z.p
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y is not z.right:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.p = y
                p = y.p
            else:
                x.p = y
                p = z.p
            self.transplant(z, y)
            y.size = z.size - 1
            y.left = z.left
            y.left.p = y
            y.color = z.color
        while p is not NIL:
            p.size -= 1
            if self.callback:
                self.callback(p)
            p = p.p

        if y_original_color is BLACK:
            self.delete_fixup(x)

    def delete_fixup(self, x):
        while x is not self.root and x.color is BLACK:
            if x is x.p.left:
                w = x.p.right
                if w.color is RED:
                    w.color = BLACK
                    x.p.color = RED
                    self.left_rotate(x.p)
                    w = x.p.right
                if w.left.color is BLACK and w.right.color is BLACK:
                    w.color = RED
                    x = x.p
                else:
                    if w.right.color is BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.p.right
                    w.color = x.p.color
                    x.p.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.color is RED:
                    w.color = BLACK
                    x.p.color = RED
                    self.right_rotate(x.p)
                    w = x.p.left
                if w.right.color is BLACK and w.left.color is BLACK:
                    w.color = RED
                    x = x.p
                else:
                    if w.left.color is BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.p.left
                    w.color = x.p.color
                    x.p.color = BLACK
                    w.left.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.p)
                    x = self.root
        x.color = BLACK

    def transplant(self, u, v):
        if u.p is NIL:
            self.root = v
        elif u.p.left is u:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    def left_rotate(self, x):
        y = x.right
        if y is NIL:
            return
        x.right = y.left
        if x.right is not NIL:
            x.right.p = x
        if x.p is NIL:
            self.root = y
        elif x.p.left is x:
            x.p.left = y
        else:
            x.p.right = y
        y.p = x.p
        y.left = x
        x.p = y
        y.size = x.size
        x.size = x.left.size + x.right.size + 1
        if self.callback:
            n = x
            while n is not NIL:
                self.callback(n)
                n = n.p

    def right_rotate(self, y):
        x = y.left
        if x is NIL:
            return
        y.left = x.right
        if y.left is not NIL:
            y.left.p = y
        if y.p is NIL:
            self.root = x
        elif y.p.left is y:
            y.p.left = x
        else:
            y.p.right = x
        x.p = y.p
        x.right = y
        y.p = x
        x.size = y.size
        y.size = y.left.size + y.right.size + 1
        if self.callback:
            n = y
            while n is not NIL:
                self.callback(n)
                n = n.p

    def minimum(self, u):
        while u.left is not NIL:
            u = u.left
        return u

    def nth(self, n):
        x = self.root
        if x is NIL or x.size < n:
            return None
        while True:
            if x.left.size + 1 == n:
                return x
            elif x.left.size >= n:
                x = x.left
            else:
                n = n - x.left.size - 1
                x = x.right

    def dump(self):
        q = deque()
        x = self.root
        q.append((x, 0))
        cur_level = 0
        al = []
        while q:
            e = q.popleft()
            al.append(e[0])
            if cur_level != e[1]:
                print("")
                cur_level = e[1]
            print("|{}|{}({})".format(e[0].p.key, e[0].key, e[0].size), end=" ")
            if e[0].left is not NIL:
                q.append((e[0].left, e[1] + 1))
            if e[0].right is not NIL:
                q.append((e[0].right, e[1] + 1))
        print()


from functools import total_ordering


@total_ordering
class Interval:
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self.max = high

    def __eq__(self, value) -> bool:
        return self.low == value.low

    def __le__(self, other):
        return self.low < other.low

    def __repr__(self) -> str:
        return "[{},{}]{}".format(self.low, self.high, self.max)


def overlap(ia, ib) -> bool:
    return ia.high >= ib.low and ia.low <= ib.high


def interval_search(tree, i):
    x = tree.root
    while x is not NIL and not overlap(x.key, i):
        if x.left is not NIL and x.left.key.max >= i.low:
            x = x.left
        else:
            x = x.right
    return x


from collections import deque


def test():
    q = deque()
    T = RbTree()
    for i in range(1, 20):
        T.insert(Node(i))
    T.dump()
    n10 = T.search(10)
    n13 = T.search(13)
    T.delete(n10)
    T.delete(n13)
    T.dump()
    for n in range(1, 20):
        nth = T.nth(n)
        if nth:
            print("{}th={}".format(n, T.nth(n).key))
        else:
            print("{}th does not exists")


def max_node(node):
    if node.left is NIL and node.right is NIL:
        node.key.max = node.key.high
    elif node.left is not NIL and node.right is not NIL:
        node.key.max = max(node.key.high, node.left.key.max, node.right.key.max)
    elif node.left is not NIL:
        node.key.max = max(node.key.high, node.left.key.max)
    else:
        node.key.max = max(node.key.high, node.right.key.max)


if __name__ == "__main__":
    t = RbTree(callback=max_node)
    intervals = [
        (0, 3),
        (6, 10),
        (5, 8),
        (15, 23),
        (8, 9),
        (16, 21),
        (25, 30),
        (17, 19),
        (26, 26),
        (19, 20),
    ]
    for l, h in intervals:
        n = Interval(l, h)
        t.insert(Node(n))

    p = interval_search(t, Interval(31, 41))
    print(p and p.key)
