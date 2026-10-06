"""
Graph Matrix Representation & Analysis Core Engine
Implements graph structures, adjacency/incidence parsing, spanning trees,
fundamental cycle matrices, and cut-set matrices.
"""

from collections import deque
from itertools import combinations
from typing import List, Dict, Tuple, Set, Optional, Any


class Graph:
    def __init__(self, is_directed: bool = False):
        self.is_directed = is_directed
        self.vertices: List[str] = []
        self.vertex_indices: Dict[str, int] = {}
        # edges: list of dicts: {'id': 'e1', 'u': 'v1', 'v': 'v2', 'weight': 1.0}
        self.edges: List[Dict[str, Any]] = []

    def add_vertex(self, name: str) -> None:
        if name not in self.vertex_indices:
            self.vertex_indices[name] = len(self.vertices)
            self.vertices.append(name)

    def add_edge(self, u: str, v: str, edge_id: Optional[str] = None, weight: float = 1.0) -> str:
        self.add_vertex(u)
        self.add_vertex(v)
        if not edge_id:
            edge_id = f"e{len(self.edges) + 1}"
        self.edges.append({
            'id': edge_id,
            'u': u,
            'v': v,
            'weight': weight
        })
        return edge_id

    @classmethod
    def from_adjacency_matrix(
        cls,
        matrix: List[List[float]],
        vertex_labels: Optional[List[str]] = None,
        is_directed: bool = False
    ) -> 'Graph':
        n = len(matrix)
        for row in matrix:
            if len(row) != n:
                raise ValueError("Adjacency matrix must be square (N x N).")

        g = cls(is_directed=is_directed)
        if not vertex_labels or len(vertex_labels) != n:
            vertex_labels = [f"v{i + 1}" for i in range(n)]

        for v in vertex_labels:
            g.add_vertex(v)

        edge_count = 1
        if is_directed:
            for i in range(n):
                for j in range(n):
                    val = matrix[i][j]
                    if val != 0:
                        g.add_edge(vertex_labels[i], vertex_labels[j], f"e{edge_count}", weight=val)
                        edge_count += 1
        else:
            for i in range(n):
                for j in range(i, n):
                    val = matrix[i][j]
                    if i == j and val != 0:
                        # self loop
                        g.add_edge(vertex_labels[i], vertex_labels[j], f"e{edge_count}", weight=val)
                        edge_count += 1
                    elif i < j:
                        # For undirected, could be multigraph if integer > 1
                        int_val = int(round(val)) if abs(val - round(val)) < 1e-6 else 1
                        if int_val > 0 and abs(val - 1.0) < 1e-6:
                            g.add_edge(vertex_labels[i], vertex_labels[j], f"e{edge_count}", weight=val)
                            edge_count += 1
                        elif val != 0:
                            # weighted or multigraph
                            for _ in range(max(1, int_val if abs(val - int_val) < 1e-6 else 1)):
                                g.add_edge(vertex_labels[i], vertex_labels[j], f"e{edge_count}", weight=val)
                                edge_count += 1
        return g

    @classmethod
    def from_incidence_matrix(
        cls,
        matrix: List[List[float]],
        vertex_labels: Optional[List[str]] = None,
        edge_labels: Optional[List[str]] = None,
        is_directed: bool = False
    ) -> 'Graph':
        n = len(matrix)
        if n == 0:
            raise ValueError("Incidence matrix cannot be empty.")
        m = len(matrix[0])
        for row in matrix:
            if len(row) != m:
                raise ValueError("All rows in incidence matrix must have the same length.")

        g = cls(is_directed=is_directed)
        if not vertex_labels or len(vertex_labels) != n:
            vertex_labels = [f"v{i + 1}" for i in range(n)]
        if not edge_labels or len(edge_labels) != m:
            edge_labels = [f"e{j + 1}" for j in range(m)]

        for v in vertex_labels:
            g.add_vertex(v)

        for j in range(m):
            col = [matrix[i][j] for i in range(n)]
            non_zeros = [(i, col[i]) for i in range(n) if col[i] != 0]

            if is_directed:
                # 1 = leaving vertex, -1 = arriving vertex (per Week 5 Slide 6)
                pos = [i for i, val in non_zeros if val > 0]
                neg = [i for i, val in non_zeros if val < 0]
                if len(pos) == 1 and len(neg) == 1:
                    u = vertex_labels[pos[0]]
                    v = vertex_labels[neg[0]]
                    weight = abs(col[pos[0]])
                    g.add_edge(u, v, edge_labels[j], weight=weight)
                elif len(non_zeros) == 1:
                    # self loop
                    u = vertex_labels[non_zeros[0][0]]
                    g.add_edge(u, u, edge_labels[j], weight=abs(non_zeros[0][1]))
                else:
                    raise ValueError(f"Column {j + 1} ({edge_labels[j]}) is not a valid directed edge (+1 leaving, -1 entering).")
            else:
                if len(non_zeros) == 2:
                    u = vertex_labels[non_zeros[0][0]]
                    v = vertex_labels[non_zeros[1][0]]
                    weight = non_zeros[0][1]
                    g.add_edge(u, v, edge_labels[j], weight=weight)
                elif len(non_zeros) == 1:
                    u = vertex_labels[non_zeros[0][0]]
                    weight = non_zeros[0][1]
                    g.add_edge(u, u, edge_labels[j], weight=weight)
                else:
                    raise ValueError(f"Column {j + 1} ({edge_labels[j]}) must connect exactly 2 vertices (or 1 for a loop).")

        return g

    def get_adjacency_matrix(self) -> Tuple[List[str], List[List[float]]]:
        n = len(self.vertices)
        mat = [[0.0 for _ in range(n)] for _ in range(n)]
        for edge in self.edges:
            u_idx = self.vertex_indices[edge['u']]
            v_idx = self.vertex_indices[edge['v']]
            w = edge['weight']
            if self.is_directed:
                mat[u_idx][v_idx] = w
            else:
                mat[u_idx][v_idx] = w
                mat[v_idx][u_idx] = w
        return self.vertices, mat

    def get_incidence_matrix(self) -> Tuple[List[str], List[str], List[List[float]]]:
        n = len(self.vertices)
        m = len(self.edges)
        edge_ids = [e['id'] for e in self.edges]
        mat = [[0.0 for _ in range(m)] for _ in range(n)]

        for j, edge in enumerate(self.edges):
            u_idx = self.vertex_indices[edge['u']]
            v_idx = self.vertex_indices[edge['v']]
            w = edge['weight']
            if self.is_directed:
                if u_idx == v_idx:
                    mat[u_idx][j] = 0.0 # self loop
                else:
                    mat[u_idx][j] = w   # leaving
                    mat[v_idx][j] = -w  # arriving
            else:
                if u_idx == v_idx:
                    mat[u_idx][j] = 2.0 * w
                else:
                    mat[u_idx][j] = w
                    mat[v_idx][j] = w
        return self.vertices, edge_ids, mat

    def get_neighbors(self, vertex: str) -> List[Tuple[str, str, Dict[str, Any]]]:
        """Returns list of (neighbor_vertex, direction, edge_data)"""
        res = []
        for edge in self.edges:
            if edge['u'] == vertex:
                res.append((edge['v'], 'outgoing', edge))
            elif not self.is_directed and edge['v'] == vertex:
                res.append((edge['u'], 'incoming', edge))
            elif self.is_directed and edge['v'] == vertex:
                res.append((edge['u'], 'incoming', edge))
        return res

    def get_connected_components(self) -> List[List[str]]:
        visited = set()
        components = []
        for v in self.vertices:
            if v not in visited:
                comp = []
                queue = deque([v])
                visited.add(v)
                while queue:
                    curr = queue.popleft()
                    comp.append(curr)
                    # For connectivity, treat edges as undirected
                    for edge in self.edges:
                        other = None
                        if edge['u'] == curr and edge['v'] not in visited:
                            other = edge['v']
                        elif edge['v'] == curr and edge['u'] not in visited:
                            other = edge['u']
                        if other:
                            visited.add(other)
                            queue.append(other)
                components.append(comp)
        return components

    def find_spanning_forest(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Computes a spanning forest/tree.
        Returns:
            tree_edges (branches), non_tree_edges (chords)
        """
        # Disjoint set / union-find
        parent = {v: v for v in self.vertices}

        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]

        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False

        branches: List[Dict[str, Any]] = []
        chords: List[Dict[str, Any]] = []

        for edge in self.edges:
            u, v = edge['u'], edge['v']
            if u != v and union(u, v):
                branches.append(edge)
            else:
                chords.append(edge)

        return branches, chords

    def get_path_in_tree(self, tree_edges: List[Dict[str, Any]], start: str, end: str) -> Optional[List[Dict[str, Any]]]:
        """Finds unique simple path between start and end in the spanning tree."""
        if start == end:
            return []

        adj: Dict[str, List[Tuple[str, Dict[str, Any]]]] = {v: [] for v in self.vertices}
        for edge in tree_edges:
            adj[edge['u']].append((edge['v'], edge))
            adj[edge['v']].append((edge['u'], edge))

        queue = deque([(start, [])])
        visited = {start}

        while queue:
            curr, path = queue.popleft()
            if curr == end:
                return path
            for nxt, edge in adj[curr]:
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, path + [edge]))
        return None

    def compute_fundamental_cycle_matrix(self) -> Dict[str, Any]:
        """
        Computes the Fundamental Cycle Matrix B_f with respect to a spanning tree.
        Column ordering: Chords first, then Branches (as in Slide 9: [I_mu | B_ft]).
        """
        branches, chords = self.find_spanning_forest()
        all_ordered_edges = chords + branches
        edge_id_to_idx = {e['id']: idx for idx, e in enumerate(all_ordered_edges)}

        cycle_list = []
        matrix = []

        for i, chord in enumerate(chords):
            u, v = chord['u'], chord['v']
            path = self.get_path_in_tree(branches, u, v)
            if path is None:
                # Different components or self-loop
                cycle_edges = [chord]
            else:
                cycle_edges = [chord] + path

            cycle_id = f"Z{i + 1}"
            edge_ids = [e['id'] for e in cycle_edges]
            cycle_list.append({
                'cycle_id': cycle_id,
                'chord': chord['id'],
                'edges': edge_ids
            })

            row = [0] * len(all_ordered_edges)
            for e in cycle_edges:
                row[edge_id_to_idx[e['id']]] = 1
            matrix.append(row)

        return {
            'branches': [e['id'] for e in branches],
            'chords': [e['id'] for e in chords],
            'columns': [e['id'] for e in all_ordered_edges],
            'cycle_names': [c['cycle_id'] for c in cycle_list],
            'cycles': cycle_list,
            'matrix': matrix,
            'mu': len(chords),
            'rank': len(branches)
        }

    def compute_fundamental_cutset_matrix(self) -> Dict[str, Any]:
        """
        Computes Fundamental Cut-Set Matrix Q_f with respect to the spanning tree.
        For each tree branch, removing it partitions the tree into two sets V1 and V2.
        The cut-set is all edges in G connecting V1 and V2.
        Columns: Chords first, then Branches: [Q_fc | I_(n-1)]
        """
        branches, chords = self.find_spanning_forest()
        all_ordered_edges = chords + branches
        edge_id_to_idx = {e['id']: idx for idx, e in enumerate(all_ordered_edges)}

        cutsets = []
        matrix = []

        for i, branch in enumerate(branches):
            # Spanning tree without this branch
            remaining_tree = [b for b in branches if b['id'] != branch['id']]
            # Find component containing branch['u']
            adj: Dict[str, List[str]] = {v: [] for v in self.vertices}
            for e in remaining_tree:
                adj[e['u']].append(e['v'])
                adj[e['v']].append(e['u'])

            v1 = set()
            queue = deque([branch['u']])
            v1.add(branch['u'])
            while queue:
                curr = queue.popleft()
                for nxt in adj[curr]:
                    if nxt not in v1:
                        v1.add(nxt)
                        queue.append(nxt)

            # All edges with one endpoint in v1 and one outside v1
            cut_edges = []
            for e in self.edges:
                u_in = e['u'] in v1
                v_in = e['v'] in v1
                if u_in != v_in:
                    cut_edges.append(e)

            cut_id = f"S{i + 1}"
            cutsets.append({
                'cut_id': cut_id,
                'branch': branch['id'],
                'partition_v1': sorted(list(v1)),
                'partition_v2': sorted([v for v in self.vertices if v not in v1]),
                'edges': [e['id'] for e in cut_edges]
            })

            row = [0] * len(all_ordered_edges)
            for e in cut_edges:
                row[edge_id_to_idx[e['id']]] = 1
            matrix.append(row)

        return {
            'branches': [e['id'] for e in branches],
            'chords': [e['id'] for e in chords],
            'columns': [e['id'] for e in all_ordered_edges],
            'cut_names': [c['cut_id'] for c in cutsets],
            'cutsets': cutsets,
            'matrix': matrix
        }

    def compute_all_minimal_cutsets(self) -> Dict[str, Any]:
        """
        Enumerates all minimal cut-sets of the graph (as shown in Slide 10: c1, c2, ...).
        A minimal cut-set is an edge cut (S, V - S) where both G[S] and G[V - S] are connected.
        """
        n = len(self.vertices)
        if n <= 1:
            return {'columns': [e['id'] for e in self.edges], 'cut_names': [], 'cutsets': [], 'matrix': []}

        # Subsets of vertices containing vertex 0 to avoid duplicates (S and V - S)
        all_v = set(self.vertices)
        v0 = self.vertices[0]
        other_v = self.vertices[1:]

        def is_connected_subgraph(node_subset: Set[str]) -> bool:
            if not node_subset:
                return False
            nodes_list = list(node_subset)
            visited = {nodes_list[0]}
            queue = deque([nodes_list[0]])
            adj = {v: [] for v in node_subset}
            for e in self.edges:
                if e['u'] in node_subset and e['v'] in node_subset:
                    adj[e['u']].append(e['v'])
                    adj[e['v']].append(e['u'])

            while queue:
                curr = queue.popleft()
                for nxt in adj[curr]:
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append(nxt)
            return len(visited) == len(node_subset)

        cutsets = []
        seen_edge_sets = set()
        columns = [e['id'] for e in self.edges]
        edge_id_to_idx = {e['id']: idx for idx, e in enumerate(self.edges)}

        # Iterate through all non-empty proper subsets of vertices containing v0
        for r in range(len(other_v) + 1):
            for combo in combinations(other_v, r):
                s = {v0} | set(combo)
                vs = all_v - s
                if not vs:
                    continue

                # Check if G[S] and G[V - S] are connected
                if is_connected_subgraph(s) and is_connected_subgraph(vs):
                    # Cut edges
                    cut_edges = []
                    for e in self.edges:
                        if (e['u'] in s and e['v'] in vs) or (e['u'] in vs and e['v'] in s):
                            cut_edges.append(e['id'])

                    cut_edges_sorted = tuple(sorted(cut_edges))
                    if cut_edges_sorted and cut_edges_sorted not in seen_edge_sets:
                        seen_edge_sets.add(cut_edges_sorted)
                        cutsets.append({
                            'cut_id': f"c{len(cutsets) + 1}",
                            'partition_v1': sorted(list(s)),
                            'partition_v2': sorted(list(vs)),
                            'edges': list(cut_edges_sorted)
                        })

        # Sort cutsets by size, then by edge IDs
        cutsets.sort(key=lambda c: (len(c['edges']), c['edges']))
        for i, c in enumerate(cutsets):
            c['cut_id'] = f"c{i + 1}"

        matrix = []
        for c in cutsets:
            row = [0] * len(columns)
            for eid in c['edges']:
                row[edge_id_to_idx[eid]] = 1
            matrix.append(row)

        return {
            'columns': columns,
            'cut_names': [c['cut_id'] for c in cutsets],
            'cutsets': cutsets,
            'matrix': matrix
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serializes graph and all matrices for frontend/API consumption."""
        adj_v, adj_mat = self.get_adjacency_matrix()
        inc_v, inc_e, inc_mat = self.get_incidence_matrix()
        fund_cycle = self.compute_fundamental_cycle_matrix()
        fund_cutset = self.compute_fundamental_cutset_matrix()
        all_cutsets = self.compute_all_minimal_cutsets()

        # Vertex degrees
        degrees = {}
        for v in self.vertices:
            neighbors = self.get_neighbors(v)
            degrees[v] = len(neighbors)

        return {
            'is_directed': self.is_directed,
            'vertices': self.vertices,
            'edges': self.edges,
            'degrees': degrees,
            'adjacency_matrix': {
                'vertices': adj_v,
                'matrix': adj_mat
            },
            'incidence_matrix': {
                'vertices': inc_v,
                'edges': inc_e,
                'matrix': inc_mat
            },
            'fundamental_cycle_matrix': fund_cycle,
            'fundamental_cutset_matrix': fund_cutset,
            'all_cutset_matrix': all_cutsets
        }
