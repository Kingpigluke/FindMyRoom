from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Directions import app, nodes, shortest_path, can_reach

# Add CORS middleware to the existing app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint for the frontend to get all nodes
@app.get("/nodes")
def get_all_nodes():
    result = []
    for node_id, node_data in nodes.items():
        result.append({
            "id": node_id,
            "label": node_data.get("label", node_id),
            "type": node_data.get("node_type", "place")
        })
    return result

# Endpoint adapting the frontend request model to the backend logic
class RouteRequest(BaseModel):
    start: str
    end: str

@app.post("/route")
def calculate_route(request: RouteRequest):
    start_node = request.start
    goal_node = request.end

    if start_node not in nodes or goal_node not in nodes:
        return {"error": "Invalid start or end node"}

    if not can_reach(start_node, goal_node):
        return {"error": "No path exists"}

    total_distance, steps = shortest_path(start_node, goal_node)

    instructions = []
    if steps:
        for step_node, instruction in steps:
            if instruction:
                instructions.append({"instruction": instruction})

    return {
        "distance": total_distance,
        "instructions": instructions
    }