import random


# O(1) time.
def hash_division(x, m):
    if m <= 0:
        raise ValueError("table size must be positive")
    return x % m


# const A
# example A = math.pi % 1
# O(1) time.
def hash_multiplication(x, A, m):
    if m <= 0:
        raise ValueError("table size must be positive")
    return int(m * (x * A % 1))


# O(1) time.
def hash_multiply_shift(k, a, w, l):
    if w < 1 or not 0 <= l <= w:
        raise ValueError("require w >= 1 and 0 <= l <= w")
    return (k * a % (2**w)) >> (w - l)


# O(1) time to construct the hash function.
def hash_suite(p):
    if p <= 1:
        raise ValueError("p must be greater than 1")
    a = random.randrange(1, p)
    b = random.randrange(p)
    return lambda key: (a * key + b) % p


# Hash table mode: open address
# linear probe
# Expected O(1) time at a bounded load factor; O(n) worst case.
def hash_insert(T, hf, k, v):
    if not T:
        raise ValueError("hash table must not be empty")
    key = hf(k) % len(T)
    for _ in range(len(T)):
        if T[key] is None or T[key][0] == k:
            T[key] = (k, v)
            return
        else:
            key = (key + 1) % len(T)
    raise RuntimeError("hash table is full")


# Expected O(1) time at a bounded load factor; O(n) worst case.
def hash_search(T, hf, k):
    if not T:
        raise ValueError("hash table must not be empty")
    key = hf(k) % len(T)
    for _ in range(len(T)):
        if T[key] is None:
            return None
        elif T[key][0] == k:
            return T[key]
        else:
            key = (key + 1) % len(T)
    return None


# O(1) time.
def g(T, hf, k, q):
    key = hf(k)
    return (q - key) % len(T)


# O(n) worst-case time to close a deleted slot's probe sequence.
def hash_delete_inner(T, hf, q):
    while True:
        T[q] = None
        qd = q
        while True:
            qd = (qd + 1) % len(T)
            if T[qd] is None:
                return
            if g(T, hf, T[qd][0], q) < g(T, hf, T[qd][0], qd):
                T[q] = T[qd]
                q = qd
                break


# Expected O(1) time at a bounded load factor; O(n) worst case.
def hash_delete(T, hf, k):
    if not T:
        raise ValueError("hash table must not be empty")
    key = hf(k) % len(T)
    for _ in range(len(T)):
        if T[key] is None:
            return None
        elif T[key][0] == k:
            entry = T[key]
            hash_delete_inner(T, hf, key)
            return entry
        key = (key + 1) % len(T)
    return None


if __name__ == "__main__":
    T = [None] * (2**9)
    hf = hash_suite(701)
    for i in range(100, 200):
        hash_insert(T, hf, i, i * 2)
    print(hash_search(T, hf, 22))
    print(hash_search(T, hf, 150))
    print(hash_delete(T, hf, 22))
    print(hash_delete(T, hf, 150))
    print(hash_search(T, hf, 150))
    hash_insert(T, hf, 150, 222)
    print(hash_search(T, hf, 150))
    hash_delete(T, hf, 150)
    print(hash_search(T, hf, 150))
