import random
from .graph import RoadGraph

def generate_grid_graph(size: int, traffic_factor: float = 1.0, seed: int = 7) -> RoadGraph:
    """Create a connected synthetic city grid. Coordinates make Euclidean A* admissible."""
    side = max(3, round(size ** 0.5))
    while side * side < size:
        side += 1
    g = RoadGraph(); rng = random.Random(seed)
    for i in range(side):
        for j in range(side):
            idx=i*side+j
            if idx >= size: continue
            g.add_node(f'N{idx}', j/(side-1), i/(side-1), f'Intersection {idx}')
    for i in range(side):
        for j in range(side):
            idx=i*side+j
            if idx >= size: continue
            if j+1 < side and idx+1 < size:
                g.add_edge(f'N{idx}', f'N{idx+1}', (1.0+rng.uniform(0.05,0.35))*traffic_factor)
            if i+1 < side and idx+side < size:
                g.add_edge(f'N{idx}', f'N{idx+side}', (1.0+rng.uniform(0.05,0.35))*traffic_factor)
            # A few diagonals create alternate routes while keeping the graph local.
            if i+1 < side and j+1 < side and idx+side+1 < size and rng.random() < 0.25:
                g.add_edge(f'N{idx}', f'N{idx+side+1}', (1.35+rng.uniform(0.0,0.25))*traffic_factor)
    return g

def build_default_graph(scenario='medium'):
    sizes={'small': 16,'medium': 64,'large': 144,'dense': 100}
    traffic={'small':1.0,'medium':1.0,'large':1.0,'dense':0.82}
    return generate_grid_graph(sizes.get(scenario,64), traffic.get(scenario,1.0), seed=19 if scenario=='dense' else 7)
