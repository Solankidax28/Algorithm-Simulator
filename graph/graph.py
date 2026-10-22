from dataclasses import dataclass
from math import hypot
from typing import Dict, List, Tuple

@dataclass(frozen=True)
class Node:
    id: str
    x: float
    y: float
    label: str

class RoadGraph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.adjacency: Dict[str, List[Tuple[str, float]]] = {}
        # Largest globally safe conversion from coordinate distance to graph cost.
        self._min_cost_per_coordinate = float('inf')

    def add_node(self, node_id: str, x: float, y: float, label: str | None = None):
        self.nodes[node_id] = Node(node_id, float(x), float(y), label or node_id)
        self.adjacency.setdefault(node_id, [])

    def add_edge(self, a: str, b: str, weight: float):
        cost = float(weight)
        self.adjacency[a].append((b, cost))
        self.adjacency[b].append((a, cost))
        coordinate_distance = self._coordinate_distance(a, b)
        if coordinate_distance > 0:
            self._min_cost_per_coordinate = min(
                self._min_cost_per_coordinate, cost / coordinate_distance
            )

    def _coordinate_distance(self, a: str, b: str) -> float:
        na, nb = self.nodes[a], self.nodes[b]
        return hypot(na.x - nb.x, na.y - nb.y)

    @property
    def heuristic_scale(self) -> float:
        """Minimum observed road cost per coordinate unit."""
        if self._min_cost_per_coordinate == float('inf'):
            return 0.0
        return self._min_cost_per_coordinate

    def heuristic(self, a: str, b: str) -> float:
        # Every edge costs at least scale * its coordinate length. By the
        # triangle inequality, scaled direct Euclidean distance is a lower
        # bound for every multi-edge route, so this heuristic is admissible.
        return self.heuristic_scale * self._coordinate_distance(a, b)

    def to_dict(self):
        return {
            'nodes': [vars(n) for n in self.nodes.values()],
            'edges': [{'from': a, 'to': b, 'weight': w} for a, nbrs in self.adjacency.items() for b, w in nbrs if a < b]
        }
