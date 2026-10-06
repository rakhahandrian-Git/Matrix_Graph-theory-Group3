/**
 * Graph Matrix Visualizer & Analyzer Engine
 * Front-end controller & Offline Client-side Solver
 */

// Presets registry
const PRESETS = {
  slide4_undirected: {
    name: "Slide 4 - Undirected Adjacency",
    type: "adj",
    directed: false,
    nodes: ["1", "2", "3", "4", "5"],
    matrix: [
      [0, 1, 0, 1, 1],
      [1, 0, 1, 1, 1],
      [0, 1, 0, 0, 1],
      [1, 1, 0, 0, 1],
      [1, 1, 1, 1, 0]
    ]
  },
  slide4_directed: {
    name: "Slide 4 - Directed Adjacency",
    type: "adj",
    directed: true,
    nodes: ["1", "2", "3", "4", "5"],
    matrix: [
      [0, 1, 0, 1, 0],
      [0, 0, 0, 1, 1],
      [0, 1, 0, 0, 0],
      [0, 0, 0, 0, 1],
      [1, 0, 1, 0, 0]
    ]
  },
  slide6_digraph: {
    name: "Slide 6 - Digraph Incidence Matrix",
    type: "inc",
    directed: true,
    nodes: ["1", "2", "3", "4"],
    edges: ["e1", "e2", "e3", "e4"],
    matrix: [
      [ 1,  0,  0, -1],
      [-1,  1,  0,  0],
      [ 0,  0, -1,  1],
      [ 0, -1,  1,  0]
    ]
  },
  slide9_cycles: {
    name: "Slide 9 - Fundamental Cycles Example",
    type: "edges",
    directed: false,
    nodes: ["v1", "v2", "v3", "v4", "v5"],
    edges_list: [
      { u: "v4", v: "v5", id: "e1" },
      { u: "v1", v: "v5", id: "e2" },
      { u: "v2", v: "v4", id: "e3" },
      { u: "v1", v: "v2", id: "e4" },
      { u: "v2", v: "v3", id: "e5" },
      { u: "v3", v: "v4", id: "e6" },
      { u: "v2", v: "v4", id: "e7" }
    ]
  },
  slide10_cutsets: {
    name: "Slide 10 - Cut-Set Matrix G1 (8 edges)",
    type: "edges",
    directed: false,
    nodes: ["v1", "v2", "v3", "v4", "v5", "v6"],
    edges_list: [
      { u: "v4", v: "v6", id: "e1" },
      { u: "v4", v: "v6", id: "e2" },
      { u: "v4", v: "v5", id: "e3" },
      { u: "v1", v: "v5", id: "e4" },
      { u: "v2", v: "v4", id: "e5" },
      { u: "v2", v: "v1", id: "e6" },
      { u: "v2", v: "v5", id: "e7" },
      { u: "v3", v: "v2", id: "e8" }
    ]
  },
  exercise1: {
    name: "Slide 12 - Exercise 1 (AI Service Architecture)",
    type: "edges",
    directed: false,
    nodes: ["A", "B", "C", "D", "E", "F"],
    edges_list: [
      { u: "A", v: "B", id: "e1" },
      { u: "B", v: "C", id: "e2" },
      { u: "B", v: "E", id: "e3" },
      { u: "C", v: "D", id: "e4" },
      { u: "C", v: "E", id: "e5" },
      { u: "D", v: "E", id: "e6" },
      { u: "D", v: "F", id: "e7" },
      { u: "E", v: "F", id: "e8" }
    ]
  },
  exercise2: {
    name: "Slide 13 - Exercise 2 (Data Centers Network)",
    type: "edges",
    directed: false,
    nodes: ["1", "2", "3", "4", "5"],
    edges_list: [
      { u: "1", v: "2", id: "e1" },
      { u: "1", v: "3", id: "e2" },
      { u: "2", v: "3", id: "e3" },
      { u: "2", v: "4", id: "e4" },
      { u: "3", v: "5", id: "e5" },
      { u: "4", v: "5", id: "e6" }
    ]
  }
};

// Application state
let currentNetwork = null;
let currentGraphData = null;
let activeHighlight = null; // { type: 'tree' | 'cycle' | 'cut', id: string }

// Initialization
document.addEventListener("DOMContentLoaded", () => {
  setupTabs();
  setupEventListeners();
  loadPreset("slide4_undirected");
});

function setupTabs() {
  const tabBtns = document.querySelectorAll(".tab-btn");
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      const targetPane = document.getElementById(btn.dataset.target);
      if (targetPane) targetPane.classList.add("active");
    });
  });
}

