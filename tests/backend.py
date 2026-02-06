from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import heapq

app = Flask(__name__)
CORS(app)  # Permite peticiones desde Angular


class BuildingGraph:
    def __init__(self, nodes, edges):
        self.nodes = {node["id"]: node for node in nodes}
        self.graph = {node_id: [] for node_id in self.nodes}

        # Validate edges first
        for edge in edges:
            if edge["from"] not in self.nodes or edge["to"] not in self.nodes:
                raise ValueError(f"Invalid edge reference: {edge}")

        # Add edges (bidirectional by default)
        for edge in edges:
            self.graph[edge["from"]].append({
                "to": edge["to"],
                "distance": edge["distance"],
                "instruction": edge["instruction"]
            })
            self.graph[edge["to"]].append({
                "to": edge["from"],
                "distance": edge["distance"],
                "instruction": edge["instruction"]
            })


def dijkstra(graph, start, end):
    distances = {node: float("inf") for node in graph.graph}
    previous = {}
    edge_used = {}

    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break

        if current_distance > distances[current_node]:
            continue

        for edge in graph.graph[current_node]:
            neighbor = edge["to"]
            new_distance = current_distance + edge["distance"]

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                edge_used[neighbor] = edge
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, previous, edge_used


def reconstruct_path(previous, start, end):
    path = []
    current = end

    while current != start:
        path.append(current)
        current = previous.get(current)
        if current is None:
            return None

    path.append(start)
    path.reverse()
    return path


# Cargar el grafo al iniciar (FUERA de la clase)
with open('STCf3.json', 'r') as f:
    data = json.load(f)
    building_graph = BuildingGraph(data["nodes"], data["edges"])


@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    return jsonify(list(building_graph.nodes.values()))

@app.route('/api/route', methods=['POST'])
def find_route():
    data = request.json
    start = data.get('start')
    end = data.get('end')
    
    if start not in building_graph.nodes or end not in building_graph.nodes:
        return jsonify({"error": "Invalid Nodes"}), 400
    
    distances, previous, edge_used = dijkstra(building_graph, start, end)
    path = reconstruct_path(previous, start, end)
    
    if not path:
        return jsonify({"error": "There is no route"}), 404
    
    # Construir instrucciones
    instructions = []
    for i in range(1, len(path)):
        edge = edge_used[path[i]]
        instructions.append({
            "step": i,
            "instruction": edge['instruction'],
            "distance": edge['distance']
        })
    
    return jsonify({
        "path": path,
        "total_distance": distances[end],
        "instructions": instructions
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)