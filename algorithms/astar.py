import heapq, time

def astar(graph, start, goal):
    start_time=time.perf_counter(); g_cost={node: float('inf') for node in graph.nodes}; parents={start: None}; g_cost[start]=0.0
    queue=[(graph.heuristic(start,goal),0.0,start)]; explored=0; visited=set()
    while queue:
        _, current_cost, current=heapq.heappop(queue)
        if current in visited: continue
        visited.add(current); explored += 1
        if current == goal: break
        for neighbor, weight in graph.adjacency[current]:
            candidate=current_cost+weight
            if candidate < g_cost[neighbor]:
                g_cost[neighbor]=candidate; parents[neighbor]=current
                f=candidate+graph.heuristic(neighbor,goal)
                heapq.heappush(queue,(f,candidate,neighbor))
    path=_reconstruct(parents,start,goal)
    return {'algorithm':'A*','path':path,'cost':g_cost[goal], 'nodes_explored':explored, 'time_ms':(time.perf_counter()-start_time)*1000, 'found':bool(path)}

def _reconstruct(parents,start,goal):
    if goal != start and goal not in parents: return []
    path=[]; cur=goal
    while cur is not None:
        path.append(cur); cur=parents.get(cur)
    path.reverse(); return path