function setupEventListeners() {
  const presetSelect = document.getElementById("presetSelect");
  if (presetSelect) {
    presetSelect.addEventListener("change", (e) => {
      if (e.target.value) loadPreset(e.target.value);
    });
  }

  document.getElementById("btnAnalyze").addEventListener("click", () => {
    runAnalysisFromInputs();
  });

  document.querySelectorAll("input[name='matrixType']").forEach(elem => {
    elem.addEventListener("change", (e) => {
      updateInputLabels(e.target.value);
    });
  });

  document.getElementById("btnToggleTree").addEventListener("click", () => {
    if (activeHighlight && activeHighlight.type === "tree") {
      clearHighlight();
    } else {
      highlightSpanningTree();
    }
  });

  document.getElementById("btnResetView").addEventListener("click", () => {
    if (currentNetwork) currentNetwork.fit();
    clearHighlight();
  });

  document.getElementById("btnExportPng").addEventListener("click", exportGraphPng);
  document.getElementById("btnExportLatex").addEventListener("click", exportLatexModal);
}

function updateInputLabels(matrixType) {
  const label = document.getElementById("matrixLabel");
  const placeholder = document.getElementById("matrixInput");
  if (matrixType === "adj") {
    label.innerText = "Adjacency Matrix (N x N)";
    placeholder.placeholder = "0 1 0 1 1\n1 0 1 1 1\n0 1 0 0 1\n1 1 0 0 1\n1 1 1 1 0";
  } else {
    label.innerText = "Incidence Matrix (N vertices x M edges)";
    placeholder.placeholder = "1  0  0 -1\n-1 1  0  0\n0  0 -1  1\n0 -1  1  0";
  }
}

// Preset Loader
function loadPreset(key) {
  const preset = PRESETS[key];
  if (!preset) return;

  // Set form controls
  const typeRadio = document.querySelector(`input[name='matrixType'][value='${preset.type === "edges" ? "adj" : preset.type}']`);
  if (typeRadio) typeRadio.checked = true;

  const dirRadio = document.querySelector(`input[name='graphDirected'][value='${preset.directed ? "true" : "false"}']`);
  if (dirRadio) dirRadio.checked = true;

  document.getElementById("vertexNamesInput").value = preset.nodes.join(", ");

  let matrixText = "";
  if (preset.matrix) {
    matrixText = preset.matrix.map(row => row.join(" ")).join("\n");
  } else if (preset.type === "edges") {
    // Generate adjacency matrix representation for text box
    const n = preset.nodes.length;
    const nodeIdx = {};
    preset.nodes.forEach((v, i) => nodeIdx[v] = i);
    const m = Array(n).fill(0).map(() => Array(n).fill(0));
    preset.edges_list.forEach(e => {
      const u = nodeIdx[e.u];
      const v = nodeIdx[e.v];
      m[u][v] = 1;
      if (!preset.directed) m[v][u] = 1;
    });
    matrixText = m.map(row => row.join(" ")).join("\n");
  }

  document.getElementById("matrixInput").value = matrixText;
  updateInputLabels(preset.type === "edges" ? "adj" : preset.type);

  // Directly run solver
  if (preset.type === "edges") {
    // Solve edge list directly
    const solved = solveFromEdgesList(preset.nodes, preset.edges_list, preset.directed);
    renderGraphAndResults(solved);
  } else {
    runAnalysisFromInputs();
  }
}

// Input parser & dispatcher
function runAnalysisFromInputs() {
  const matrixType = document.querySelector("input[name='matrixType']:checked").value;
  const isDirected = document.querySelector("input[name='graphDirected']:checked").value === "true";
  const rawText = document.getElementById("matrixInput").value.trim();
  const rawNames = document.getElementById("vertexNamesInput").value.trim();

  if (!rawText) {
    alert("Please enter matrix values.");
    return;
  }

  const matrix = parseMatrixString(rawText);
  if (!matrix || matrix.length === 0) {
    alert("Invalid matrix format. Please enter rows of numbers separated by spaces or commas.");
    return;
  }

  const vertexLabels = rawNames ? rawNames.split(",").map(s => s.trim()).filter(Boolean) : null;

  // Try calling Python backend if served via Flask, fallback to client-side JS solver
  fetch("/api/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      matrix_type: matrixType,
      is_directed: isDirected,
      matrix: matrix,
      vertex_labels: vertexLabels
    })
  })
  .then(res => {
    if (!res.ok) throw new Error("API call failed, falling back to local JS solver.");
    return res.json();
  })
  .then(data => {
    if (data.error) throw new Error(data.error);
    renderGraphAndResults(data);
  })
  .catch(() => {
    // Standalone / Offline client-side JS solver fallback
    try {
      const result = clientSideSolve(matrixType, matrix, vertexLabels, isDirected);
      renderGraphAndResults(result);
    } catch (err) {
      alert("Error solving graph: " + err.message);
    }
  });
}

