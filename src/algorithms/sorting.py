import random


# O(n^2) worst-case time, O(n) best-case time, and O(1) extra space.
def insertion_sort(l: list[int]):
    for i in range(1, len(l)):
        for j in range(i, 0, -1):
            if l[j - 1] > l[j]:
                l[j - 1], l[j] = l[j], l[j - 1]
            else:
                break


# O(n^2) time and O(1) extra space.
def insertion_sort_rev(l: list[int]):
    for i in range(1, len(l)):
        for j in range(i, 0, -1):
            if l[j - 1] < l[j]:
                l[j - 1], l[j] = l[j], l[j - 1]


# O(n^2) time and O(n) recursion space.
def insertion_sort_rec(l: list[int], p: int):
    if p > 0:
        insertion_sort_rec(l, p - 1)
        while p != 0 and l[p] < l[p - 1]:
            l[p - 1], l[p] = l[p], l[p - 1]
            p -= 1


# O(n log n) time and O(n) extra space.
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


# O(n log n) time and O(n) extra space because the input is sorted first.
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


# O(n) time and O(1) extra space.
def linear_search(x: int, l: list[int]) -> int | None:
    for i, lx in enumerate(l):
        if lx == x:
            return i
    return None


# O(log n) time and O(1) extra space; input must be sorted.
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


# O(n) time and O(n) output space.
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


# O(n^2) time and O(1) extra space.
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


# O(log n) time.
def bubble_up(heap: list[int], idx: int, cmp):
    while idx != 0:
        pidx = parent(idx)
        if cmp(heap[idx], heap[pidx]):
            heap[pidx], heap[idx] = heap[idx], heap[pidx]
        else:
            return
        idx = pidx


# O(log n) time.
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


# O(n log n) time and O(n) extra space.
def build_heap(raw: list[int], cmp) -> list[int]:
    heap = [0] * len(raw)
    for i, e in enumerate(raw):
        heap[i] = e
        bubble_up(heap, i, cmp)
    return heap


# O(n) time and O(1) extra space.
def heapify(raw: list[int], cmp):
    heap_size = len(raw)
    pivot = parent(heap_size - 1)
    while pivot >= 0:
        push_down(raw, pivot, heap_size, cmp)
        pivot -= 1


# O(log n) time.
def heap_extract(heap: list[int], heap_size: int, cmp) -> None | int:
    if heap_size == 0:
        return None
    heap[0], heap[heap_size - 1] = heap[heap_size - 1], heap[0]
    push_down(heap, 0, heap_size - 1, cmp)
    return heap[heap_size - 1]


# O(n log n) time and O(1) extra space.
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

    # O(log n) time.
    def append(self, e):
        self.heap.append(e)
        bubble_up(self.heap, len(self.heap) - 1, self.ord)

    # O(log n) time.
    def extract(self) -> None | int:
        if self.heap:
            self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
            e = self.heap.pop()
            push_down(self.heap, 0, len(self.heap), self.ord)
            return e
        else:
            return None


# O(n log n) average time, O(n^2) worst-case time, and O(log n) extra space.
def quick_sort(ls: list[int]):
    ranges = [(0, len(ls))]
    while ranges:
        start, stop = ranges.pop()
        while stop - start > 1:
            pivot = ls[random.randrange(start, stop)]
            lower = current = start
            upper = stop
            while current < upper:
                if ls[current] < pivot:
                    ls[lower], ls[current] = ls[current], ls[lower]
                    lower += 1
                    current += 1
                elif ls[current] > pivot:
                    upper -= 1
                    ls[current], ls[upper] = ls[upper], ls[current]
                else:
                    current += 1

            left_size = lower - start
            right_size = stop - upper
            if left_size < right_size:
                if right_size > 1:
                    ranges.append((upper, stop))
                stop = lower
            else:
                if left_size > 1:
                    ranges.append((start, lower))
                start = upper


# O(n + k) time and O(k) extra space, where k = e - s.
def counting_sort(ls: list[int], s: int, e: int):
    if e < s:
        raise ValueError("range end must not be less than range start")
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


# O(n) time and O(1) extra space for a single partition.
def parition(ls: list[int], start, stop, pivot) -> int:
    i = start
    ls[pivot], ls[stop - 1] = ls[stop - 1], ls[pivot]
    for j in range(start, stop - 1):
        if ls[j] <= ls[stop - 1]:
            ls[j], ls[i] = ls[i], ls[j]
            i += 1
    ls[i], ls[stop - 1] = ls[stop - 1], ls[i]
    return i


# Expected O(n) time and O(1) extra space; worst-case time is O(n^2).
def select_by_partition(ls: list[int], s: int, e: int, nth: int) -> int | None:
    if s < 0 or e > len(ls) or s > e or nth < 0:
        return None
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


# Worst-case O(n) time using median-of-medians; recursion uses O(log n) space.
def select(ls: list[int], s: int, e: int, nth: int) -> int | None:
    if s < 0 or e > len(ls) or s > e or nth < 0 or e - s <= nth:
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
