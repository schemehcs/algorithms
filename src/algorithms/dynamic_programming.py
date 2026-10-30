from functools import cache


# rod cutting
#              0  1  2  3  4  5   6   7   8   9   10
price_table = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]


# formula: sol(n) = max{ for i in [0, n) sol(i) + sol(n-i) }
# O(n^2) time and O(n) space with memoization.
def rod_cutting_rec(n):
    if n < 0:
        raise ValueError("rod length must be non-negative")

    @cache
    def solve(length):
        best_price = price_table[length] if length < len(price_table) else 0
        best_first_cut = length if length < len(price_table) else 0
        for first_cut in range(1, length):
            first_price, _ = solve(first_cut)
            second_price, _ = solve(length - first_cut)
            candidate = first_price + second_price
            if candidate > best_price:
                best_price = candidate
                best_first_cut = first_cut
        return best_price, best_first_cut

    best_price, _ = solve(n)
    cuts = []
    pending_lengths = [n]
    while pending_lengths:
        length = pending_lengths.pop()
        if length == 0:
            continue
        _, first_cut = solve(length)
        if first_cut == length:
            cuts.append(length)
        else:
            pending_lengths.append(length - first_cut)
            pending_lengths.append(first_cut)
    return best_price, tuple(cuts)


# O(n^2) time and O(n) space for requested rod length n.
def rod_cutting_dp(n):
    if n < 0:
        raise ValueError("rod length must be non-negative")
    revenue = [0] * (n + 1)
    for length in range(1, n + 1):
        best = price_table[length] if length < len(price_table) else 0
        for first_cut in range(1, length):
            best = max(best, revenue[first_cut] + revenue[length - first_cut])
        revenue[length] = best
    return revenue


a = "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
b = "GTCGTTCGGAATGCCGTTGCTCTGTAAA"


# O(mn) time and O(mn) space for input lengths m and n.
def longest_common_subsequence(a, b):
    al = len(a)
    bl = len(b)
    mat = [[0] * (bl + 1) for _ in range(al + 1)]
    for i in range(al):
        for j in range(bl):
            if a[i] == b[j]:
                mat[i + 1][j + 1] = mat[i][j] + 1
            elif mat[i][j + 1] < mat[i + 1][j]:
                mat[i + 1][j + 1] = mat[i + 1][j]
            else:
                mat[i + 1][j + 1] = mat[i][j + 1]
    sequence = []
    i = al - 1
    j = bl - 1
    while i >= 0 and j >= 0:
        if a[i] == b[j]:
            sequence.append(a[i])
            i -= 1
            j -= 1
        elif mat[i][j + 1] > mat[i + 1][j]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(sequence))


if __name__ == "__main__":
    print(longest_common_subsequence(a, b))
    print(longest_common_subsequence("10010101", "010110110"))
