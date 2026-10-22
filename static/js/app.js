const $ = id => document.getElementById(id);
const scenario = $('scenario');
const source = $('source');
const destination = $('destination');
const svg = $('map');

let network;

async function requestJson(url, options) {
  const response = await fetch(url, options);
  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.error || 'The request could not be completed.');
  }

  return result;
}

function setNotice(message) {
  $('run-note').textContent = message;
}

function setResultsUnavailable(message) {
  ['d-cost', 'd-nodes', 'd-time', 'a-cost', 'a-nodes', 'a-time'].forEach(id => {
    $(id).textContent = '—';
  });
  $('d-path').textContent = message;
  $('a-path').textContent = message;
  $('insight-title').textContent = 'No comparison to show yet.';
  $('insight-text').textContent = message;
}

function nodePosition(node) {
  return [35 + node.x * 730, 35 + node.y * 450];
}

function draw(graph, dijkstraPath = [], astarPath = []) {
  svg.replaceChildren();

  const nodes = new Map(graph.nodes.map(node => [node.id, node]));

  graph.edges.forEach(edge => {
    const start = nodes.get(edge.from);
    const end = nodes.get(edge.to);
    const [x1, y1] = nodePosition(start);
    const [x2, y2] = nodePosition(end);
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');

    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x2);
    line.setAttribute('y2', y2);
    line.setAttribute('class', 'edge');
    svg.appendChild(line);
  });

  function drawRoute(path, className) {
    for (let index = 0; index < path.length - 1; index += 1) {
      const start = nodes.get(path[index]);
      const end = nodes.get(path[index + 1]);

      if (!start || !end) continue;

      const [x1, y1] = nodePosition(start);
      const [x2, y2] = nodePosition(end);
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');

      line.setAttribute('x1', x1);
      line.setAttribute('y1', y1);
      line.setAttribute('x2', x2);
      line.setAttribute('y2', y2);
      line.setAttribute('class', `route ${className}`);
      svg.appendChild(line);
    }
  }

  drawRoute(dijkstraPath, 'droute');
  drawRoute(astarPath, 'aroute');

  graph.nodes.forEach(node => {
    const [cx, cy] = nodePosition(node);
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    const isSource = node.id === source.value;
    const isDestination = node.id === destination.value;

    circle.setAttribute('cx', cx);
    circle.setAttribute('cy', cy);
    circle.setAttribute('r', isSource || isDestination ? '6' : '2.6');
    circle.setAttribute(
      'class',
      isSource ? 'source-node' : isDestination ? 'dest-node' : 'node'
    );
    svg.appendChild(circle);
  });
}

function resetComparison() {
  $('route-status').textContent = 'Ready';
  $('map-caption-text').textContent = ' Choose a start and destination to begin.';
  $('d-path').textContent = 'Run a comparison to see the route.';
  $('a-path').textContent = 'Run a comparison to see the route.';
  $('insight-title').textContent = 'The results will show up here.';
  $('insight-text').textContent =
    'Run a comparison to see route costs, search effort, and timings from this particular run. Timing can vary from one run to the next.';
  ['d-cost', 'd-nodes', 'd-time', 'a-cost', 'a-nodes', 'a-time'].forEach(id => {
    $(id).textContent = '—';
  });
}

async function loadNetwork() {
  const scenarioName = scenario.options[scenario.selectedIndex].text.split(' · ')[0];

  try {
    network = await requestJson(`/api/network?scenario=${encodeURIComponent(scenario.value)}`);
    $('node-count').textContent = network.nodes.length;
    $('edge-count').textContent = network.edges.length;

    source.replaceChildren();
    destination.replaceChildren();
    network.nodes.forEach(node => {
      source.add(new Option(node.label, node.id));
      destination.add(new Option(node.label, node.id));
    });

    source.value = 'N0';
    destination.value = `N${network.nodes.length - 1}`;
    draw(network);
    resetComparison();
    $('map-title').textContent = `${scenarioName} network · ready to explore`;
    setNotice('Ready when you are. This demo runs entirely on your machine.');
  } catch (error) {
    network = null;
    $('node-count').textContent = '—';
    $('edge-count').textContent = '—';
    svg.replaceChildren();
    $('map-title').textContent = 'Could not load this network';
    $('route-status').textContent = 'Unavailable';
    $('map-caption-text').textContent = '';
    setNotice(error.message);
    setResultsUnavailable(error.message);
  }
}

function setResult(prefix, result) {
  $(`${prefix}-cost`).textContent = result.found ? result.cost.toFixed(2) : 'No route';
  $(`${prefix}-nodes`).textContent = result.nodes_explored;
  $(`${prefix}-time`).textContent = `${result.time_ms.toFixed(3)} ms`;
  $(`${prefix}-path`).textContent = result.found
    ? result.path.join(' → ')
    : 'No route connects these points.';
}

function updateTakeaway(result) {
  const dijkstra = result.dijkstra;
  const astar = result.astar;

  if (!dijkstra.found || !astar.found) {
    $('insight-title').textContent = 'There is no route between these points.';
    $('insight-text').textContent =
      'Both searches use the same generated network. Try another start or destination.';
    return;
  }

  const nodesSaved = dijkstra.nodes_explored - astar.nodes_explored;
  if (nodesSaved > 0) {
    $('insight-title').textContent = `A* checked ${nodesSaved} fewer intersections this time.`;
  } else if (nodesSaved < 0) {
    $('insight-title').textContent = `Dijkstra checked ${Math.abs(nodesSaved)} fewer intersections this time.`;
  } else {
    $('insight-title').textContent = 'Both searches checked the same number of intersections.';
  }

  $('insight-text').textContent =
    `Both found a route with a cost of ${dijkstra.cost.toFixed(2)}. The time shown is for this run only; it can vary with your machine and the selected network.`;
}

$('run').addEventListener('click', async () => {
  if (!network) {
    setNotice('The network is not available yet. Try changing the network size.');
    return;
  }

  const button = $('run');
  button.disabled = true;
  button.firstChild.textContent = 'Comparing routes… ';
  setNotice('Finding both routes on the same network…');

  try {
    const result = await requestJson('/api/route', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scenario: scenario.value,
        source: source.value,
        destination: destination.value
      })
    });

    setResult('d', result.dijkstra);
    setResult('a', result.astar);
    draw(result.network, result.dijkstra.path, result.astar.path);
    $('route-status').textContent = 'Compared';
    $('map-caption-text').textContent =
      ` ${source.options[source.selectedIndex].text} to ${destination.options[destination.selectedIndex].text}.`;
    $('map-title').textContent = `${scenario.options[scenario.selectedIndex].text.split(' · ')[0]} network · routes compared`;
    updateTakeaway(result);
    setNotice('Comparison complete. Change either point to try another route.');
  } catch (error) {
    $('route-status').textContent = 'Could not compare';
    setNotice(error.message);
  } finally {
    button.disabled = false;
    button.firstChild.textContent = 'Compare routes ';
  }
});

scenario.addEventListener('change', loadNetwork);
source.addEventListener('change', () => network && draw(network));
destination.addEventListener('change', () => network && draw(network));

loadNetwork();