function parseMatrixString(text) {
  const lines = text.split("\n").map(l => l.trim()).filter(Boolean);
  const matrix = [];
  for (const line of lines) {
    const cleaned = line.replace(/[\[\],;]/g, " ").trim();
    const parts = cleaned.split(/\s+/).map(Number);
    if (parts.some(isNaN)) throw new Error("Matrix contains non-numeric values.");
    if (parts.length > 0) matrix.push(parts);
  }
  return matrix;
}

// ==========================================
// PURE CLIENT-SIDE GRAPH THEORY SOLVER
// ==========================================
function clientSideSolve(matrixType, matrix, customLabels, isDirected) {
  if (matrixType === "adj") {
    const n = matrix.length;
    for (const r of matrix) {
      if (r.length !== n) throw new Error("Adjacency matrix must be square (N x N).");
    }
    const vertices = (customLabels && customLabels.length === n) ? customLabels : Array.from({ length: n }, (_, i) => `v${i + 1}`);
    const edges = [];
    let edgeCount = 1;

    if (isDirected) {
      for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
          if (matrix[i][j] !== 0) {
            edges.push({ id: `e${edgeCount++}`, u: vertices[i], v: vertices[j], weight: matrix[i][j] });
          }
        }
      }
    } else {
      for (let i = 0; i < n; i++) {
        for (let j = i; j < n; j++) {
          const val = matrix[i][j];
          if (val !== 0) {
            const count = Math.round(val);
            for (let c = 0; c < Math.max(1, count); c++) {
              edges.push({ id: `e${edgeCount++}`, u: vertices[i], v: vertices[j], weight: val });
            }
          }
        }
      }
    }
    return solveFromEdgesList(vertices, edges, isDirected);
  } else {
    // Incidence matrix
    const n = matrix.length;
    const m = matrix[0].length;
    for (const r of matrix) {
      if (r.length !== m) throw new Error("All rows in incidence matrix must have identical column counts.");
    }
    const vertices = (customLabels && customLabels.length === n) ? customLabels : Array.from({ length: n }, (_, i) => `v${i + 1}`);
    const edges = [];

    for (let j = 0; j < m; j++) {
      const col = matrix.map(r => r[j]);
      const nonZero = [];
      col.forEach((val, i) => { if (val !== 0) nonZero.push({ i, val }); });

      if (isDirected) {
        const pos = nonZero.filter(x => x.val > 0);
        const neg = nonZero.filter(x => x.val < 0);
        if (pos.length === 1 && neg.length === 1) {
          edges.push({ id: `e${j + 1}`, u: vertices[pos[0].i], v: vertices[neg[0].i], weight: Math.abs(pos[0].val) });
        } else if (nonZero.length === 1) {
          edges.push({ id: `e${j + 1}`, u: vertices[nonZero[0].i], v: vertices[nonZero[0].i], weight: Math.abs(nonZero[0].val) });
        } else {
          throw new Error(`Column ${j + 1} is invalid for directed incidence matrix.`);
        }
      } else {
        if (nonZero.length === 2) {
          edges.push({ id: `e${j + 1}`, u: vertices[nonZero[0].i], v: vertices[nonZero[1].i], weight: nonZero[0].val });
        } else if (nonZero.length === 1) {
          edges.push({ id: `e${j + 1}`, u: vertices[nonZero[0].i], v: vertices[nonZero[0].i], weight: nonZero[0].val });
        } else {
          throw new Error(`Column ${j + 1} must connect exactly 2 vertices in undirected graph.`);
        }
      }
    }
    return solveFromEdgesList(vertices, edges, isDirected);
  }
}

