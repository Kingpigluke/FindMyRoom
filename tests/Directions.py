import json
import heapq
import re

# -----------------------------
# Load JSON graph
# -----------------------------
with open("STCf3.json", "r") as f:
    data = json.load(f)

nodes = {n["id"]: n for n in data["nodes"]}
edges = data["edges"]

print(f"Loaded {len(nodes)} nodes and {len(edges)} edges from JSON.")

# -----------------------------
# Add Realistic Connector Edges
# -----------------------------
connector_edges = [
    {
        "from": "W_HALL_8",
        "to": "N_HALL_1",
        "distance": 8,
        "instruction": "Turn right at the end of the west hallway toward the central corridor"
    },
    {
        "from": "E_HALL_8",
        "to": "N_HALL_1",
        "distance": 8,
        "instruction": "Turn left at the end of the east hallway toward the central corridor"
    },
    {
        "from": "ENT_WEST",
        "to": "ENT_CENT",
        "distance": 6,
        "instruction": "Walk through the main corridor toward the central staircase"
    },
    {
        "from": "ENT_EAST",
        "to": "ENT_CENT",
        "distance": 6,
        "instruction": "Walk through the main corridor toward the central staircase"
    }
]

# Avoid duplicate edges
for new_edge in connector_edges:
    exists = any(
        (e["from"] == new_edge["from"] and e["to"] == new_edge["to"]) or
        (e["from"] == new_edge["to"] and e["to"] == new_edge["from"])
        for e in edges
    )
    if not exists:
        edges.append(new_edge)

# -----------------------------
# Build adjacency list
# -----------------------------
graph = {}

for edge in edges:
    a = edge["from"]
    b = edge["to"]
    dist = edge["distance"]
    instr = edge["instruction"]

    graph.setdefault(a, []).append((b, dist, instr))
    graph.setdefault(b, []).append((a, dist, instr))  # bidirectional


# -----------------------------
# Find which node contains a room
# -----------------------------
def find_room_node(room_number):
    room_number = str(room_number)

    for node_id, node_data in nodes.items():
        label = node_data.get("label", "")
        rooms = re.findall(r'\b\d+\w*\b', label)

        if room_number in rooms:
            return node_id

    return None


# -----------------------------
# Dijkstra shortest path
# -----------------------------
def shortest_path(start, goal):
    if start not in graph or goal not in graph:
        return None, None

    pq = [(0, start, [])]
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
                heapq.heappush(
                    pq,
                    (dist + ndist, neighbor, path + [(neighbor, instr)])
                )

    return None, None


# -----------------------------
# Connectivity Check
# -----------------------------
def can_reach(start, goal):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node == goal:
            return True

        if node not in visited:
            visited.add(node)
            for neighbor, _, _ in graph.get(node, []):
                stack.append(neighbor)

    return False


# -----------------------------
# Navigation Function
# -----------------------------
def navigate(start_node, room_number):

    if start_node not in nodes:
        print(f"Start node '{start_node}' does not exist.")
        return

    goal_node = find_room_node(room_number)

    if not goal_node:
        print(f"Room {room_number} not found.")
        return

    if not can_reach(start_node, goal_node):
        print("No path exists between these locations.")
        return

    total_distance, steps = shortest_path(start_node, goal_node)

    if steps is None:
        print("No path found.")
        return

    print(f"\nNavigation from {nodes[start_node]['label']} to Room {room_number}")
    print(f"Total distance: {total_distance} units\n")

    for node, instruction in steps:
        if instruction:
            print(f"- {instruction}")

    print(f"\nYou have arrived at Room {room_number}.")


# -----------------------------
# Main Program
# -----------------------------
def main():
    print("=== Indoor Navigation System ===")

    while True:
        start_node = input("Enter starting node ID (e.g., ENT_WEST): ").strip()
        if start_node in nodes:
            break
        print("Invalid starting node. Please try again.")

    while True:
        room_number = input("Enter destination room number (e.g., 375, 330A, 393): ").strip()
        if find_room_node(room_number):
            break
        print("Room not found. Please enter a valid room number.")

    navigate(start_node, room_number)


# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    main()
