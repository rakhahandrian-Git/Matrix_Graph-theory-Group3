# Week 5 Graph Theory — Exercises Analytical Solutions
**Course:** Graph Theory (Teori Graf) — Week 5: Graph Matrix Representation  
**Institution:** Institut Teknologi Sepuluh Nopember (ITS)  
**Lecturer:** Ilham Gurat Adillion (`ilhamgurata@its.ac.id`)  

---

## Exercise 1 (Slide 12): AI Service Architecture

### Problem Statement
Your team is building an AI service with several components:
- **A** — Image Upload
- **B** — Preprocessing
- **C** — Object Detection
- **D** — Tracking
- **E** — Database
- **F** — Dashboard

A component can communicate directly with another component if a connection exists.  
The current architecture is given by the undirected connections:  
$$\text{Architecture: } A\text{–}B,\ B\text{–}C,\ B\text{–}E,\ C\text{–}D,\ C\text{–}E,\ D\text{–}E,\ D\text{–}F,\ E\text{–}F$$

---

### Questions & Solutions

#### 1. Draw the graph to represent it visually
**Graph Model:** Undirected Graph $G_1 = (V_1, E_1)$  
- Vertex set: $V_1 = \{A, B, C, D, E, F\}$ ($n = 6$ vertices)
- Edge set: $E_1 = \{e_1=(A,B), e_2=(B,C), e_3=(B,E), e_4=(C,D), e_5=(C,E), e_6=(D,E), e_7=(D,F), e_8=(E,F)\}$ ($m = 8$ edges)

```
       [A]
        |  e1
       [B]-----------------(e3)-----------------[E]
       /                                       / | \
     (e2)                                  (e5)/ |  \(e8)
     /                                       /   |   \
   [C]----------------(e4)-----------------[D]   |   [F]
                                             \   |   /
                                              \ (e6)/
                                               \ | /
                                                (e7)
```
*(Notice the central subnetwork formed by $\{B, C, D, E\}$ which forms a chordal cycle structure with $E$ connecting directly to almost all internal services).*

---

#### 2. Represent the architecture as an adjacency matrix
Let the ordered vertices be $(A, B, C, D, E, F)$.  
The symmetric adjacency matrix $A(G)$ of size $6 \times 6$ is:

$$
A = \begin{pmatrix}
0 & 1 & 0 & 0 & 0 & 0 \\
1 & 0 & 1 & 0 & 1 & 0 \\
0 & 1 & 0 & 1 & 1 & 0 \\
0 & 0 & 1 & 0 & 1 & 1 \\
0 & 1 & 1 & 1 & 0 & 1 \\
0 & 0 & 0 & 1 & 1 & 0
\end{pmatrix}
$$

**Incidence Matrix $M$ (Vertices $\times$ Edges):**
$$
M = \begin{pmatrix}
 & e_1 & e_2 & e_3 & e_4 & e_5 & e_6 & e_7 & e_8 \\
A & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
B & 1 & 1 & 1 & 0 & 0 & 0 & 0 & 0 \\
C & 0 & 1 & 0 & 1 & 1 & 0 & 0 & 0 \\
D & 0 & 0 & 0 & 1 & 0 & 1 & 1 & 0 \\
E & 0 & 0 & 1 & 0 & 1 & 1 & 0 & 1 \\
F & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 1
\end{pmatrix}
$$

---

#### 3. Analyse: Which components does E (Database) communicate with directly?
Look at row $E$ (or column $E$) in the adjacency matrix $A$:
- $A_{E, B} = 1 \implies$ **B (Preprocessing)**
- $A_{E, C} = 1 \implies$ **C (Object Detection)**
- $A_{E, D} = 1 \implies$ **D (Tracking)**
- $A_{E, F} = 1 \implies$ **F (Dashboard)**

$$\mathcal{N}(E) = \{B, C, D, F\}$$
**Answer:** E (Database) communicates directly with **Preprocessing (B)**, **Object Detection (C)**, **Tracking (D)**, and **Dashboard (F)**. It does not communicate directly with Image Upload (A).

---

