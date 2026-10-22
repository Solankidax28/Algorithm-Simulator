from graph.data import generate_grid_graph
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar

def test_same_optimal_cost():
    g=generate_grid_graph(25)
    d=dijkstra(g,'N0','N24'); a=astar(g,'N0','N24')
    assert d['found'] and a['found']; assert abs(d['cost']-a['cost']) < 1e-9

def test_same_node():
    g=generate_grid_graph(9)
    assert dijkstra(g,'N4','N4')['path']==['N4']; assert astar(g,'N4','N4')['path']==['N4']

def test_no_path():
    g=generate_grid_graph(4); g.adjacency['N0']=[]; g.adjacency['N1']=[]
    assert not dijkstra(g,'N0','N3')['found']; assert not astar(g,'N0','N3')['found']

def test_path_edges_exist():
    g=generate_grid_graph(36); r=astar(g,'N0','N35')
    assert all(any(v==b for v,w in g.adjacency[a]) for a,b in zip(r['path'],r['path'][1:]))


def test_calibrated_heuristic_is_admissible_on_every_edge():
    g=generate_grid_graph(64)
    for a, neighbors in g.adjacency.items():
        for b, weight in neighbors:
            assert g.heuristic(a, b) <= weight + 1e-12

def test_calibrated_heuristic_uses_graph_cost_scale():
    g=generate_grid_graph(64)
    raw_distance = g._coordinate_distance('N0', 'N63')
    assert g.heuristic_scale > 1.0
    assert g.heuristic('N0', 'N63') > raw_distance
