import heapq  # Used for a priority queue (always pulls the best next option)


class GridMap:
    def __init__(self, walls):
        # Store all wall segments for fast lookup
        # Each wall blocks movement between two adjacent cells
        self.walls = set(walls)

    def is_blocked(self, a, b):
        # Check if movement between two cells is blocked by a wall
        # frozenset makes the check direction-agnostic
        return frozenset({a, b}) in self.walls


def find_path(start, end, grid_map):
    # Priority queue of positions to explore
    # Each entry is (estimated_total_cost, position)
    open_set = []
    heapq.heappush(open_set, (0, start))

    # Tracks where we came from for each visited position
    came_from = {}

    # Tracks the shortest known distance from start to each position
    g_score = {start: 0}

    def heuristic(a, b):
        # Estimates distance from a to b (Manhattan distance)
        # Helps guide the search toward the destination
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Continue searching while there are positions left to explore
    while open_set:
        # Get the most promising position to explore next
        _, current = heapq.heappop(open_set)

        # If we reached the destination, rebuild and return the path
        if current == end:
            return reconstruct_path(came_from, current)

        # Check all reachable neighboring positions
        for neighbor in get_neighbors(current, grid_map):
            # Distance if we move to this neighbor
            tentative_g = g_score[current] + 1

            # Only update if this path is better than any previous one
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                # Total estimated cost (actual so far + estimated remaining)
                f_score = tentative_g + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score, neighbor))

    # No valid path found
    return None


def get_neighbors(pos, grid_map):
    # Possible movement directions (up, down, left, right)
    x, y = pos
    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    neighbors = []
    for dx, dy in directions:
        candidate = (x + dx, y + dy)

        # Only allow movement if there is no wall blocking it
        if not grid_map.is_blocked(pos, candidate):
            neighbors.append(candidate)

    return neighbors


def reconstruct_path(came_from, current):
    # Rebuild the path by walking backward from the destination
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    # Reverse so the path goes from start to end
    return path[::-1]


# Example usage / test run
if __name__ == "__main__":
    # Define walls between adjacent grid cells
    walls = [
        frozenset({(2,1), (2,2)}),
        frozenset({(3,1), (3,2)}),
        frozenset({(4,1), (4,2)})
    ]

    # Create the grid map
    grid_map = GridMap(walls)

    # Define start and end positions
    start = (1, 1)
    end = (5, 3)

    # Find and print the path
    path = find_path(start, end, grid_map)
    print(path)