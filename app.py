from flask import Flask, jsonify, render_template, request, send_from_directory
from pathlib import Path
from graph.data import build_default_graph
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar

app=Flask(__name__)
RESULTS_DIR = Path(__file__).resolve().parent / 'results'

def run(scenario, source, destination):
    graph=build_default_graph(scenario)
    if source not in graph.nodes or destination not in graph.nodes:
        return graph, {'error':'Choose valid source and destination nodes.'}
    return graph, {'dijkstra':dijkstra(graph,source,destination), 'astar':astar(graph,source,destination)}

@app.route('/manus-routes.json')
def routes_manifest():
    return jsonify({'routes':[{'path':'/','title':'Dispatch Graph'}]})

@app.route('/results/<path:filename>')
def results_file(filename):
    return send_from_directory(RESULTS_DIR, filename)

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/network')
def network():
    scenario=request.args.get('scenario','medium'); return jsonify(build_default_graph(scenario).to_dict())

@app.route('/api/route', methods=['POST'])
def route():
    payload=request.get_json(silent=True) or {}; scenario=payload.get('scenario','medium'); source=payload.get('source','N0'); destination=payload.get('destination')
    graph=build_default_graph(scenario); destination=destination or f'N{len(graph.nodes)-1}'
    graph, result=run(scenario,source,destination)
    if 'error' in result: return jsonify(result),400
    return jsonify({'network':graph.to_dict(), **result})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000, debug=False)
