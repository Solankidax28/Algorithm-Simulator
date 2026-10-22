# Emergency Ambulance Route Optimization System

A beginner-friendly, offline DAA mini project comparing **Dijkstra's Algorithm** and **A* Search** on a locally generated weighted road network.

## Features
- Flask dashboard with source, hospital, and scenario controls.
- Hand-written Dijkstra and A* using adjacency lists and Python min-heaps.
- Route cost, path, nodes explored, and measured execution time.
- Synthetic small, medium, large, and dense scenarios; no APIs or live traffic.
- Automated tests and real repeated benchmark measurements.
- Charts and raw CSV stored in `results/`.

## Installation and run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`.

## Tests and benchmark
```bash
pytest -q
python benchmarking/benchmark.py
```
Benchmark output: `results/benchmark_results.csv`, `results/benchmark_summary.json`, `results/performance_time.png`, and `results/performance_nodes.png`.

## Structure
`app.py` is the Flask entry point; `graph/` models and generates the graph; `algorithms/` contains the two algorithms; `benchmarking/` measures them; `templates/` and `static/` implement the UI; `tests/` verifies behavior; `report/` contains the academic report; `screenshots/` contains screenshots from the working app.

## DAA notes
With a binary heap and adjacency list, both algorithms have worst-case time O((V+E) log V) and space O(V+E) including the graph. A* is not always faster: its practical advantage depends on heuristic quality and graph structure. The A* heuristic is graph-calibrated: the minimum observed edge_cost / coordinate_distance ratio is multiplied by Euclidean distance. It is admissible by the triangle inequality and is stronger than raw normalized distance.

## Academic integrity
This project uses a self-contained synthetic dataset and standard Python/Flask/pytest/matplotlib libraries. Replace personal-information placeholders in the report before submission. All measurements must be regenerated on the machine used for the viva.
