import csv, json, statistics, time, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import matplotlib.pyplot as plt
from graph.data import generate_grid_graph
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar
OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)

def benchmark(sizes=(10,50,100,500), trials=7):
    rows=[]
    for size in sizes:
        side_goal=None
        for t in range(trials):
            g=generate_grid_graph(size,seed=100+t)
            start='N0'; goal=f'N{len(g.nodes)-1}'
            # warm up not included in measured data
            for name,fn in [('Dijkstra',dijkstra),('A*',astar)]:
                r=fn(g,start,goal); rows.append({'input_size':size,'trial':t+1,'algorithm':name,'time_ms':r['time_ms'],'nodes_explored':r['nodes_explored'],'route_cost':r['cost'],'path_length':len(r['path'])})
    with (OUT/'benchmark_results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    summary=[]
    for size in sizes:
        for name in ['Dijkstra','A*']:
            subset=[r for r in rows if r['input_size']==size and r['algorithm']==name]
            summary.append({'input_size':size,'algorithm':name,'avg_time_ms':statistics.mean(r['time_ms'] for r in subset),'avg_nodes_explored':statistics.mean(r['nodes_explored'] for r in subset),'avg_route_cost':statistics.mean(r['route_cost'] for r in subset)})
    (OUT/'benchmark_summary.json').write_text(json.dumps({'methodology':{'trials':trials,'sizes':list(sizes),'dataset':'deterministic synthetic grid graphs','hardware_note':'runtime is machine-dependent'},'summary':summary},indent=2))
    for metric,ylabel,filename in [('avg_time_ms','Average execution time (ms)','performance_time.png'),('avg_nodes_explored','Average nodes explored','performance_nodes.png')]:
        plt.figure(figsize=(8,4.5));
        for name,color in [('Dijkstra','#ff5b61'),('A*','#47d8dc')]:
            s=[x for x in summary if x['algorithm']==name];plt.plot([x['input_size'] for x in s],[x[metric] for x in s],marker='o',label=name,color=color,linewidth=2)
        plt.title(ylabel+' vs input size');plt.xlabel('Input size (nodes)');plt.ylabel(ylabel);plt.grid(alpha=.2);plt.legend();plt.tight_layout();plt.savefig(OUT/filename,dpi=160);plt.close()
    return rows,summary
if __name__=='__main__':
    rows,summary=benchmark();print(f'Wrote {len(rows)} raw measurements and {len(summary)} summary rows to {OUT}')
