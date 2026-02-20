import json
import heapq
import re

# -----------------------------
# Main Function
# -----------------------------
def main():
    print("=== Indoor Navigation System ===")

    # --- Get valid starting node ---
    while True:
        start_node = input("Enter starting node ID (e.g., ENT_WEST): ").strip()
        
        if start_node in nodes:
            break
        else:
            print("Invalid starting node. Please try again.")

    # --- Get valid destination room ---
    while True:
        room_number = input("Enter destination room number (e.g., 375): ").strip()
        
        goal_node = find_room_node(room_number)
        if goal_node:
            break
        else:
            print("Room not found. Please enter a valid room number.")

    # If both inputs are valid, navigate
    navigate(start_node, room_number)


# -----------------------------
# Load JSON graph
# -----------------------------
with open("nodes&edges.json", "r") as f:
    data = json.load(f)

nodes = {n["id"]: n for n in data["nodes"]}
edges = data["edges"]
print(f"Loaded nodes and  edges from JSON.")

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

        # Extract numbers from label
        rooms = re.findall(r'\b\d+\w*\b', label)
        print(f"Checking node with label for room. Found rooms")
        if room_number in rooms:
            return node_id

    return None


# -----------------------------
# Dijkstra shortest path
# -----------------------------
def shortest_path(start, goal):
    if start not in graph:
        print(f"Start node '{start}' has no connections.")
        return None, None

    if goal not in graph:
        print(f"Goal node '{goal}' has no connections.")
        return None, None

    pq = [(0, start, [])]  # (distance, current_node, path)
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

    # If we exit loop without returning
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
        raise ValueError(f"Start node '{start_node}' does not exist.")

    goal_node = find_room_node(room_number)

    if not can_reach(start_node, goal_node):
        print("\nNo path exists between these locations.")
        return
    
    total_distance, steps = shortest_path(start_node, goal_node)

    if steps is None:
        print(f"No path found between '{start_node}' and room {room_number}.")
        print("This likely means the nodes are not connected in the graph.")
        return

    print(f"\nNavigation from {nodes[start_node]['label']} to Room {room_number}")
    print(f"Total distance: {total_distance} units\n")

    current = start_node
    for node, instruction in steps:
        if instruction:
            print(f"- {instruction}")
        current = node

    print(f"\nYou have arrived at Room {room_number}.")

# Debug Tool
print("\nGraph connectivity check:")
for node in graph:
    print(f"{node} -> {[n[0] for n in graph[node]]}")





# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    main()


# -----------------------------
# Example Call
# -----------------------------
# navigate("ENT_WEST", "375")







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

