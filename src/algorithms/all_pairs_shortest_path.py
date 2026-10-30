import copy
import pprint
from .graph import WGraph


# O(|V|^3)
def floyd_warshall(G):
    distances = copy.deepcopy(G.matrix)
    predecessors = copy.deepcopy(G.matrix)
    for i in range(len(predecessors)):
        for j in range(len(predecessors)):
            if i == j or predecessors[i][j] == float("inf"):
                predecessors[i][j] = None
            else:
                predecessors[i][j] = i
    n = len(distances)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                through_k = distances[i][k] + distances[k][j]
                if through_k < distances[i][j]:
                    distances[i][j] = through_k
                    predecessors[i][j] = predecessors[k][j]
    return (distances, predecessors)


if __name__ == "__main__":
    G = WGraph(
        [1, 2, 3, 4, 5],
        [
            (1, 2, 3),
            (1, 5, -4),
            (1, 3, 8),
            (2, 5, 7),
            (2, 4, 1),
            (3, 2, 4),
            (4, 3, -5),
            (4, 1, 2),
            (5, 4, 6),
        ],
    )
    pprint.pp(G.matrix)
    distances, predecessors = floyd_warshall(G)
    pprint.pp(distances)
    pprint.pp(predecessors)
