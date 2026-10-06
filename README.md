# Informatics ITS Graph Theory IUP

## Group 1 Assignment 5

<div align="center">

| NRP | Name |
| :---: | :---: |
| 5025251012 | Khumaidy Syafiq El Maududy |
| 5025251015 | Renato Kiran Arisandi |
| 5025251016 | Keven John Gondowardojo |
| 5025251010 | Agile Octa Agrakha Handrian |

</div>

---

Adjacency Matrix, Incidence Matrix, Spanning Trees, Fundamental Cycles ($B_f$), and Cut-Set Matrices ($Q_f$ / C(G)$).

---

## Key Features

1. **Dual Matrix Input Support:**
   - **Adjacency Matrix ($A$):** Accepts $N \times N$ matrices for undirected and directed graphs (digraphs) with automatic symmetry validation and loop detection.
   - **Incidence Matrix ($M$):** Accepts $N$ vertices $\times$ $M$ edges. For digraphs, adheres strictly to Week 5 Slide 6 convention ($+1$ leaving a vertex, $-1$ arriving at a vertex).
2. **Interactive Graph Visualization:**
   - Smooth physics-based force-directed topology rendering (via Vis-Network).
   - Draggable nodes, dynamic zooming, directional arrows, and edge labels ($e_1, e_2, \dots$).
   - Color-coded spanning tree branches (emerald green) vs chords (purple dashed).
3. **Fundamental Cycle Matrix ($B_f$):**
   - Spanning tree algorithm partitions edges into $r = n - 1$ branches and $\mu = m - n + 1$ chords.
   - Computes fundamental cycles $Z_1, Z_2, \dots, Z_\mu$ for each chord.
   - Outputs canonical matrix partitioned as **$B_f = [I_\mu \mid B_{ft}]$**.
   - **Interactive Highlighting:** Click any cycle in the UI to highlight that exact loop on the canvas.
4. **Cut-Set Matrix (Q<sub>f</sub> & C(G)):**
   - **Fundamental Cut-Set Matrix ($Q_f$):** For each tree branch, isolates the fundamental cut-set partitioning the graph into $(V_1 \mid V_2)$. Formatted canonically as **$Q_f = [Q_{fc} \mid I_{n-1}]$**.
   - **All Minimal Cut-Sets Matrix ($C(G)$):** Enumerates all minimal cut-sets (matching Week 5 Slide 10 $c_1 \dots c_8$).
   - Verifies the fundamental theorem: **$B_f \cdot Q_f^T \equiv 0 \pmod 2$** (orthogonality of cycle and cut spaces).
   - **Interactive Highlighting:** Click any cut-set to highlight the cut edges and tint the two vertex partitions.
5. **Preloaded Graph Presets:**
   - Undirected & Directed Adjacency Presets
   - Digraph Incidence Matrix Preset
   - Fundamental Cycles Model
   - Cut-Set Matrix (Graph G₁) Model (8 cuts)
   - Case Study 1: AI Service Architecture
   - Case Study 2: Data Centers Network
6. **Export Capabilities:**
   - Export graph canvas directly as high-resolution PNG.
   - Export matrices into LaTeX `pmatrix` code ready for assignment reports.

---

## Prerequisites

- **Python:** 3.10 or higher
- **Browser
- **Optional Dependencies:** `flask` and `requests` (for the Flask web server):
  ```bash
  pip install -r requirements.txt
  ```

---

## How to Run

You can run this project in **3 convenient ways**:

### Method 1: Interactive Flask Web Server (Recommended)
1. Clone this repository or open the project folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

### Method 2: Standalone Offline Browser Mode (Zero Installation)
If you don't want to run Python, simply **double-click `index.html`** or open it in your browser:
- Everything is bundled with a pure client-side JavaScript solver and local visualization assets.
- 100% functional offline without an internet connection or web server.

### Method 3: Command-Line Interface (CLI)
Run analysis directly from your terminal with formatted ASCII/Unicode matrix outputs:

- **Run built-in presets:**
  ```bash
  python cli.py --preset exercise1
  python cli.py --preset exercise2
  python cli.py --preset slide10_cutsets
  python cli.py --preset slide9_cycles
  ```

- **Run custom matrix:**
  ```bash
  # Undirected Adjacency Matrix
  python cli.py --type adj --matrix "0 1 1; 1 0 1; 1 1 0"

  # Directed Incidence Matrix
  python cli.py --type inc --directed --matrix "1 0 -1; -1 1 0; 0 -1 1"
  ```

### Running the Test Suite
Verify all graph theory algorithms against lecture slide ground truth:
```bash
python test_graph.py
```

---

## Sample Input & Output Walkthrough

