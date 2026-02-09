import json
import heapq

# -----------------------------
# Load JSON graph
# -----------------------------
with open("nodes&edges.json", "r") as f:
    data = json.load(f)

nodes = {n["id"]: n for n in data["nodes"]}
edges = data["edges"]

# Build adjacency list
graph = {}
for edge in edges:
    a = edge["from"]
    b = edge["to"]
    dist = edge["distance"]
    instr = edge["instruction"]

    graph.setdefault(a, []).append((b, dist, instr))
    graph.setdefault(b, []).append((a, dist, instr))  # bidirectional
        

# -----------------------------
# Dijkstra shortest path
# -----------------------------
def shortest_path(start, goal):
    pq = [(0, start, [])]  # (distance, node, path)
    visited = set()

    while pq:
        dist, node, path = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return dist, path

        for neighbor, ndist, instr in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(pq, (dist + ndist, neighbor, path + [(neighbor, instr)]))

    return None, None


# -----------------------------
# Example usage
# -----------------------------
def navigate(start_node, room_number):
    # Convert "375" → "ROOM_375"
    goal = f"ROOM_{room_number}"

    if goal not in nodes:
        raise ValueError(f"Room {room_number} does not exist in the map")

    total_distance, steps = shortest_path(start_node, goal)

    if steps is None:
        print("No path found.")
        return

    print(f"\nNavigation from {start_node} to {goal}")
    print(f"Total distance: {total_distance} units\n")

    for node, instruction in steps:
        print(f"- {instruction}")



# -----------------------------
# Example call
# -----------------------------
# navigate("ENT_WEST", "375")

