# NOTE:
# Instructions are assumed to be valid in both directions.
# For production use, reverse-direction instructions should be explicitly defined.


import json
import heapq
import sys


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




def load_graph(json_file):
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
        return BuildingGraph(data["nodes"], data["edges"])
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)


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


def print_instructions(path, edge_used):
    print("\nFastest Route Instructions:\n")
    step = 1
    for i in range(1, len(path)):
        edge = edge_used[path[i]]
        print(f"{step}. {edge['instruction']}")
        step += 1


def main():
    json_file = input("Enter path to building JSON file [STCf3.json]: ").strip()
    if not json_file: 
        json_file = "STCf3.json"
    graph = load_graph(json_file)

    print("\nAvailable Nodes:")
    for node_id, node in graph.nodes.items():
        print(f"- {node_id}: {node.get('label', '')}")


    start = input("\nEnter starting node ID: ").strip()
    end = input("Enter destination node ID: ").strip()

    if start not in graph.nodes or end not in graph.nodes:
        print("Invalid node ID entered.")
        sys.exit(1)

    distances, previous, edge_used = dijkstra(graph, start, end)
    path = reconstruct_path(previous, start, end)

    if not path:
        print("No route found between the selected nodes.")
        sys.exit(1)

    print(f"\nTotal Distance: {distances[end]} units")
    print_instructions(path, edge_used)


if __name__ == "__main__":
    main()