function solveFromEdgesList(vertices, edges, isDirected) {
  const n = vertices.length;
  const vIdx = {};
  vertices.forEach((v, i) => vIdx[v] = i);

  // Degrees
  const degrees = {};
  vertices.forEach(v => degrees[v] = 0);
  edges.forEach(e => {
    degrees[e.u] = (degrees[e.u] || 0) + 1;
    if (!isDirected || e.u !== e.v) {
      degrees[e.v] = (degrees[e.v] || 0) + 1;
    }
  });

  // Adjacency Matrix
  const adjMat = Array(n).fill(0).map(() => Array(n).fill(0));
  edges.forEach(e => {
    const u = vIdx[e.u];
    const v = vIdx[e.v];
    if (isDirected) {
      adjMat[u][v] = e.weight || 1;
    } else {
      adjMat[u][v] = e.weight || 1;
      adjMat[v][u] = e.weight || 1;
    }
  });

  // Incidence Matrix
  const incMat = Array(n).fill(0).map(() => Array(edges.length).fill(0));
  edges.forEach((e, j) => {
    const u = vIdx[e.u];
    const v = vIdx[e.v];
    const w = e.weight || 1;
    if (isDirected) {
      if (u === v) incMat[u][j] = 0;
      else {
        incMat[u][j] = w;
        incMat[v][j] = -w;
      }
    } else {
      if (u === v) incMat[u][j] = 2 * w;
      else {
        incMat[u][j] = w;
        incMat[v][j] = w;
      }
    }
  });

  // Spanning Forest / Tree
  const parent = {};
  vertices.forEach(v => parent[v] = v);
  function find(i) {
    if (parent[i] === i) return i;
    parent[i] = find(parent[i]);
    return parent[i];
  }
  function union(i, j) {
    const ri = find(i);
    const rj = find(j);
    if (ri !== rj) {
      parent[ri] = rj;
      return true;
    }
    return false;
  }

  const branches = [];
  const chords = [];
  edges.forEach(e => {
    if (e.u !== e.v && union(e.u, e.v)) {
      branches.push(e);
    } else {
      chords.push(e);
    }
  });

  // Tree BFS path finder
  function getPathInTree(start, end) {
    if (start === end) return [];
    const adj = {};
    vertices.forEach(v => adj[v] = []);
    branches.forEach(e => {
      adj[e.u].push({ next: e.v, edge: e });
      adj[e.v].push({ next: e.u, edge: e });
    });
    const queue = [[start, []]];
    const visited = new Set([start]);
    while (queue.length > 0) {
      const [curr, path] = queue.shift();
      if (curr === end) return path;
      for (const { next, edge } of adj[curr]) {
        if (!visited.has(next)) {
          visited.add(next);
          queue.push([next, [...path, edge]]);
        }
      }
    }
    return null;
  }

  // Fundamental Cycles [I_mu | B_ft]
  const orderedEdges = [...chords, ...branches];
  const edgeIdxMap = {};
  orderedEdges.forEach((e, idx) => edgeIdxMap[e.id] = idx);

  const cycles = [];
  const cycleMatrix = [];

  chords.forEach((chord, i) => {
    const path = getPathInTree(chord.u, chord.v);
    const cycleEdges = path ? [chord, ...path] : [chord];
    const cycleId = `Z${i + 1}`;
    cycles.push({
      cycle_id: cycleId,
      chord: chord.id,
      edges: cycleEdges.map(e => e.id)
    });
    const row = Array(orderedEdges.length).fill(0);
    cycleEdges.forEach(e => {
      row[edgeIdxMap[e.id]] = 1;
    });
    cycleMatrix.push(row);
  });

  // Fundamental Cut-Sets [Q_fc | I_(n-1)]
  const cutsets = [];
  const cutsetMatrix = [];

  branches.forEach((branch, i) => {
    const remaining = branches.filter(b => b.id !== branch.id);
    const adj = {};
    vertices.forEach(v => adj[v] = []);
    remaining.forEach(e => {
      adj[e.u].push(e.v);
      adj[e.v].push(e.u);
    });

    const v1 = new Set([branch.u]);
    const queue = [branch.u];
    while (queue.length > 0) {
      const curr = queue.shift();
      for (const nxt of adj[curr]) {
        if (!v1.has(nxt)) {
          v1.add(nxt);
          queue.push(nxt);
        }
      }
    }

    const cutEdges = [];
    edges.forEach(e => {
      const uIn = v1.has(e.u);
      const vIn = v1.has(e.v);
      if (uIn !== vIn) cutEdges.push(e);
    });

    const cutId = `S${i + 1}`;
    const v1Arr = Array.from(v1).sort();
    const v2Arr = vertices.filter(v => !v1.has(v)).sort();

    cutsets.push({
      cut_id: cutId,
      branch: branch.id,
      partition_v1: v1Arr,
      partition_v2: v2Arr,
      edges: cutEdges.map(e => e.id)
    });

    const row = Array(orderedEdges.length).fill(0);
    cutEdges.forEach(e => {
      row[edgeIdxMap[e.id]] = 1;
    });
    cutsetMatrix.push(row);
  });

  // All Minimal Cut-Sets
  const allCutsets = computeAllMinimalCutsetsClient(vertices, edges);

  return {
    is_directed: isDirected,
    vertices: vertices,
    edges: edges,
    degrees: degrees,
    adjacency_matrix: {
      vertices: vertices,
      matrix: adjMat
    },
    incidence_matrix: {
      vertices: vertices,
      edges: edges.map(e => e.id),
      matrix: incMat
    },
    fundamental_cycle_matrix: {
      branches: branches.map(b => b.id),
      chords: chords.map(c => c.id),
      columns: orderedEdges.map(e => e.id),
      cycle_names: cycles.map(c => c.cycle_id),
      cycles: cycles,
      matrix: cycleMatrix,
      mu: chords.length,
      rank: branches.length
    },
    fundamental_cutset_matrix: {
      branches: branches.map(b => b.id),
      chords: chords.map(c => c.id),
      columns: orderedEdges.map(e => e.id),
      cut_names: cutsets.map(c => c.cut_id),
      cutsets: cutsets,
      matrix: cutsetMatrix
    },
    all_cutset_matrix: allCutsets
  };
}

