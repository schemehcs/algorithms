import random 

def hash_division(x, m):
    return x % m

# const A
# example A = math.pi % 1
def hash_multiplication(x, A, m):
    return int(m * (x * A % 1))

def hash_multiply_shift(k, a, w, l):
    return (k*a % (2**w)) >> (w-l)

def hash_suite(p):
    a = random.randrange(1, p)
    b = random.randrange(p)
    return lambda key: (a * key + b) % p

# Hash table mode: open address
# linear probe
def hash_insert(T, hf, k, v):
    key = hf(k) % len(T)
    for _ in range(len(T)):
        if T[key] == None or T[key][0] == k:
            T[key] = (k, v)
            return
        else:
            key = (key+1) % len(T)
    raise RuntimeError("hash table is full")

def hash_search(T, hf, k):
    key = hf(k) % len(T)
    for _ in range(len(T)):
        if T[key] == None:
            return None
        elif T[key][0] == k:
            return T[key]
        else:
            key = (key + 1) % len(T)
    return None

def g(T, hf, k, q):
    key = hf(k)
    return (q - key) % len(T)

def hash_delete_inner(T, hf, q):
    while True:
        T[q] = None
        qd = q
        while True:
            qd = (qd + 1) % len(T)
            if T[qd] == None:
                return
            if g(T, hf, T[qd][0], q) < g(T, hf, T[qd][0], qd):
                T[q] = T[qd]
                q = qd
                break

def hash_delete(T, hf, k):
    key = hf(k) % len(T)
    for _ in range(len(T)):
        if T[key] == None:
            return None
        elif T[key][0] == k:
            entry = T[key]
            hash_delete_inner(T, hf, key)
            return entry
    return None

if __name__ == '__main__':
    T = [None] * (2**9)
    hf = hash_suite(701)
    for i in range(100, 200):
        hash_insert(T, hf, i, i*2)
    print(hash_search(T, hf, 22))
    print(hash_search(T, hf, 150))
    print(hash_delete(T, hf, 22))
    print(hash_delete(T, hf, 150))
    print(hash_search(T, hf, 150))
    hash_insert(T, hf, 150, 222)
    print(hash_search(T, hf, 150))
    hash_delete(T, hf, 150)
    print(hash_search(T, hf, 150))
    
    

