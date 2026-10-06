#!/usr/bin/env python3
"""
Graph Visualizer & Matrix Analysis CLI
Terminal tool for computing Adjacency, Incidence, Fundamental Cycle, and Cut-Set matrices.
"""

import argparse
import sys
from typing import List
from graph_core import Graph


PRESETS = {
    "slide4_undirected": {
        "name": "Week 5 Slide 4 - Undirected Graph",
        "type": "adj",
        "directed": False,
        "nodes": ["1", "2", "3", "4", "5"],
        "matrix": [
            [0, 1, 0, 1, 1],
            [1, 0, 1, 1, 1],
            [0, 1, 0, 0, 1],
            [1, 1, 0, 0, 1],
            [1, 1, 1, 1, 0]
        ]
    },
    "slide4_directed": {
        "name": "Week 5 Slide 4 - Digraph",
        "type": "adj",
        "directed": True,
        "nodes": ["1", "2", "3", "4", "5"],
        "matrix": [
            [0, 1, 0, 1, 0],
            [0, 0, 0, 1, 1],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0]
        ]
    },
    "slide6_digraph": {
        "name": "Week 5 Slide 6 - Directed Incidence Matrix",
        "type": "inc",
        "directed": True,
        "nodes": ["1", "2", "3", "4"],
        "edges": ["e1", "e2", "e3", "e4"],
        "matrix": [
            [ 1,  0,  0, -1],
            [-1,  1,  0,  0],
            [ 0,  0, -1,  1],
            [ 0, -1,  1,  0]
        ]
    },
    "slide9_cycles": {
        "name": "Week 5 Slide 9 - Fundamental Cycles Example",
        "type": "edges",
        "directed": False,
        "nodes": ["v1", "v2", "v3", "v4", "v5"],
        # Graph with 5 nodes, 7 edges where chords are e2, e3, e6, tree: e1, e4, e5, e7
        "edges_list": [
            ("v4", "v5", "e1"),
            ("v1", "v5", "e2"),
            ("v2", "v4", "e3"),
            ("v1", "v2", "e4"),
            ("v2", "v3", "e5"),
            ("v3", "v4", "e6"),
            ("v2", "v4", "e7")
        ]
    },
    "slide10_cutsets": {
        "name": "Slide 10 - Cut-Set Matrix (Graph G₁)",
        "type": "edges",
        "directed": False,
        "nodes": ["v1", "v2", "v3", "v4", "v5", "v6"],
        "edges_list": [
            ("v4", "v6", "e1"),
            ("v4", "v6", "e2"),
            ("v4", "v5", "e3"),
            ("v1", "v5", "e4"),
            ("v2", "v4", "e5"),
            ("v2", "v1", "e6"),
            ("v2", "v5", "e7"),
            ("v3", "v2", "e8")
        ]
    },
    "exercise1": {
        "name": "Week 5 Slide 12 - Exercise 1 (AI Service Architecture)",
        "type": "edges",
        "directed": False,
        "nodes": ["A", "B", "C", "D", "E", "F"],
        "edges_list": [
            ("A", "B", "e1"),
            ("B", "C", "e2"),
            ("B", "E", "e3"),
            ("C", "D", "e4"),
            ("C", "E", "e5"),
            ("D", "E", "e6"),
            ("D", "F", "e7"),
            ("E", "F", "e8")
        ]
    },
    "exercise2": {
        "name": "Week 5 Slide 13 - Exercise 2 (Data Centers Network)",
        "type": "edges",
        "directed": False,
        "nodes": ["1", "2", "3", "4", "5"],
        "edges_list": [
            ("1", "2", "e1"),
            ("1", "3", "e2"),
            ("2", "3", "e3"),
            ("2", "4", "e4"),
            ("3", "5", "e5"),
            ("4", "5", "e6")
        ]
    }
}


def print_matrix(row_labels: List[str], col_labels: List[str], matrix: List[List[Any]], title: str):
    print(f"\n--- {title} ---")
    if not matrix or not row_labels or not col_labels:
        print("(empty)")
        return

    col_widths = [max(len(str(c)), 3) for c in col_labels]
    row_label_width = max(len(str(r)) for r in row_labels)

    # Header
    header = " " * (row_label_width + 2) + " ".join(f"{c:>{col_widths[i]}}" for i, c in enumerate(col_labels))
    print(header)
    print(" " * (row_label_width + 2) + "-" * (sum(col_widths) + len(col_widths) - 1))

    # Rows
    for r_idx, row in enumerate(matrix):
        row_str = f"{row_labels[r_idx]:<{row_label_width}} | "
        vals = []
        for c_idx, val in enumerate(row):
            if isinstance(val, float):
                v_str = f"{int(val)}" if val.is_integer() else f"{val:.1f}"
            else:
                v_str = str(val)
            vals.append(f"{v_str:>{col_widths[c_idx]}}")
        row_str += " ".join(vals)
        print(row_str)


