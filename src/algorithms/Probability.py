def permutations(n: int, r: int) -> int:
    v = 1
    while r > 0:
        v *= n
        n -= 1
        r -= 1
    return v


def combinations(n: int, r: int) -> int:
    return permutations(n, r) // permutations(r, r)


def multinomial_coefficient(n: int, *rs: int) -> int:
    v = permutations(n, n)
    for r in rs:
        v //= permutations(r, r)
    return v


# print(combinations(6, 2) * 2**4)
# print(combinations(14, 7))

print(permutations(7, 7) // permutations(3, 3) // permutations(2, 2))
print(permutations(5, 5) // permutations(2, 2))
print(5 * permutations(5, 5) // permutations(2, 2))


print(multinomial_coefficient(7, 2, 3, 2))
print(
    2**2
    * combinations(7, 2)
    * (-3) ** 3
    * combinations(5, 3)
    * combinations(2, 2)
    * 1
)

print(combinations(12, 2))
print(combinations(9, 2))

print(combinations(6, 3) * combinations(3, 2))
print(combinations(6, 2) * 4)

if __name__ == "__main__":
    print(combinations(51, 12) / combinations(52, 13))
    print(combinations(13, 5) * combinations(39, 8) / combinations(52, 13))
    print(
        combinations(13, 5)
        * combinations(13, 5)
        * combinations(13, 2)
        * combinations(13, 1)
        / combinations(52, 13)
    )

    print(permutations(6, 3) / 6**3)
    print(5 / 9)

    print(1 - (5 / 6) ** 4)

    # at least one double six in 24 rolls
    print(1 - (1 - 1 / 36) ** 24)
