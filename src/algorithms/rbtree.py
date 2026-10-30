from collections import deque
from enum import Enum
from functools import total_ordering


class Color(Enum):
    BLACK = 0
    RED = 1


class Node:
    def __init__(self, key, color=Color.BLACK):
        self.size = 1
        self.key = key
        self.color = color
        self.p = None
        self.left = None
        self.right = None


class RbTree:
    def __init__(self, callback=None):
        self.nil = Node(None)
        self.nil.size = 0
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.nil.p = self.nil
        self.root = self.nil
        self.callback = callback

    # O(log n) time.
    def search(self, key):
        x = self.root
        while x is not self.nil:
            if x.key == key:
                return x
            elif x.key > key:
                x = x.left
            else:
                x = x.right
        return None

    # O(log n) time.
    def insert(self, z: Node):
        x = self.root
        y = self.nil
        while x is not self.nil:
            y = x
            x.size += 1
            if x.key > z.key:
                x = x.left
            else:
                x = x.right
        if y is self.nil:
            self.root = z
        elif y.key > z.key:
            y.left = z
        else:
            y.right = z
        z.p = y
        z.left = self.nil
        z.right = self.nil
        z.color = Color.RED
        if self.callback:
            while y is not self.nil:
                self.callback(y)
                y = y.p
        self.insert_fixup(z)

    # O(log n) time.
    def insert_fixup(self, z: Node):
        while z.p.color is Color.RED:
            if z.p is z.p.p.left:
                y = z.p.p.right  # uncle node
                if y.color is Color.RED:
                    z.p.color = Color.BLACK
                    y.color = Color.BLACK
                    z.p.p.color = Color.RED
                    z = z.p.p
                else:
                    if z is z.p.right:
                        z = z.p
                        self.left_rotate(z)
                    z.p.color = Color.BLACK
                    z.p.p.color = Color.RED
                    self.right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.color is Color.RED:
                    z.p.color = Color.BLACK
                    y.color = Color.BLACK
                    z.p.p.color = Color.RED
                    z = z.p.p
                else:
                    if z is z.p.left:
                        z = z.p
                        self.right_rotate(z)
                    z.p.color = Color.BLACK
                    z.p.p.color = Color.RED
                    self.left_rotate(z.p.p)
        self.root.color = Color.BLACK

    # O(log n) time.
    def delete(self, z):
        y = z
        y_original_color = y.color
        if z.left is self.nil:
            x = z.right
            p = z.p
            self.transplant(z, z.right)
        elif z.right is self.nil:
            x = z.left
            p = z.p
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y is not z.right:
                p = y.p
                self.transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            else:
                x.p = y
                p = y
            self.transplant(z, y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        self._recompute_up(p)

        if y_original_color is Color.BLACK:
            self.delete_fixup(x)

    # O(log n) time, excluding optional callback work.
    def _recompute_up(self, node):
        while node is not self.nil:
            node.size = node.left.size + node.right.size + 1
            if self.callback:
                self.callback(node)
            node = node.p

    # O(log n) time.
    def delete_fixup(self, x):
        while x is not self.root and x.color is Color.BLACK:
            if x is x.p.left:
                w = x.p.right
                if w.color is Color.RED:
                    w.color = Color.BLACK
                    x.p.color = Color.RED
                    self.left_rotate(x.p)
                    w = x.p.right
                if (
                    w.left.color is Color.BLACK
                    and w.right.color is Color.BLACK
                ):
                    w.color = Color.RED
                    x = x.p
                else:
                    if w.right.color is Color.BLACK:
                        w.left.color = Color.BLACK
                        w.color = Color.RED
                        self.right_rotate(w)
                        w = x.p.right
                    w.color = x.p.color
                    x.p.color = Color.BLACK
                    w.right.color = Color.BLACK
                    self.left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.color is Color.RED:
                    w.color = Color.BLACK
                    x.p.color = Color.RED
                    self.right_rotate(x.p)
                    w = x.p.left
                if (
                    w.right.color is Color.BLACK
                    and w.left.color is Color.BLACK
                ):
                    w.color = Color.RED
                    x = x.p
                else:
                    if w.left.color is Color.BLACK:
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self.left_rotate(w)
                        w = x.p.left
                    w.color = x.p.color
                    x.p.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self.right_rotate(x.p)
                    x = self.root
        x.color = Color.BLACK

    # O(1) time.
    def transplant(self, u, v):
        if u.p is self.nil:
            self.root = v
        elif u.p.left is u:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    # O(1) time, excluding optional callback work.
    def left_rotate(self, x):
        y = x.right
        if y is self.nil:
            return
        x.right = y.left
        if x.right is not self.nil:
            x.right.p = x
        if x.p is self.nil:
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
            while n is not self.nil:
                self.callback(n)
                n = n.p

    # O(1) time, excluding optional callback work.
    def right_rotate(self, y):
        x = y.left
        if x is self.nil:
            return
        y.left = x.right
        if y.left is not self.nil:
            y.left.p = y
        if y.p is self.nil:
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
            while n is not self.nil:
                self.callback(n)
                n = n.p

    # O(log n) time.
    def minimum(self, u):
        while u.left is not self.nil:
            u = u.left
        return u

    # O(log n) time using subtree sizes.
    def nth(self, n):
        x = self.root
        if n < 1 or x is self.nil or x.size < n:
            return None
        while True:
            if x.left.size + 1 == n:
                return x
            elif x.left.size >= n:
                x = x.left
            else:
                n = n - x.left.size - 1
                x = x.right

    # O(n) time and O(n) extra space.
    def dump(self):
        if self.root is self.nil:
            return
        q = deque()
        x = self.root
        q.append((x, 0))
        cur_level = 0
        while q:
            e = q.popleft()
            if cur_level != e[1]:
                print("")
                cur_level = e[1]
            print(
                "|{}|{}({})".format(e[0].p.key, e[0].key, e[0].size),
                end=" ",
            )
            if e[0].left is not self.nil:
                q.append((e[0].left, e[1] + 1))
            if e[0].right is not self.nil:
                q.append((e[0].right, e[1] + 1))
        print()


@total_ordering
class Interval:
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self.max = high

    def __eq__(self, other) -> bool:
        if not isinstance(other, Interval):
            return NotImplemented
        return (self.low, self.high) == (other.low, other.high)

    def __lt__(self, other):
        if not isinstance(other, Interval):
            return NotImplemented
        return (self.low, self.high) < (other.low, other.high)

    def __repr__(self) -> str:
        return "[{},{}]{}".format(self.low, self.high, self.max)


# O(1) time.
def overlap(ia, ib) -> bool:
    return ia.high >= ib.low and ia.low <= ib.high


# O(log n) time for a balanced tree.
def interval_search(tree, i):
    x = tree.root
    while x is not tree.nil and not overlap(x.key, i):
        if x.left is not tree.nil and x.left.key.max >= i.low:
            x = x.left
        else:
            x = x.right
    return x


# O(1) time, excluding the callback work it computes.
def max_node(node):
    if node.left.size == 0 and node.right.size == 0:
        node.key.max = node.key.high
    elif node.left.size != 0 and node.right.size != 0:
        node.key.max = max(
            node.key.high, node.left.key.max, node.right.key.max
        )
    elif node.left.size != 0:
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