#### 4. Which components have the highest number of direct connections?
Compute the degree $\deg(v) = \sum_{j} A_{ij}$ for each vertex:
- $\deg(A) = 1$
- $\deg(B) = 3$ (connected to A, C, E)
- $\deg(C) = 3$ (connected to B, D, E)
- $\deg(D) = 3$ (connected to C, E, F)
- $\deg(E) = 4$ (connected to B, C, D, F)
- $\deg(F) = 2$ (connected to D, E)

**Answer:** **Component E (Database)** has the highest number of direct connections with **degree 4**.

---

#### 5. If communication between C and E is disabled, update the matrix and determine which components are affected directly.
Disabling communication between $C$ and $E$ removes edge $e_5 = (C, E)$.
The updated adjacency matrix $A'$ is:

$$
A' = \begin{pmatrix}
0 & 1 & 0 & 0 & 0 & 0 \\
1 & 0 & 1 & 0 & 1 & 0 \\
0 & 1 & 0 & 1 & \mathbf{0} & 0 \\
0 & 0 & 1 & 0 & 1 & 1 \\
0 & 1 & \mathbf{0} & 1 & 0 & 1 \\
0 & 0 & 0 & 1 & 1 & 0
\end{pmatrix}
$$

**Directly Affected Components:**
- **C (Object Detection)**: Its degree drops from $3 \to 2$. It loses direct access to the Database and must route through $B$ or $D$.
- **E (Database)**: Its degree drops from $4 \to 3$. It loses direct incoming/outgoing telemetry with Object Detection.
- Other components ($A, B, D, F$) are **not directly affected** because their adjacent edges remain intact.

---

## Exercise 2 (Slide 13): Network of Data Centers

### Problem Statement
The network of data centers is represented as an undirected graph $G = (V, E)$ with:
- Vertices: $V = \{1, 2, 3, 4, 5\}$ where each vertex represents a data center.
- Edges: $E = \{(1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5)\}$ where each edge represents a communication link between data centers.

Let edges be indexed as:
- $e_1 = (1, 2)$
- $e_2 = (1, 3)$
- $e_3 = (2, 3)$
- $e_4 = (2, 4)$
- $e_5 = (3, 5)$
- $e_6 = (4, 5)$

---

### Questions & Solutions

#### 1. Construct the cut edge matrix C of the graph
In graph theory (Narsingh Deo Chapter 4 & Slide 10), the **cut-set matrix** $C(G)$ has rows corresponding to cut-sets and columns corresponding to edges.

##### (A) Single Cut-Edges (Bridges):
A bridge (cut-edge) is an edge whose removal strictly increases the number of connected components (i.e. $|c| = 1$).
Let us inspect the edge connectivity $\lambda(G)$:
- Cycle 1: $\{1, 2, 3\}$ with edges $e_1, e_2, e_3$ (Triangle $K_3$).
- Cycle 2: $\{2, 4, 5, 3\}$ with edges $e_4, e_6, e_5, e_3$ (4-cycle).
Since every edge in $G$ belongs to at least one cycle:
$$\forall e \in E, \quad e \text{ is part of a cycle} \implies e \text{ is NOT a bridge.}$$
Thus, **there are 0 single-edge cut-edges (bridges)** in $G$. The graph is $2$-edge-connected ($\lambda(G) = 2$).

##### (B) Complete Minimal Cut-Sets Matrix $C(G)$:
The minimal cut-sets (disconnecting $G$ into two connected components $S$ and $V \setminus S$) are:
- $c_1 = \{e_1, e_2\}$: Isolates vertex $\{1\}$ from $\{2, 3, 4, 5\}$.
- $c_2 = \{e_4, e_6\}$: Isolates vertex $\{4\}$ from $\{1, 2, 3, 5\}$.
- $c_3 = \{e_5, e_6\}$: Isolates vertex $\{5\}$ from $\{1, 2, 3, 4\}$.
- $c_4 = \{e_1, e_3, e_4\}$: Isolates vertex $\{2\}$ from $\{1, 3, 4, 5\}$.
- $c_5 = \{e_2, e_3, e_5\}$: Isolates vertex $\{3\}$ from $\{1, 2, 4, 5\}$.
- $c_6 = \{e_4, e_5\}$: Separates the triangle $\{1, 2, 3\}$ from the line $\{4, 5\}$.
- $c_7 = \{e_1, e_2, e_4, e_5\}$: Separates $\{1, 4, 5\}$ from $\{2, 3\}$ (non-minimal / compound) or minimal with cross-connections.