function computeAllMinimalCutsetsClient(vertices, edges) {
  const n = vertices.length;
  if (n <= 1) return { columns: edges.map(e => e.id), cut_names: [], cutsets: [], matrix: [] };

  const allV = new Set(vertices);
  const v0 = vertices[0];
  const others = vertices.slice(1);

  function isConnected(subset) {
    if (subset.size === 0) return false;
    const arr = Array.from(subset);
    const visited = new Set([arr[0]]);
    const queue = [arr[0]];
    const adj = {};
    arr.forEach(v => adj[v] = []);
    edges.forEach(e => {
      if (subset.has(e.u) && subset.has(e.v)) {
        adj[e.u].push(e.v);
        adj[e.v].push(e.u);
      }
    });
    while (queue.length > 0) {
      const curr = queue.shift();
      for (const nxt of adj[curr]) {
        if (!visited.has(nxt)) {
          visited.add(nxt);
          queue.push(nxt);
        }
      }
    }
    return visited.size === subset.size;
  }

  const cutsets = [];
  const seen = new Set();
  const columns = edges.map(e => e.id);
  const edgeIdx = {};
  edges.forEach((e, idx) => edgeIdx[e.id] = idx);

  // Power set combinations of others
  const totalCombos = 1 << others.length;
  for (let mask = 0; mask < totalCombos; mask++) {
    const s = new Set([v0]);
    for (let i = 0; i < others.length; i++) {
      if ((mask & (1 << i)) !== 0) s.add(others[i]);
    }
    const vs = new Set(vertices.filter(v => !s.has(v)));
    if (vs.size === 0) continue;

    if (isConnected(s) && isConnected(vs)) {
      const cutEdges = [];
      edges.forEach(e => {
        if ((s.has(e.u) && vs.has(e.v)) || (vs.has(e.u) && s.has(e.v))) {
          cutEdges.push(e.id);
        }
      });
      const key = cutEdges.slice().sort().join(",");
      if (key && !seen.has(key)) {
        seen.add(key);
        cutsets.push({
          cut_id: `c${cutsets.length + 1}`,
          partition_v1: Array.from(s).sort(),
          partition_v2: Array.from(vs).sort(),
          edges: cutEdges.slice().sort()
        });
      }
    }
  }

  cutsets.sort((a, b) => a.edges.length - b.edges.length);
  cutsets.forEach((c, idx) => c.cut_id = `c${idx + 1}`);

  const matrix = cutsets.map(c => {
    const row = Array(columns.length).fill(0);
    c.edges.forEach(eid => row[edgeIdx[eid]] = 1);
    return row;
  });

  return {
    columns: columns,
    cut_names: cutsets.map(c => c.cut_id),
    cutsets: cutsets,
    matrix: matrix
  };
}

// ==========================================
// VISUALIZATION & UI RENDERING
// ==========================================
function renderGraphAndResults(data) {
  currentGraphData = data;
  clearHighlight();

  // Metrics
  document.getElementById("metricNodes").innerText = data.vertices.length;
  document.getElementById("metricEdges").innerText = data.edges.length;
  document.getElementById("metricNullity").innerText = data.fundamental_cycle_matrix.mu;
  document.getElementById("metricRank").innerText = data.fundamental_cycle_matrix.rank;

  // Initialize Vis-Network
  drawVisNetwork(data);

  // Render Matrix Tables
  renderAdjacencyTable(data.adjacency_matrix);
  renderIncidenceTable(data.incidence_matrix);
  renderCycleTable(data.fundamental_cycle_matrix);
  renderCutsetTable(data.fundamental_cutset_matrix);
  renderAllCutsetsTable(data.all_cutset_matrix);
}

