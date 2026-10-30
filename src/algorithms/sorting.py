import random
import unittest


def insertion_sort(l: list[int]):
    for i in range(1, len(l)):
        for j in range(i, 0, -1):
            if l[j - 1] > l[j]:
                l[j - 1], l[j] = l[j], l[j - 1]
            else:
                break


def insertion_sort_rev(l: list[int]):
    for i in range(1, len(l)):
        for j in range(i, 0, -1):
            if l[j - 1] < l[j]:
                l[j - 1], l[j] = l[j], l[j - 1]


def insertion_sort_rec(l: list[int], p: int):
    if p > 0:
        insertion_sort_rec(l, p - 1)
        while p != 0 and l[p] < l[p - 1]:
            l[p - 1], l[p] = l[p], l[p - 1]
            p -= 1


def merge_sort(l: list[int]):
    def merge(s, mid, e, stage):
        si = ai = s
        bi = mid
        while ai < mid and bi < e:
            if l[ai] < l[bi]:
                stage[si] = l[ai]
                si += 1
                ai += 1
            else:
                stage[si] = l[bi]
                si += 1
                bi += 1
        while ai < mid:
            stage[si] = l[ai]
            si += 1
            ai += 1
        while bi < e:
            stage[si] = l[bi]
            si += 1
            bi += 1
        l[s:e] = stage[s:e]

    def merge_sort_inner(s: int, e: int, stage):
        if e - s <= 1:
            return
        mid = int((s + e) / 2)
        merge_sort_inner(s, mid, stage)
        merge_sort_inner(mid, e, stage)
        merge(s, mid, e, stage)

    merge_sort_inner(0, len(l), [0] * len(l))


def search_sum_of_2(ls: list[int], s: int) -> tuple[int, int] | None:
    merge_sort(ls)
    i, j = 0, len(ls) - 1
    while i < j:
        ijs = ls[i] + ls[j]
        if ijs == s:
            return ls[i], ls[j]
        elif ijs > s:
            j -= 1
        else:
            i += 1
    return None


def linear_search(x: int, l: list[int]) -> int | None:
    for i, lx in enumerate(l):
        if lx == x:
            return i
    return None


def binary_search(ls: list[int], e: int) -> None | int:
    if len(ls) == 0:
        return None
    l = 0
    r = len(ls) - 1
    while l <= r:
        mid = (l + r) // 2
        if ls[mid] == e:
            return mid
        elif ls[mid] > e:
            r = mid - 1
        else:
            l = mid + 1
    return None


def adder(a, b) -> list[int]:
    carry = 0
    if len(a) > len(b):
        return adder(b, a)
    i = 0
    c = []
    while i < len(a):
        v = a[i] + b[i] + carry
        c.append(v % 2)
        carry = int(v / 2)
        i += 1
    while i < len(b):
        v = b[i] + carry
        c.append(v % 2)
        carry = int(v / 2)
        i += 1
    if carry != 0:
        c.append(carry)
    return c


def selection_sort(l: list[int]):
    for i in range(0, len(l)):
        min_i = i
        for j in range(i + 1, len(l)):
            if l[j] < l[min_i]:
                min_i = j
        if min_i != i:
            l[min_i], l[i] = l[i], l[min_i]


def min_cmp(a, b):
    return a < b


def max_cmp(a, b):
    return a > b


def parent(idx: int) -> int:
    return (idx - 1) // 2


def left(idx: int) -> int:
    return idx * 2 + 1


def right(idx: int) -> int:
    return idx * 2 + 2


def bubble_up(heap: list[int], idx: int, cmp):
    while idx != 0:
        pidx = parent(idx)
        if cmp(heap[idx], heap[pidx]):
            heap[pidx], heap[idx] = heap[idx], heap[pidx]
        else:
            return
        idx = pidx


def push_down(heap: list[int], idx: int, heap_size: int, cmp):
    while idx < heap_size:
        candidate = idx
        if left(idx) < heap_size and cmp(heap[left(idx)], heap[candidate]):
            candidate = left(idx)
        if right(idx) < heap_size and cmp(heap[right(idx)], heap[candidate]):
            candidate = right(idx)
        if candidate != idx:
            heap[idx], heap[candidate] = heap[candidate], heap[idx]
            idx = candidate
        else:
            return


def build_heap(raw: list[int], cmp) -> list[int]:
    heap = [0] * len(raw)
    for i, e in enumerate(raw):
        heap[i] = e
        bubble_up(heap, i, cmp)
    return heap


def heapify(raw: list[int], cmp):
    heap_size = len(raw)
    pivot = parent(heap_size - 1)
    while pivot >= 0:
        push_down(raw, pivot, heap_size, cmp)
        pivot -= 1


