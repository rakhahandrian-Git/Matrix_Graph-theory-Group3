"""
Unit and verification tests for graph_core algorithms.
"""

import unittest
from graph_core import Graph


class TestGraphCore(unittest.TestCase):

    def test_slide_4_undirected(self):
        # 5 vertices
        # A = [
        #  [0, 1, 0, 1, 1],
        #  [1, 0, 1, 1, 1],
        #  [0, 1, 0, 0, 1],
        #  [1, 1, 0, 0, 1],
        #  [1, 1, 1, 1, 0]
        # ]
        adj = [
            [0, 1, 0, 1, 1],
            [1, 0, 1, 1, 1],
            [0, 1, 0, 0, 1],
            [1, 1, 0, 0, 1],
            [1, 1, 1, 1, 0]
        ]
        g = Graph.from_adjacency_matrix(adj, is_directed=False)
        self.assertEqual(len(g.vertices), 5)
        self.assertEqual(len(g.edges), 8)

        v_names, reconstructed = g.get_adjacency_matrix()
        self.assertEqual(adj, [[int(x) for x in row] for row in reconstructed])

    def test_slide_4_directed(self):
        adj = [
            [0, 1, 0, 1, 0],
            [0, 0, 0, 1, 1],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0]
        ]
        g = Graph.from_adjacency_matrix(adj, is_directed=True)
        self.assertEqual(len(g.vertices), 5)
        self.assertEqual(len(g.edges), 8)
        v_names, reconstructed = g.get_adjacency_matrix()
        self.assertEqual(adj, [[int(x) for x in row] for row in reconstructed])

    def test_slide_6_incidence_digraph(self):
        # 4 vertices, 4 edges
        # Col 1: 1 -> 2
        # Col 2: 2 -> 4
        # Col 3: 4 -> 3
        # Col 4: 3 -> 1
        inc = [
            [ 1,  0,  0, -1],
            [-1,  1,  0,  0],
            [ 0,  0, -1,  1],
            [ 0, -1,  1,  0]
        ]
        g = Graph.from_incidence_matrix(inc, is_directed=True)
        self.assertEqual(len(g.vertices), 4)
        self.assertEqual(len(g.edges), 4)
        _, _, reconstructed = g.get_incidence_matrix()
        self.assertEqual(inc, [[int(x) for x in row] for row in reconstructed])

    def test_exercise_1(self):
        # Architecture: A–B, B–C, B–E, C–D, C–E, D–E, D–F, E–F
        nodes = ['A', 'B', 'C', 'D', 'E', 'F']
        g = Graph(is_directed=False)
        for n in nodes:
            g.add_vertex(n)
        edges = [
            ('A', 'B'), ('B', 'C'), ('B', 'E'),
            ('C', 'D'), ('C', 'E'),
            ('D', 'E'), ('D', 'F'),
            ('E', 'F')
        ]
        for u, v in edges:
            g.add_edge(u, v)

        self.assertEqual(len(g.edges), 8)
        degrees = {v: len(g.get_neighbors(v)) for v in nodes}
        self.assertEqual(degrees['E'], 4)
        self.assertEqual(degrees['A'], 1)
        self.assertEqual(degrees['F'], 2)

        fund_cycle = g.compute_fundamental_cycle_matrix()
        # n = 6, m = 8 => mu = 8 - (6 - 1) = 3 fundamental cycles
        self.assertEqual(fund_cycle['mu'], 3)
        self.assertEqual(fund_cycle['rank'], 5)

        fund_cutset = g.compute_fundamental_cutset_matrix()
        # rank = n - 1 = 5 fundamental cutsets
        self.assertEqual(len(fund_cutset['cutsets']), 5)

    def test_exercise_2(self):
        # Data center network
        # V = {1, 2, 3, 4, 5}
        # E = {(1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5)}
        g = Graph(is_directed=False)
        for v in ['1', '2', '3', '4', '5']:
            g.add_vertex(v)
        edges = [('1', '2'), ('1', '3'), ('2', '3'), ('2', '4'), ('3', '5'), ('4', '5')]
        for u, v in edges:
            g.add_edge(u, v)

        # n = 5, m = 6 => mu = 6 - (5 - 1) = 2 fundamental cycles
        fund_cycle = g.compute_fundamental_cycle_matrix()
        self.assertEqual(fund_cycle['mu'], 2)
        self.assertEqual(fund_cycle['rank'], 4)

        # Check bridge / cut-edge count
    def test_slide_10_cutsets(self):
        # Graph G1 from Slide 10:
        # v3 -e8- v2
        # v2 -e6- v1
        # v2 -e5- v4
        # v2 -e7- v5
        # v1 -e4- v5
        # v4 -e3- v5
        # v4 -e1- v6
        # v4 -e2- v6 (parallel edge)
        g = Graph(is_directed=False)
        for v in ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']:
            g.add_vertex(v)
        g.add_edge('v4', 'v6', 'e1')
        g.add_edge('v4', 'v6', 'e2')
        g.add_edge('v4', 'v5', 'e3')
        g.add_edge('v1', 'v5', 'e4')
        g.add_edge('v2', 'v4', 'e5')
        g.add_edge('v2', 'v1', 'e6')
        g.add_edge('v2', 'v5', 'e7')
        g.add_edge('v3', 'v2', 'e8')

        cuts_result = g.compute_all_minimal_cutsets()
        cut_edge_sets = [set(c['edges']) for c in cuts_result['cutsets']]

        expected_cuts = [
            {'e8'},
            {'e1', 'e2'},
            {'e3', 'e5'},
            {'e4', 'e6'},
            {'e5', 'e6', 'e7'},
            {'e3', 'e6', 'e7'},
            {'e3', 'e4', 'e7'},
            {'e4', 'e5', 'e7'}
        ]

        self.assertEqual(len(cut_edge_sets), len(expected_cuts))
        for exp in expected_cuts:
            self.assertIn(exp, cut_edge_sets)


if __name__ == '__main__':
    unittest.main()