The Cut-Set Matrix $C(G)$ (Slide 10 format) for all minimal cut-sets is:

$$
C(G) = \begin{pmatrix}
 & e_1 & e_2 & e_3 & e_4 & e_5 & e_6 \\
c_1 & 1 & 1 & 0 & 0 & 0 & 0 \\
c_2 & 0 & 0 & 0 & 1 & 0 & 1 \\
c_3 & 0 & 0 & 0 & 0 & 1 & 1 \\
c_4 & 1 & 0 & 1 & 1 & 0 & 0 \\
c_5 & 0 & 1 & 1 & 0 & 1 & 0 \\
c_6 & 0 & 0 & 0 & 1 & 1 & 0
\end{pmatrix}
$$

##### (C) Fundamental Cut-Set Matrix $Q_f$:
Selecting spanning tree $T$ with branches $B = \{e_1, e_2, e_4, e_6\}$ and chords $C = \{e_3, e_5\}$:
$$
Q_f = \begin{pmatrix}
 & e_3 & e_5 & e_1 & e_2 & e_4 & e_6 \\
S_1 & 1 & 0 & 1 & 0 & 0 & 0 \\
S_2 & 1 & 1 & 0 & 1 & 0 & 0 \\
S_3 & 0 & 1 & 0 & 0 & 1 & 0 \\
S_4 & 0 & 1 & 0 & 0 & 0 & 1
\end{pmatrix}
$$

---

#### 2. Which communication links are critical because their failure would disconnect a data center from the rest of the network?
- **Strict Single-Failure Analysis:**  
  As proven above, the graph is 2-edge connected ($\lambda=2$). **No single communication link failure can completely disconnect any data center.**
- **Bottleneck / 2-Link Vulnerability Analysis:**  
  Notice that vertices **1, 4, and 5 each have degree 2**:
  - Data Center **1** relies entirely on $\{e_1=(1,2), e_2=(1,3)\}$. If either link fails, Data Center 1 has degree 1 and is on the verge of total isolation.
  - Data Center **4** relies entirely on $\{e_4=(2,4), e_6=(4,5)\}$.
  - Data Center **5** relies entirely on $\{e_5=(3,5), e_6=(4,5)\}$.
  - In particular, **$e_6 = (4, 5)$** is the inter-link between the two peripheral data centers 4 and 5; if $e_6$ fails, then 4 is connected *only* via 2 and 5 is connected *only* via 3.

---

#### 3. Propose an additional communication link that will prevent that data center from becoming disconnected if the critical link fails. Explain your choice using the graph.

##### Proposal 1: Add Link $(1, 4)$
- **Effect:** Connects Data Center 1 directly to Data Center 4.
- **Degrees become:** $\deg(1) = 3$, $\deg(4) = 3$.
- **Explanation:** Currently, Data Center 1 is only connected to the cluster $\{2, 3\}$. Adding $(1, 4)$ creates an alternate route bypassing $\{2, 3\}$. If link $(1, 2)$ or $(1, 3)$ fails, 1 can still reach 2 and 3 via $1 \to 4 \to 5 \to 3$. Similarly, if $(2, 4)$ or $(4, 5)$ fails, 4 remains connected via $4 \to 1 \to 3$.

##### Proposal 2: Add Link $(1, 5)$
- **Effect:** Dual-diagonal link connecting Data Center 1 to Data Center 5.
- **Degrees become:** $\deg(1) = 3$, $\deg(5) = 3$.
- **Explanation:** Balances redundancy symmetrically with proposal 1.

##### Best Complete Recommendation:
Adding link **$(1, 4)$** (or **$(1, 5)$**) elevates the entire network to minimum degree 3 ($\delta(G) \ge 3$), eliminating the 2-edge cut-sets that isolate peripheral data centers 1, 4, or 5.
