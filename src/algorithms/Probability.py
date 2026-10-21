def P(n: int, r: int) -> int:
    v = 1
    while r > 0:
        v *= n
        n -= 1
        r -= 1
    return v

def C(n: int, r: int) -> int:
    return P(n, r) // P(r, r)

def MC(n: int, *rs: int) -> int:
    v = P(n, n)
    for r in rs:
        v //= P(r, r)
    return v

#print(C(6, 2) * 2**4)
#print(C(14, 7))

print(P(7, 7) // P(3, 3) // P(2, 2))
print(P(5, 5) // P(2, 2))
print(5* P(5, 5) // P(2, 2))


print(MC(7, 2, 3, 2))
print(2**2 * C(7, 2) * (-3)**3 * C(5, 3) * C(2, 2) * 1)

print(C(12, 2))
print(C(9, 2))

print(C(6, 3) * C(3, 2))
print(C(6, 2) * 4)

if __name__ == '__main__':
    print( C(51, 12) / C(52, 13) )
    print( C(13, 5) * C(39, 8) / C(52, 13) )
    print( C(13, 5) * C(13, 5) * C(13, 2) * C(13, 1) / C(52, 13) )

    print( P(6, 3) / 6**3 )
    print ( 5/ 9)


    print(1- (5/6)**4)
    
    # at least one double six in 24 rolls
    print( 1- (1 - 1/ 36) ** 24 )