def analyze_and_print(graph: Graph, title: str = "Graph Analysis"):
    print("=" * 70)
    print(f" {title.upper()} ")
    print("=" * 70)

    print(f"Vertices ({len(graph.vertices)}): {', '.join(graph.vertices)}")
    print(f"Edges ({len(graph.edges)}):")
    for e in graph.edges:
        arrow = "->" if graph.is_directed else "--"
        print(f"  {e['id']}: {e['u']} {arrow} {e['v']} (weight={e['weight']})")

    # Degrees
    print("\nVertex Degrees:")
    for v in graph.vertices:
        deg = len(graph.get_neighbors(v))
        print(f"  deg({v}) = {deg}")

    # Adjacency Matrix
    adj_v, adj_m = graph.get_adjacency_matrix()
    print_matrix(adj_v, adj_v, adj_m, "Adjacency Matrix A")

    # Incidence Matrix
    inc_v, inc_e, inc_m = graph.get_incidence_matrix()
    print_matrix(inc_v, inc_e, inc_m, "Incidence Matrix M")

    if not graph.is_directed:
        # Spanning Tree
        branches, chords = graph.find_spanning_forest()
        print("\n--- Spanning Tree Partition ---")
        print(f"Tree Branches (T): {[b['id'] for b in branches]}")
        print(f"Chords (Non-Tree): {[c['id'] for c in chords]}")

        # Fundamental Cycle Matrix
        fund_cycle = graph.compute_fundamental_cycle_matrix()
        print(f"\n--- Fundamental Cycles (Nullity mu = {fund_cycle['mu']}) ---")
        for c in fund_cycle['cycles']:
            print(f"  {c['cycle_id']} (Chord {c['chord']}): {', '.join(c['edges'])}")
        print_matrix(fund_cycle['cycle_names'], fund_cycle['columns'], fund_cycle['matrix'], "Fundamental Cycle Matrix B_f = [I_mu | B_ft]")

        # Fundamental Cut-Set Matrix
        fund_cut = graph.compute_fundamental_cutset_matrix()
        print(f"\n--- Fundamental Cut-Sets (Rank = {len(branches)}) ---")
        for c in fund_cut['cutsets']:
            print(f"  {c['cut_id']} (Branch {c['branch']}): {', '.join(c['edges'])} | Partition: {c['partition_v1']} vs {c['partition_v2']}")
        print_matrix(fund_cut['cut_names'], fund_cut['columns'], fund_cut['matrix'], "Fundamental Cut-Set Matrix Q_f = [Q_fc | I_(n-1)]")

        # All Minimal Cut-Sets
        all_cuts = graph.compute_all_minimal_cutsets()
        print(f"\n--- All Minimal Cut-Sets (Total = {len(all_cuts['cutsets'])}) ---")
        for c in all_cuts['cutsets']:
            print(f"  {c['cut_id']}: {{{', '.join(c['edges'])}}} | Partition: {c['partition_v1']} vs {c['partition_v2']}")
        print_matrix(all_cuts['cut_names'], all_cuts['columns'], all_cuts['matrix'], "All Minimal Cut-Sets Matrix C(G)")

    print("\n" + "=" * 70)


def parse_matrix_string(text: str) -> List[List[float]]:
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    matrix = []
    for line in lines:
        cleaned = line.replace('[', '').replace(']', '').replace(',', ' ').replace(';', ' ')
        row = [float(val) for val in cleaned.split()]
        if row:
            matrix.append(row)
    return matrix


def main():
    parser = argparse.ArgumentParser(description="Graph Theory Matrix Analyzer & Visualizer CLI")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), help="Run a built-in course preset")
    parser.add_argument("--type", choices=["adj", "inc"], help="Matrix type (adj = adjacency, inc = incidence)")
    parser.add_argument("--directed", action="store_true", help="Treat graph as directed")
    parser.add_argument("--matrix", type=str, help="Matrix entries as string, e.g. '0 1; 1 0'")
    parser.add_argument("--file", type=str, help="Read matrix from text file")

    args = parser.parse_args()

    if args.preset:
        p = PRESETS[args.preset]
        if p["type"] == "adj":
            g = Graph.from_adjacency_matrix(p["matrix"], vertex_labels=p.get("nodes"), is_directed=p["directed"])
        elif p["type"] == "inc":
            g = Graph.from_incidence_matrix(p["matrix"], vertex_labels=p.get("nodes"), edge_labels=p.get("edges"), is_directed=p["directed"])
        elif p["type"] == "edges":
            g = Graph(is_directed=p["directed"])
            for v in p["nodes"]:
                g.add_vertex(v)
            for u, v, eid in p["edges_list"]:
                g.add_edge(u, v, eid)
        analyze_and_print(g, p["name"])
        return

    if not args.type and not args.matrix and not args.file:
        print("No input provided. Listing available presets:\n")
        for key, p in PRESETS.items():
            print(f"  --preset {key:<18} : {p['name']}")
        print("\nExample usage:")
        print("  python cli.py --preset exercise1")
        print("  python cli.py --preset exercise2")
        print("  python cli.py --preset slide10_cutsets")
        sys.exit(0)

    raw_text = args.matrix or ""
    if args.file:
        with open(args.file, "r") as f:
            raw_text = f.read()

    mat = parse_matrix_string(raw_text)
    if not mat:
        print("Error: Empty or unparseable matrix.")
        sys.exit(1)

    if args.type == "adj":
        g = Graph.from_adjacency_matrix(mat, is_directed=args.directed)
    elif args.type == "inc":
        g = Graph.from_incidence_matrix(mat, is_directed=args.directed)
    else:
        print("Please specify --type adj or --type inc.")
        sys.exit(1)

    analyze_and_print(g, "Custom Matrix Analysis")


if __name__ == "__main__":
    main()
