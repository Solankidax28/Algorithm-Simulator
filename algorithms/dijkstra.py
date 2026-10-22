import heapq, time

def dijkstra(graph, start, goal):
    start_time=time.perf_counter(); distances={node: float('inf') for node in graph.nodes}; parents={start: None}; distances[start]=0.0
    queue=[(0.0,start)]; explored=0; visited=set()
    while queue:
        current_cost, current=heapq.heappop(queue)
        if current in visited: continue
        visited.add(current); explored += 1
        if current == goal: break
        for neighbor, weight in graph.adjacency[current]:
            candidate=current_cost+weight
            if candidate < distances[neighbor]:
                distances[neighbor]=candidate; parents[neighbor]=current
                heapq.heappush(queue,(candidate,neighbor))
    path=_reconstruct(parents,start,goal)
    return {'algorithm':'Dijkstra','path':path,'cost':distances[goal], 'nodes_explored':explored, 'time_ms':(time.perf_counter()-start_time)*1000, 'found':bool(path)}

def _reconstruct(parents,start,goal):
    if goal != start and goal not in parents: return []
    path=[]; cur=goal
    while cur is not None:
        path.append(cur); cur=parents.get(cur)
    path.reverse(); return path
