import random
import unittest

from algorithms import all_pairs_shortest_path
from algorithms import binarytree
from algorithms import btree
from algorithms import disjointset
from algorithms import dynamic_programming
from algorithms import graph
from algorithms import greedy
from algorithms import hashing
from algorithms import linked_list
from algorithms import minimum_spanning_tree
from algorithms import probability
from algorithms import rbtree
from algorithms import single_source_shortest_path
from algorithms import sorting


class SortingTests(unittest.TestCase):
    def test_comparison_sorts(self):
        source = [5, -1, 3, 3, 0, 9]
        expected = sorted(source)
        for sort in (
            sorting.insertion_sort,
            sorting.insertion_sort_rec,
            sorting.merge_sort,
            sorting.selection_sort,
            sorting.quick_sort,
        ):
            with self.subTest(sort=sort.__name__):
                values = source.copy()
                if sort is sorting.insertion_sort_rec:
                    sort(values, len(values) - 1)
                else:
                    sort(values)
                self.assertEqual(values, expected)

    def test_quick_sort_large_duplicate_input(self):
        values = [5] * 5000 + list(range(100, 0, -1))
        sorting.quick_sort(values)
        self.assertEqual(values, sorted(values))

    def test_reverse_and_counting_sorts(self):
        values = [5, -1, 3, 0, 9]
        sorting.insertion_sort_rev(values)
        self.assertEqual(values, [9, 5, 3, 0, -1])

        values = [5, -1, 3, 0, 9, 3]
        sorting.counting_sort(values, -1, 10)
        self.assertEqual(values, [-1, 0, 3, 3, 5, 9])
        with self.assertRaises(IndexError):
            sorting.counting_sort([10], 0, 10)

    def test_searches_and_selection(self):
        values = [8, 1, 4, 2, 7, 3, 6, 5]
        self.assertEqual(sorting.linear_search(4, values), 2)
        self.assertIsNone(sorting.linear_search(0, values))
        ordered = sorted(values)
        self.assertEqual(ordered[sorting.binary_search(ordered, 6)], 6)
        self.assertIsNone(sorting.binary_search([], 1))

        values = [8, 1, 4, 2, 7, 3, 6, 5]
        self.assertEqual(sorting.search_sum_of_2(values, 9), (1, 8))
        self.assertIsNone(sorting.search_sum_of_2([1, 2, 3], 10))

        source = [9, 1, 5, 3, 7, 2, 8, 4, 6, 0]
        expected = sorted(source)
        values = source.copy()
        self.assertEqual(
            sorting.select_by_partition(values, 0, len(values), 4), expected[4]
        )
        values = source.copy()
        index = sorting.select(values, 0, len(values), 4)
        self.assertIsNotNone(index)
        self.assertEqual(values[index], expected[4])
        self.assertIsNone(
            sorting.select_by_partition(source.copy(), 0, 10, 10)
        )

    def test_selection_algorithms_across_input_sizes(self):
        rng = random.Random(12)
        for size in range(1, 36):
            source = [rng.randrange(-5, 6) for _ in range(size)]
            expected = sorted(source)
            for index in {0, size // 2, size - 1}:
                values = source.copy()
                selected_index = sorting.select(values, 0, size, index)
                self.assertEqual(values[selected_index], expected[index])
                values = source.copy()
                self.assertEqual(
                    sorting.select_by_partition(values, 0, size, index),
                    expected[index],
                )

    def test_heaps_and_binary_adder(self):
        values = [3, 1, 6, 2, 5, 4]
        sorting.heap_sort(values, sorting.max_cmp)
        self.assertEqual(values, [1, 2, 3, 4, 5, 6])

        values = [3, 1, 6, 2, 5, 4]
        heap = sorting.build_heap(values, sorting.max_cmp)
        self.assertEqual(heap[0], 6)
        sorting.heapify(values, sorting.max_cmp)
        self.assertEqual(values[0], 6)
        self.assertEqual(
            sorting.heap_extract(values, len(values), sorting.max_cmp), 6
        )

        heap = sorting.Heap()
        for value in [3, 1, 6, 2, 5, 4]:
            heap.append(value)
        self.assertEqual(
            [heap.extract() for _ in range(6)], [6, 5, 4, 3, 2, 1]
        )
        self.assertIsNone(heap.extract())
        self.assertEqual(sorting.adder([1, 1, 1], [1, 0, 1]), [0, 0, 1, 1])


class GraphTests(unittest.TestCase):
    def test_breadth_first_search_and_topological_sort(self):
        graph_value = graph.Graph(
            ["a", "b", "c", "d"], [("a", "b"), ("a", "c"), ("c", "d")]
        )
        graph.bfs(graph_value, graph_value.vertex_map["a"])
        self.assertEqual(graph_value.vertex_map["d"].d, 2)
        self.assertEqual(graph_value.vertex_map["d"].p.key, "c")

        dag = graph.Graph(
            ["a", "b", "c", "d"],
            [("a", "c"), ("b", "c"), ("c", "d")],
        )
        order = graph.topological_sort(dag)
        positions = {vertex.key: i for i, vertex in enumerate(order)}
        for start, end in dag.edges:
            self.assertLess(positions[start], positions[end])

    def test_depth_first_cycle_detection_propagates(self):
        cyclic = graph.Graph(
            ["a", "b", "c"],
            [("a", "b"), ("b", "c"), ("c", "b")],
        )
        self.assertTrue(graph.dfs(cyclic))
        self.assertIsNone(graph.topological_sort(cyclic))

        acyclic = graph.Graph(["a", "b", "c"], [("a", "b"), ("b", "c")])
        self.assertFalse(graph.dfs(acyclic))
        self.assertFalse(graph.dfs_iter(acyclic))
        self.assertTrue(all(v.f is not None for v in acyclic.vertices))
        self.assertTrue(graph.dfs_iter(cyclic))

    def test_transpose_and_weighted_shortest_paths(self):
        value = graph.Graph(["a", "b"], [("a", "b")]).transpose()
        self.assertIn(
            value.vertex_map["a"],
            value.adjacency[value.vertex_map["b"]],
        )

        weighted = graph.WGraph(
            ["s", "a", "b", "unreachable"],
            [("s", "a", 4), ("s", "b", 5), ("a", "b", -2)],
        )
        self.assertTrue(
            single_source_shortest_path.bellman_ford(weighted, "s")
        )
        self.assertEqual(weighted.vertex_map["b"].d, 2)
        self.assertEqual(weighted.vertex_map["unreachable"].d, float("inf"))
        distances, _ = all_pairs_shortest_path.floyd_warshall(weighted)
        self.assertEqual(distances[0][2], 2)
        self.assertEqual(distances[2][0], float("inf"))

        parallel_edges = graph.WGraph(
            ["a", "b"], [("a", "b", 7), ("a", "b", 2)]
        )
        parallel_distances, _ = all_pairs_shortest_path.floyd_warshall(
            parallel_edges
        )
        self.assertEqual(parallel_distances[0][1], 2)

    def test_bellman_ford_detects_negative_cycle(self):
        weighted = graph.WGraph(["a", "b"], [("a", "b", -2), ("b", "a", -1)])
        self.assertFalse(
            single_source_shortest_path.bellman_ford(weighted, "a")
        )

    def test_dijkstra_and_minimum_spanning_trees(self):
        weighted = graph.WGraph(
            ["a", "b", "c"],
            [("a", "b", 1), ("b", "a", 1), ("b", "c", 2),
             ("c", "b", 2), ("a", "c", 5), ("c", "a", 5)],
        )
        single_source_shortest_path.dijkstra(weighted, "a")
        self.assertEqual(weighted.vertex_map["c"].d, 3)

        kruskal_edges = minimum_spanning_tree.kruskal(weighted)
        prim_edges = minimum_spanning_tree.prim(weighted)
        self.assertEqual(len(kruskal_edges), 2)
        self.assertEqual(sum(edge.w for edge in kruskal_edges), 3)
        self.assertEqual(len(prim_edges), 2)
        self.assertEqual(sum(edge.w for edge in prim_edges), 3)
        self.assertEqual(len(minimum_spanning_tree.prim(weighted)), 2)
        self.assertEqual(
            minimum_spanning_tree.prim(graph.WGraph([], [])), set()
        )
        negative = graph.WGraph(["a", "b"], [("a", "b", -1)])
        with self.assertRaises(ValueError):
            single_source_shortest_path.dijkstra(negative, "a")
        self.assertIsNone(negative.vertex_map["a"].d)


class DataStructureTests(unittest.TestCase):
    def assert_red_black_invariants(self, tree):
        if tree.root is tree.nil:
            return
        self.assertIs(tree.root.color, rbtree.Color.BLACK)

        def visit(node, lower=None, upper=None):
            if node is tree.nil:
                return 1, 0
            self.assertTrue(lower is None or lower <= node.key)
            self.assertTrue(upper is None or node.key <= upper)
            if node.left is not tree.nil:
                self.assertIs(node.left.p, node)
            if node.right is not tree.nil:
                self.assertIs(node.right.p, node)
            if node.color is rbtree.Color.RED:
                self.assertIs(node.left.color, rbtree.Color.BLACK)
                self.assertIs(node.right.color, rbtree.Color.BLACK)
            left_height, left_size = visit(node.left, lower, node.key)
            right_height, right_size = visit(node.right, node.key, upper)
            self.assertEqual(left_height, right_height)
            self.assertEqual(node.size, left_size + right_size + 1)
            return (
                left_height + (node.color is rbtree.Color.BLACK),
                left_size + right_size + 1,
            )

        visit(tree.root)

    def test_disjoint_set_union_and_find(self):
        sets = disjointset.DisjointSet(range(5))
        sets.union(0, 1)
        sets.union(1, 2)
        root = sets.find(0)
        rank = root.rank
        sets.union(0, 2)
        self.assertEqual(root.rank, rank)
        self.assertIs(sets.find(0), sets.find(2))
        self.assertIsNot(sets.find(0), sets.find(3))

    def test_btree_insert_search_and_delete(self):
        tree = btree.BTree(2)
        values = list("FSQKCLHTVWM RNPABXYDZE".replace(" ", ""))
        for value in values:
            tree.insert(value)
        for value in values:
            node, index = tree.search(value)
            self.assertIsNotNone(node)
            self.assertEqual(node.keys[index], value)
        self.assertEqual(tree.search("?"), (None, -1))
        for value in values:
            self.assertTrue(tree.delete(value))
        self.assertFalse(tree.delete("missing"))
        self.assertEqual(tree.root.keys, [])

    def test_red_black_tree_order_statistics_and_deletion(self):
        tree = rbtree.RbTree()
        for value in [7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13]:
            tree.insert(rbtree.Node(value))
        self.assertEqual(
            [tree.nth(i).key for i in range(1, 12)],
            [2, 3, 6, 7, 8, 10, 11, 13, 18, 22, 26],
        )
        self.assertIsNone(tree.nth(0))
        for value in [18, 11, 3, 7, 26, 2, 6, 8, 10, 13, 22]:
            node = tree.search(value)
            self.assertIsNotNone(node)
            tree.delete(node)
            self.assertIsNone(tree.search(value))

    def test_red_black_randomized_deletion_and_independent_sentinels(self):
        first = rbtree.RbTree()
        second = rbtree.RbTree()
        self.assertIsNot(first.nil, second.nil)
        rng = random.Random(0)
        values = list(range(30))
        rng.shuffle(values)
        for value in values:
            first.insert(rbtree.Node(value))
            second.insert(rbtree.Node(value))
        self.assert_red_black_invariants(first)
        self.assert_red_black_invariants(second)

        rng.shuffle(values)
        remaining = set(values)
        for value in values:
            first.delete(first.search(value))
            remaining.remove(value)
            self.assert_red_black_invariants(first)
            self.assertEqual(
                [first.nth(i).key for i in range(1, len(remaining) + 1)],
                sorted(remaining),
            )
            self.assertTrue(
                all(second.nth(i).key == i - 1 for i in range(1, 31))
            )

    def test_red_black_interval_search(self):
        tree = rbtree.RbTree(callback=rbtree.max_node)
        for low, high in [(15, 20), (10, 30), (17, 19), (5, 20), (12, 15)]:
            tree.insert(rbtree.Node(rbtree.Interval(low, high)))
        match = rbtree.interval_search(tree, rbtree.Interval(14, 16))
        self.assertIsNot(match, tree.nil)
        self.assertTrue(rbtree.overlap(match.key, rbtree.Interval(14, 16)))

    def test_binary_tree_traversal_and_deletion(self):
        root = binarytree.TreeNode(5)
        root.insert_nonrec(4)
        root.insert_nonrec(6)
        self.assertIs(root.left.p, root)
        self.assertIs(root.right.p, root)
        with self.assertRaises(ValueError):
            root.insert_nonrec(5)

        tree = binarytree.Tree()
        for value in [5, 3, 7, 2, 4, 6, 8]:
            tree.insert(value)
        ordered = []
        tree.root.inorder(lambda node: ordered.append(node.key))
        self.assertEqual(ordered, [2, 3, 4, 5, 6, 7, 8])
        traversals = (
            (tree.root.inorder_nonrec, [2, 3, 4, 5, 6, 7, 8]),
            (tree.root.preorder, [5, 3, 2, 4, 7, 6, 8]),
            (tree.root.preorder_nonrec, [5, 3, 2, 4, 7, 6, 8]),
            (tree.root.postorder, [2, 4, 3, 6, 8, 7, 5]),
            (tree.root.postorder_nonrec, [2, 4, 3, 6, 8, 7, 5]),
            (tree.root.postorer_nonrec, [2, 4, 3, 6, 8, 7, 5]),
        )
        for traversal, expected in traversals:
            result = []
            traversal(result.append)
            self.assertEqual(result, expected)
        repeated = []
        tree.root.inorder_nonrec(repeated.append)
        self.assertEqual(repeated, ordered)
        self.assertEqual(tree.root.min().key, 2)
        self.assertEqual(tree.root.max().key, 8)
        self.assertEqual(tree.root.left.right.predcessor().key, 3)
        self.assertEqual(tree.root.left.right.succesor().key, 5)
        tree.delete(tree.root)
        ordered.clear()
        tree.root.inorder(lambda node: ordered.append(node.key))
        self.assertEqual(ordered, [2, 3, 4, 6, 7, 8])

    def test_linked_list_operations(self):
        values = linked_list.LinkedList()
        self.assertTrue(values.is_empty())
        self.assertIsNone(values.pop_left())
        values.append("a")
        values.append("b")
        self.assertEqual(values.search("b").key, "b")
        self.assertEqual(values.pop_left(), "a")
        self.assertEqual(values.pop_left(), "b")
        self.assertTrue(values.is_empty())
        self.assertIsNone(values.search("missing"))

    def test_hash_table_collision_and_deletion(self):
        table = [None] * 5
        def hash_function(_key):
            return 0
        for key in ["a", "b", "c"]:
            hashing.hash_insert(table, hash_function, key, key.upper())
        self.assertEqual(
            hashing.hash_search(table, hash_function, "c"), ("c", "C")
        )
        self.assertEqual(
            hashing.hash_delete(table, hash_function, "b"), ("b", "B")
        )
        self.assertIsNone(hashing.hash_search(table, hash_function, "b"))
        self.assertEqual(
            hashing.hash_search(table, hash_function, "c"), ("c", "C")
        )
        self.assertIsNone(hashing.hash_delete(table, hash_function, "missing"))

    def test_hashing_functions_and_full_table_deletion(self):
        self.assertEqual(hashing.hash_division(17, 5), 2)
        self.assertEqual(hashing.hash_multiplication(5, 0.5, 8), 4)
        self.assertEqual(hashing.hash_multiply_shift(5, 3, 4, 2), 3)
        hash_function = hashing.hash_suite(101)
        self.assertEqual(hash_function(9), hash_function(9))
        with self.assertRaises(ValueError):
            hashing.hash_suite(1)
        with self.assertRaises(ValueError):
            hashing.hash_division(1, 0)

        table = [None] * 3

        def colliding_hash(_key):
            return 0

        for key in range(3):
            hashing.hash_insert(table, colliding_hash, key, key)
        self.assertEqual(hashing.hash_delete(table, colliding_hash, 1), (1, 1))
        self.assertEqual(
            hashing.hash_search(table, colliding_hash, 2), (2, 2)
        )


class DynamicAndGreedyTests(unittest.TestCase):
    def test_dynamic_programming(self):
        self.assertEqual(dynamic_programming.rod_cutting_rec(4)[0], 10)
        self.assertEqual(dynamic_programming.rod_cutting_dp(4)[4], 10)
        self.assertEqual(
            dynamic_programming.rod_cutting_rec(12)[0],
            dynamic_programming.rod_cutting_dp(12)[12],
        )
        self.assertEqual(
            sum(dynamic_programming.rod_cutting_rec(12)[1]), 12
        )
        with self.assertRaises(ValueError):
            dynamic_programming.rod_cutting_dp(-1)
        sequence = dynamic_programming.longest_common_subsequence(
            "ABCBDAB", "BDCABA"
        )
        self.assertEqual(len(sequence), 4)
        self.assertTrue(all(c in "ABCBDAB" for c in sequence))

    def test_activity_selection_and_huffman(self):
        self.assertEqual(greedy.selection([], []), [])
        self.assertEqual(greedy.huffman({}), [])
        starts = [1, 3, 0, 5, 8, 5]
        finishes = [2, 4, 6, 7, 9, 9]
        selected = greedy.selection(starts, finishes)
        self.assertEqual(len(selected), 4)
        self.assertTrue(
            all(selected[i][1] <= selected[i + 1][0] for i in range(3))
        )

        frequencies = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
        codes = dict(greedy.huffman(frequencies))
        self.assertEqual(set(codes), {"a", "b", "c", "d", "e", "f"})
        for symbol, code in codes.items():
            self.assertTrue(
                all(
                    symbol == other or not other_code.startswith(code)
                    for other, other_code in codes.items()
                )
            )

    def test_probability_functions(self):
        self.assertEqual(probability.permutations(5, 3), 60)
        self.assertEqual(probability.combinations(5, 2), 10)
        self.assertEqual(probability.multinomial_coefficient(5, 2, 3), 10)
        with self.assertRaises(ValueError):
            probability.combinations(2, 3)
        with self.assertRaises(ValueError):
            probability.multinomial_coefficient(5, 2, 2)


if __name__ == "__main__":
    unittest.main()
