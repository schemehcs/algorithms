# activity selection
import heapq
from functools import total_ordering


s = [1, 3, 0, 5, 3, 5, 6, 7, 8, 2, 12][::-1]
f = [4, 5, 6, 7, 9, 9, 10, 11, 12, 14, 16][::-1]


# O(n log n) time and O(n) extra space.
def sort_acts_by_f(s, f):
    activities = sorted(zip(s, f), key=lambda activity: activity[1])
    s[:], f[:] = zip(*activities) if activities else ([], [])


# O(n log n) time and O(n) output space.
def selection(s, f):
    if len(s) != len(f):
        raise ValueError("start and finish arrays must have equal lengths")
    if not s:
        return []
    sort_acts_by_f(s, f)
    workable = [(s[0], f[0])]
    for i in range(1, len(f)):
        if s[i] >= workable[-1][1]:
            workable.append((s[i], f[i]))
    return workable


@total_ordering
class Node:
    def __init__(self, cnt, ch=None):
        self.cnt = cnt
        self.ch = ch
        self.left = None
        self.right = None

    def __eq__(self, other):
        return self.cnt == other.cnt

    def __lt__(self, other):
        return self.cnt < other.cnt


# O(k log k) time and O(k) space for k symbols.
def huffman(char_cnt):
    if any(count < 0 for count in char_cnt.values()):
        raise ValueError("frequencies must be non-negative")
    ls = []
    for ch, cnt in char_cnt.items():
        ls.append(Node(cnt, ch))
    if not ls:
        return []
    heapq.heapify(ls)
    while len(ls) > 1:
        l = heapq.heappop(ls)
        r = heapq.heappop(ls)
        n = Node(l.cnt + r.cnt)
        n.left = l
        n.right = r
        heapq.heappush(ls, n)
    res = []
    huffman_encodings(ls[0], "", res)
    return res


# O(kh) time for k symbols and tree height h; recursion uses O(h) space.
def huffman_encodings(node: Node, prefix, res):
    if node and node.left and node.right:
        huffman_encodings(node.left, prefix + "0", res)
        huffman_encodings(node.right, prefix + "1", res)
    else:
        res.append((node.ch, prefix))


if __name__ == "__main__":
    a = {"a": 45, "b": 13, "c": 12, "d": 16, "e": 9, "f": 5}
    res = huffman(a)
    print(res)
