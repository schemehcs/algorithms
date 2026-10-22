# rod cutting
#              0  1  2  3  4  5   6   7   8   9   10
price_table = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]


# formula: sol(n) = max{ for i in [0, n) sol(i) + sol(n-i) }
def rod_cutting_rec(n):
    if n <= 1:
        return price_table[n], (n,)
    max = price_table[n]
    sol = (n,)
    for i in range(1, n):
        fp, fpi = rod_cutting_rec(i)
        sp, spi = rod_cutting_rec(n - i)
        if fp + sp > max:
            max = fp + sp
            sol = fpi + spi
    return max, sol


def rod_cutting_dp(n):
    mat = price_table[:]
    for i in range(2, 11):
        for j in range(1, i):
            if mat[j] + mat[i - j] > mat[i]:
                mat[i] = mat[j] + mat[i - j]
    return mat


a = "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
b = "GTCGTTCGGAATGCCGTTGCTCTGTAAA"


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
    s = ""
    i = al - 1
    j = bl - 1
    while i >= 0 and j >= 0:
        if a[i] == b[j]:
            s += a[i]
            i -= 1
            j -= 1
        elif mat[i][j + 1] > mat[i + 1][j]:
            i -= 1
        else:
            j -= 1
    return s[::-1]


print(longest_common_subsequence(a, b))
print(longest_common_subsequence("10010101", "010110110"))