def heap_extract(heap: list[int], heap_size: int, cmp) -> None | int:
    if heap_size == 0:
        return None
    heap[0], heap[heap_size - 1] = heap[heap_size - 1], heap[0]
    push_down(heap, 0, heap_size - 1, cmp)
    return heap[heap_size - 1]


def heap_sort(ls: list[int], cmp):
    heapify(ls, cmp)
    heap_size = len(ls)
    while heap_size > 1:
        ls[heap_size - 1], ls[0] = ls[0], ls[heap_size - 1]
        heap_size -= 1
        push_down(ls, 0, heap_size, cmp)


class Heap:
    def __init__(self, ord=max_cmp, heap=None):
        self.ord = ord
        if heap:
            self.heap = heap
            heapify(self.heap, self.ord)
        else:
            self.heap = []

    def append(self, e):
        self.heap.append(e)
        bubble_up(self.heap, len(self.heap) - 1, self.ord)

    def extract(self) -> None | int:
        if self.heap:
            self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
            e = self.heap.pop()
            push_down(self.heap, 0, len(self.heap), self.ord)
            return e
        else:
            return None


def quick_sort(ls: list[int]):
    def partition(s: int, e: int, pivot: int) -> int:
        ls[pivot], ls[e - 1] = ls[e - 1], ls[pivot]
        i = s
        for j in range(s, e - 1):
            if ls[j] < ls[e - 1]:
                ls[j], ls[i] = ls[i], ls[j]
                i += 1
        ls[e - 1], ls[i] = ls[i], ls[e - 1]
        return i

    def quick_sort_inner(s, e):
        if s < e:
            pivot = random.randrange(s, e)
            pos = partition(s, e, pivot)
            quick_sort_inner(s, pos)
            quick_sort_inner(pos + 1, e)

    quick_sort_inner(0, len(ls))


def counting_sort(ls: list[int], s: int, e: int):
    stage = [0] * (e - s)
    for i in ls:
        if i < s or i >= e:
            raise IndexError("item={}, out of range=[{}:{})".format(i, s, e))
        stage[i - s] += 1
    i = 0
    for j, cnt in enumerate(stage):
        for _ in range(cnt):
            ls[i] = j + s
            i += 1


# worst cost O(n^2)
# expected O(n)
def parition(ls: list[int], start, stop, pivot) -> int:
    i = start
    ls[pivot], ls[stop - 1] = ls[stop - 1], ls[pivot]
    for j in range(start, stop - 1):
        if ls[j] <= ls[stop - 1]:
            ls[j], ls[i] = ls[i], ls[j]
            i += 1
    ls[i], ls[stop - 1] = ls[stop - 1], ls[i]
    return i


def select_by_partition(ls: list[int], s: int, e: int, nth: int) -> int | None:
    while s < e and nth < e - s:
        pivot = random.randrange(s, e)
        i = parition(ls, s, e, pivot)
        if i - s == nth:
            return ls[i]
        elif i - s < nth:
            nth -= i + 1 - s
            s = i + 1
        else:
            e = i
    return None


def step_sort(ls: list[int], start: int, stop: int, step: int):
    for i in range(start, stop, step):
        for j in range(i, start, -step):
            if ls[j] < ls[j - step]:
                ls[j], ls[j - step] = ls[j - step], ls[j]


# worst case O(n)
def select(ls: list[int], s: int, e: int, nth: int) -> int | None:
    if e - s <= nth:
        return None
    while (e - s) % 5 != 0:
        for i in range(s + 1, e):
            if ls[s] > ls[i]:
                ls[s], ls[i] = ls[i], ls[s]
        if nth == 0:
            return s
        else:
            nth -= 1
            s += 1
    g = (e - s) // 5
    for i in range(s, s + g):
        step_sort(ls, s, s + g * 5, g)
    pivot = select(ls, s + 2 * g, s + 3 * g, g // 2)
    if pivot is None:
        return None
    i = parition(ls, s, e, pivot)
    if i - s == nth:
        return i
    elif i - s < nth:
        return select(ls, i + 1, e, nth - (i + 1 - s))
    else:
        return select(ls, s, i, nth)


class Tests(unittest.TestCase):
    def testme(self):
        ls = [11, 33, 44, 88, 5, 4, 8, 1, 22, 66, 55]
        idx = select(ls, 0, len(ls), 20)
        if idx is None:
            print("Not found")
        else:
            print("pos:{}, val: {}, ls={}".format(idx, ls[idx], ls))


if __name__ == "__main__":
    unittest.main()