function drawVisNetwork(data) {
  const container = document.getElementById("graphCanvas");
  if (!container) return;

  const nodes = data.vertices.map(v => ({
    id: v,
    label: v,
    shape: "circle",
    size: 26,
    font: { color: "#ffffff", size: 14, face: "system-ui", bold: { color: "#ffffff" } },
    color: {
      background: "#18181b",
      border: "#ffffff",
      highlight: { background: "#27272a", border: "#ffffff" }
    },
    borderWidth: 2
  }));

  const treeEdgeIds = new Set(data.fundamental_cycle_matrix.branches);

  const edges = data.edges.map(e => {
    const isTree = treeEdgeIds.has(e.id);
    return {
      id: e.id,
      from: e.u,
      to: e.v,
      label: e.id,
      arrows: data.is_directed ? "to" : undefined,
      font: { color: "#a1a1aa", size: 11, background: "#09090b", strokeWidth: 0 },
      color: {
        color: isTree ? "#22c55e" : "#71717a",
        highlight: "#ffffff"
      },
      dashes: !isTree && !data.is_directed,
      width: isTree ? 3 : 2
    };
  });

  const networkData = {
    nodes: new vis.DataSet(nodes),
    edges: new vis.DataSet(edges)
  };

  const options = {
    physics: {
      solver: "forceAtlas2Based",
      forceAtlas2Based: {
        gravitationalConstant: -50,
        centralGravity: 0.01,
        springLength: 100,
        springConstant: 0.08
      },
      stabilization: { iterations: 150 }
    },
    interaction: {
      hover: true,
      zoomView: true,
      dragView: true
    }
  };

  currentNetwork = new vis.Network(container, networkData, options);
}

// Interactive Highlighting
function highlightSpanningTree() {
  if (!currentNetwork || !currentGraphData) return;
  activeHighlight = { type: "tree" };

  const treeEdgeIds = new Set(currentGraphData.fundamental_cycle_matrix.branches);
  const edgesUpdate = currentGraphData.edges.map(e => {
    const isTree = treeEdgeIds.has(e.id);
    return {
      id: e.id,
      color: { color: isTree ? "#22c55e" : "#27272a" },
      width: isTree ? 4 : 1,
      dashes: !isTree
    };
  });

  currentNetwork.body.data.edges.update(edgesUpdate);
  document.getElementById("btnToggleTree").classList.add("btn-active");
}

function highlightCycle(cycleId) {
  if (!currentNetwork || !currentGraphData) return;
  const cycleObj = currentGraphData.fundamental_cycle_matrix.cycles.find(c => c.cycle_id === cycleId);
  if (!cycleObj) return;

  activeHighlight = { type: "cycle", id: cycleId };
  const inCycleEdges = new Set(cycleObj.edges);

  const edgesUpdate = currentGraphData.edges.map(e => {
    const isInc = inCycleEdges.has(e.id);
    return {
      id: e.id,
      color: { color: isInc ? "#ffffff" : "#18181b" },
      width: isInc ? 4 : 1,
      dashes: false
    };
  });
  currentNetwork.body.data.edges.update(edgesUpdate);

  // Highlight rows in table
  document.querySelectorAll(".cycle-row").forEach(r => {
    r.classList.toggle("highlighted", r.dataset.id === cycleId);
  });
}

function highlightCutset(cutId, isFundamental = true) {
  if (!currentNetwork || !currentGraphData) return;
  const list = isFundamental ? currentGraphData.fundamental_cutset_matrix.cutsets : currentGraphData.all_cutset_matrix.cutsets;
  const cutObj = list.find(c => c.cut_id === cutId);
  if (!cutObj) return;

  activeHighlight = { type: "cut", id: cutId };
  const cutEdges = new Set(cutObj.edges);
  const v1Set = new Set(cutObj.partition_v1);

  // Update edges
  const edgesUpdate = currentGraphData.edges.map(e => {
    const isCut = cutEdges.has(e.id);
    return {
      id: e.id,
      color: { color: isCut ? "#ef4444" : "#18181b" },
      width: isCut ? 4 : 1,
      dashes: isCut
    };
  });
  currentNetwork.body.data.edges.update(edgesUpdate);

  // Update nodes partition coloring
  const nodesUpdate = currentGraphData.vertices.map(v => ({
    id: v,
    color: {
      background: v1Set.has(v) ? "#27272a" : "#09090b",
      border: v1Set.has(v) ? "#ffffff" : "#71717a"
    }
  }));
  currentNetwork.body.data.nodes.update(nodesUpdate);

  document.querySelectorAll(".cut-row").forEach(r => {
    r.classList.toggle("highlighted", r.dataset.id === cutId);
  });
}