### Example 1: Slide 12 (Exercise 1 — AI Service Architecture)
**Input Architecture:**  
Components: $A$ (Image Upload), $B$ (Preprocessing), $C$ (Object Detection), $D$ (Tracking), $E$ (Database), $F$ (Dashboard).  
Edges: $A\text{–}B, B\text{–}C, B\text{–}E, C\text{–}D, C\text{–}E, D\text{–}E, D\text{–}F, E\text{–}F$.

#### Adjacency Matrix Output ($A$):
```
     A   B   C   D   E   F
   -----------------------
A |  0   1   0   0   0   0
B |  1   0   1   0   1   0
C |  0   1   0   1   1   0
D |  0   0   1   0   1   1
E |  0   1   1   1   0   1
F |  0   0   0   1   1   0
```

#### Incidence Matrix Output ($M$):
```
    e1  e2  e3  e4  e5  e6  e7  e8
   -------------------------------
A |  1   0   0   0   0   0   0   0
B |  1   1   1   0   0   0   0   0
C |  0   1   0   1   1   0   0   0
D |  0   0   0   1   0   1   1   0
E |  0   0   1   0   1   1   0   1
F |  0   0   0   0   0   0   1   1
```

#### Fundamental Cycle Matrix Output ($B_f = [I_\mu \mid B_{ft}]$):
$n = 6, m = 8 \implies \mu = 8 - 6 + 1 = 3$ fundamental cycles.  
Tree branches: $\{e_1, e_2, e_3, e_4, e_7\}$. Chords: $\{e_5, e_6, e_8\}$.

```
     e5  e6  e8  e1  e2  e3  e4  e7
    -------------------------------
Z1 |  1   0   0   0   1   1   0   0  (Cycle Z1: {e5, e2, e3})
Z2 |  0   1   0   0   1   1   1   0  (Cycle Z2: {e6, e4, e2, e3})
Z3 |  0   0   1   0   1   1   1   1  (Cycle Z3: {e8, e3, e2, e4, e7})
```

#### Fundamental Cut-Set Matrix Output ($Q_f = [Q_{fc} \mid I_{n-1}]$):
Rank $r = n - 1 = 5$ fundamental cut-sets:
```
     e5  e6  e8  e1  e2  e3  e4  e7
    -------------------------------
S1 |  0   0   0   1   0   0   0   0  (Branch e1: isolates {A})
S2 |  1   1   1   0   1   0   0   0  (Branch e2: cuts {e2, e5, e6, e8})
S3 |  1   1   1   0   0   1   0   0  (Branch e3: cuts {e3, e5, e6, e8})
S4 |  0   1   1   0   0   0   1   0  (Branch e4: cuts {e4, e6, e8})
S5 |  0   0   1   0   0   0   0   1  (Branch e7: cuts {e7, e8})
```
Note that $Q_{fc} = B_{ft}^T$, satisfying $B_f \cdot Q_f^T \equiv 0 \pmod 2$.

---

### Example 2: Slide 10 (Cut-Set Matrix — Graph G₁)
For graph $G_1$ with 6 vertices and 8 edges:
- **Cut-sets found:**
  - $c_1 = \{e_8\}$ (cut-edge / bridge)
  - $c_2 = \{e_1, e_2\}$ (isolates $v_6$)
  - $c_3 = \{e_3, e_5\}$
  - $c_4 = \{e_4, e_6\}$
  - $c_5 = \{e_5, e_6, e_7\}$
  - $c_6 = \{e_3, e_6, e_7\}$
  - $c_7 = \{e_3, e_4, e_7\}$
  - $c_8 = \{e_4, e_5, e_7\}$
Matches exactly the 8 cut-sets illustrated on Slide 10.

---

## Repository File Structure

```
├── app.py                      # Flask web server & REST API
├── cli.py                      # Terminal matrix analyzer with ASCII formatting
├── graph_core.py               # Pure Python graph theory engine (Deo chapter 4 algorithms)
├── test_graph.py               # Comprehensive unit test suite
├── index.html                  # Standalone offline browser visualizer
├── templates/
│   └── index.html              # Flask Jinja2 template
├── static/
│   ├── css/
│   │   └── style.css           # Modern dark UI theme
│   └── js/
│       ├── app.js              # Frontend UI controller & client-side solver
│       └── vis-network.min.js  # Offline bundled Vis-Network library
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation & user guide
```

---

## Note & AI Usage Disclosure

AI tools were utilized during the development of this project for:
- **Styling:** Designing the clean dark monochrome user interface and CSS responsive layouts.
- **Code Assistance:** Assisting with debugging, matrix parsers, and unit test coverage.
- **Visualizations:** Configuring physics simulation parameters, graph rendering layouts, and interactive canvas components.
