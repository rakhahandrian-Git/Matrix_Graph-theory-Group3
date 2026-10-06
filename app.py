"""
Flask Web Application for Graph Matrix Representation & Visualizer
Week 5 Graph Theory - Institut Teknologi Sepuluh Nopember
"""

import os
import sys
import webbrowser
from flask import Flask, render_template, request, jsonify
from graph_core import Graph

app = Flask(__name__, static_folder='static', template_folder='templates')


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
        "name": "Week 5 Slide 9 - Fundamental Cycles (5 vertices, 7 edges)",
        "type": "edges",
        "directed": False,
        "nodes": ["v1", "v2", "v3", "v4", "v5"],
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
        "name": "Week 5 Slide 10 - Cut-Set Matrix G1 (6 vertices, 8 edges)",
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/presets', methods=['GET'])
def get_presets():
    return jsonify(PRESETS)


@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    matrix_type = data.get('matrix_type', 'adj')
    is_directed = bool(data.get('is_directed', False))
    raw_matrix = data.get('matrix', [])
    vertex_labels = data.get('vertex_labels')
    edge_labels = data.get('edge_labels')

    if not raw_matrix:
        return jsonify({'error': 'Matrix data is required.'}), 400

    try:
        matrix = [[float(val) for val in row] for row in raw_matrix]
        if matrix_type == 'adj':
            g = Graph.from_adjacency_matrix(matrix, vertex_labels=vertex_labels, is_directed=is_directed)
        elif matrix_type == 'inc':
            g = Graph.from_incidence_matrix(matrix, vertex_labels=vertex_labels, edge_labels=edge_labels, is_directed=is_directed)
        else:
            return jsonify({'error': f'Invalid matrix type: {matrix_type}'}), 400

        res = g.to_dict()
        return jsonify(res)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/preset/<key>', methods=['GET'])
def load_preset(key):
    if key not in PRESETS:
        return jsonify({'error': 'Preset not found'}), 404
    p = PRESETS[key]
    try:
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
        res = g.to_dict()
        res['preset_info'] = p
        return jsonify(res)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Graph Matrix Visualizer on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