function clearHighlight() {
  if (!currentNetwork || !currentGraphData) return;
  activeHighlight = null;
  document.getElementById("btnToggleTree").classList.remove("btn-active");

  const treeEdgeIds = new Set(currentGraphData.fundamental_cycle_matrix.branches);
  const edgesUpdate = currentGraphData.edges.map(e => {
    const isTree = treeEdgeIds.has(e.id);
    return {
      id: e.id,
      color: { color: isTree ? "#22c55e" : "#71717a" },
      width: isTree ? 3 : 2,
      dashes: !isTree && !currentGraphData.is_directed
    };
  });
  currentNetwork.body.data.edges.update(edgesUpdate);

  const nodesUpdate = currentGraphData.vertices.map(v => ({
    id: v,
    color: { background: "#18181b", border: "#ffffff" }
  }));
  currentNetwork.body.data.nodes.update(nodesUpdate);

  document.querySelectorAll(".interactive-row").forEach(r => r.classList.remove("highlighted"));
}

// ==========================================
// TABLE BUILDERS
// ==========================================
function renderAdjacencyTable(adj) {
  const container = document.getElementById("tableAdjacency");
  if (!container) return;
  let html = `<table class="matrix-table"><thead><tr><th>A</th>`;
  adj.vertices.forEach(v => html += `<th>${v}</th>`);
  html += `</tr></thead><tbody>`;

  adj.matrix.forEach((row, i) => {
    html += `<tr><th class="row-header">${adj.vertices[i]}</th>`;
    row.forEach(val => {
      const cls = val > 0 ? "val-1" : "val-0";
      html += `<td class="${cls}">${val}</td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody></table>`;
  container.innerHTML = html;
}

function renderIncidenceTable(inc) {
  const container = document.getElementById("tableIncidence");
  if (!container) return;
  let html = `<table class="matrix-table"><thead><tr><th>M</th>`;
  inc.edges.forEach(e => html += `<th>${e}</th>`);
  html += `</tr></thead><tbody>`;

  inc.matrix.forEach((row, i) => {
    html += `<tr><th class="row-header">${inc.vertices[i]}</th>`;
    row.forEach(val => {
      let cls = "val-0";
      if (val > 0) cls = "val-1";
      else if (val < 0) cls = "val-neg1";
      html += `<td class="${cls}">${val}</td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody></table>`;
  container.innerHTML = html;
}

function renderCycleTable(cycleData) {
  const container = document.getElementById("tableCycle");
  const badgesContainer = document.getElementById("cycleBadges");
  if (!container) return;

  // Cycle Badges
  if (badgesContainer) {
    let bHtml = "";
    cycleData.cycles.forEach(c => {
      bHtml += `<div class="list-item-badge" onclick="highlightCycle('${c.cycle_id}')">
        <strong>${c.cycle_id}</strong> (Chord: ${c.chord}): {${c.edges.join(", ")}}
      </div>`;
    });
    badgesContainer.innerHTML = bHtml || "<em>No fundamental cycles (acyclic tree).</em>";
  }

  let html = `<table class="matrix-table"><thead><tr><th>B_f</th>`;
  cycleData.columns.forEach((col, idx) => {
    const isChord = idx < cycleData.mu;
    const badge = isChord ? `<span style="color:#a1a1aa;">[chord]</span>` : `<span style="color:#22c55e;">[tree]</span>`;
    html += `<th>${col}<br>${badge}</th>`;
  });
  html += `</tr></thead><tbody>`;

  cycleData.matrix.forEach((row, i) => {
    const cid = cycleData.cycle_names[i];
    html += `<tr class="interactive-row cycle-row" data-id="${cid}" onclick="highlightCycle('${cid}')">
      <th class="row-header">${cid}</th>`;
    row.forEach(val => {
      html += `<td class="${val ? 'val-1' : 'val-0'}">${val}</td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody></table>`;
  container.innerHTML = html;
}

function renderCutsetTable(cutData) {
  const container = document.getElementById("tableCutset");
  const badgesContainer = document.getElementById("cutsetBadges");
  if (!container) return;

  if (badgesContainer) {
    let bHtml = "";
    cutData.cutsets.forEach(c => {
      bHtml += `<div class="list-item-badge" onclick="highlightCutset('${c.cut_id}', true)">
        <strong>${c.cut_id}</strong> (Branch: ${c.branch}): {${c.edges.join(", ")}} &bull; Partitions: [${c.partition_v1.join(",")}] | [${c.partition_v2.join(",")}]
      </div>`;
    });
    badgesContainer.innerHTML = bHtml || "<em>No cut-sets found.</em>";
  }

  let html = `<table class="matrix-table"><thead><tr><th>Q_f</th>`;
  cutData.columns.forEach((col, idx) => {
    const isChord = idx < (currentGraphData.fundamental_cycle_matrix.mu);
    const badge = isChord ? `<span style="color:#a1a1aa;">[chord]</span>` : `<span style="color:#22c55e;">[tree]</span>`;
    html += `<th>${col}<br>${badge}</th>`;
  });
  html += `</tr></thead><tbody>`;

  cutData.matrix.forEach((row, i) => {
    const cid = cutData.cut_names[i];
    html += `<tr class="interactive-row cut-row" data-id="${cid}" onclick="highlightCutset('${cid}', true)">
      <th class="row-header">${cid}</th>`;
    row.forEach(val => {
      html += `<td class="${val ? 'val-1' : 'val-0'}">${val}</td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody></table>`;
  container.innerHTML = html;
}

function renderAllCutsetsTable(allCuts) {
  const container = document.getElementById("tableAllCutsets");
  const badgesContainer = document.getElementById("allCutsetsBadges");
  if (!container) return;

  if (badgesContainer) {
    let bHtml = "";
    allCuts.cutsets.forEach(c => {
      bHtml += `<div class="list-item-badge" onclick="highlightCutset('${c.cut_id}', false)">
        <strong>${c.cut_id}</strong>: {${c.edges.join(", ")}} &bull; Partitions: [${c.partition_v1.join(",")}] | [${c.partition_v2.join(",")}]
      </div>`;
    });
    badgesContainer.innerHTML = bHtml;
  }

  let html = `<table class="matrix-table"><thead><tr><th>C(G)</th>`;
  allCuts.columns.forEach(col => html += `<th>${col}</th>`);
  html += `</tr></thead><tbody>`;

  allCuts.matrix.forEach((row, i) => {
    const cid = allCuts.cut_names[i];
    html += `<tr class="interactive-row cut-row" data-id="${cid}" onclick="highlightCutset('${cid}', false)">
      <th class="row-header">${cid}</th>`;
    row.forEach(val => {
      html += `<td class="${val ? 'val-1' : 'val-0'}">${val}</td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody></table>`;
  container.innerHTML = html;
}

// PNG Export
function exportGraphPng() {
  if (!currentNetwork) return;
  const canvas = document.querySelector("#graphCanvas canvas");
  if (!canvas) return;
  const image = canvas.toDataURL("image/png");
  const link = document.createElement("a");
  link.download = "graph-visualization.png";
  link.href = image;
  link.click();
}

// LaTeX Export Modal
function exportLatexModal() {
  if (!currentGraphData) return;
  const modal = document.getElementById("latexModal");
  const textarea = document.getElementById("latexOutput");
  if (!modal || !textarea) return;

  let code = `% Graph Matrices Export\n`;
  code += `% Vertices: ${currentGraphData.vertices.join(", ")}\n\n`;

  // Fundamental Cycle Matrix
  code += `% Fundamental Cycle Matrix B_f = [I_mu | B_ft]\n`;
  code += `\\begin{equation}\nB_f = \\begin{pmatrix}\n`;
  currentGraphData.fundamental_cycle_matrix.matrix.forEach((row, i) => {
    code += `  ` + row.join(" & ") + (i === currentGraphData.fundamental_cycle_matrix.matrix.length - 1 ? "\n" : " \\\\\n");
  });
  code += `\\end{pmatrix}\n\\end{equation}\n\n`;

  // Fundamental Cut-Set Matrix
  code += `% Fundamental Cut-Set Matrix Q_f = [Q_fc | I_(n-1)]\n`;
  code += `\\begin{equation}\nQ_f = \\begin{pmatrix}\n`;
  currentGraphData.fundamental_cutset_matrix.matrix.forEach((row, i) => {
    code += `  ` + row.join(" & ") + (i === currentGraphData.fundamental_cutset_matrix.matrix.length - 1 ? "\n" : " \\\\\n");
  });
  code += `\\end{pmatrix}\n\\end{equation}\n`;

  textarea.value = code;
  modal.classList.add("open");
}

function closeLatexModal() {
  const modal = document.getElementById("latexModal");
  if (modal) modal.classList.remove("open");
}
