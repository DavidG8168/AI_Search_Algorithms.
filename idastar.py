from ways import load_map_from_csv, compute_distance
import ways.info
import sys

sys.setrecursionlimit(1500)

# Define global variables.
global roads
#roads = load_map_from_csv()
global junctions
#junctions = roads.junctions()
global came_from
# Create a list of maximum speeds for each road type.
highway_indexes = ways.info.TYPE_INDICES
highway_speeds = ways.info.SPEED_RANGES
global highway_maximum
highway_maximum = dict(zip(highway_indexes, highway_speeds))


# Define the heuristic.
def heuristic(node_one, node_two):
    return compute_distance(node_one.lat, node_one.lon, node_two.lat, node_two.lon) / 110


# Price func, using edge distance and edge speed to find edge time.
def my_price(edge):
    # Get the maximum speeds of each rode..
    global highway_maximum
    # Convert meters to kilometers and divide by optimal speed to find the time.
    return (edge.distance / 1000) / highway_maximum[edge.highway_type][1]


# Setup the variables and the threshold to start the search.
def find_idastar_route(source, target, heuristic_func=heuristic):
    global came_from
    # Get the junction.
    global roads
    roads = load_map_from_csv()
    global junctions
    junctions = roads.junctions()
    start = junctions[source]
    goal = junctions[target]
    # Will be used to re-create the path.
    came_from = {}
    came_from = {start: None}
    bound = heuristic_func(start, goal)
    # The frontier.
    path = [start]
    # While we have not found the path.
    while 1:
        # Search.
        t = search(path, goal, 0, bound)
        # If goal, return.
        if t == goal:
            return t
        # Otherwise change the bound.
        bound = t


# Search for the goal node.
def search(path, goal, g, bound):
    # Look at the frontier.
    node = path[len(path) - 1]
    # Calculate f.
    f = g + heuristic(node, goal)
    # If f larger than bound return it to get new bound.
    if f > bound:
        return f
    # If we reached the goal, return the node.
    if node == goal:
        return node
    min = 10000
    # Check all the child nodes.
    for edge in node.links:
        # Create the junction using the index of the target from the edge.
        child = junctions[edge.target]
        # If child not in frontier.
        if child not in path:
            # Add child to list.
            path.append(child)
            # Update came from.
            came_from[child] = node
            # Recursively search.
            t = search(path, goal, g + my_price(edge), bound)
            # If t is goal, return it.
            if t == goal:
                return t
            if t < min:
                min = t
            # Remove node.
            path.pop()
    return min


# Reconstruct the path going backwards from the goal node.
def create_path(start_index, goal_index):
    goal = junctions[goal_index]
    start = junctions[start_index]
    path = []
    curr_node = goal
    while curr_node != start:
        path.append(curr_node.index)
        curr_node = came_from[curr_node]
    path.append(curr_node.index)
    path.reverse()
    return path


# Converts path in indexes to junctions.
def convert_to_junc(path):
    nodes = []
    for i in path:
        nodes.append(junctions[i])
    return nodes


# Finds the time that it takes go from each junction to another and sums it.
def find_definite_time(all_path):
    times = []
    nodes = convert_to_junc(all_path)
    for inx in range(len(nodes) - 1):
        for edge in nodes[inx][3]:
            if edge[1] == all_path[inx + 1]:
                # Distance in kilometers divided by maximum speed of the road type
                times.append(((edge.distance) / 1000) / highway_maximum[edge.highway_type][1])
    # Return time in kilometers.
    return sum(times)


# Calculates the heuristic time from source to goal.
def find_heuristic_time(all_path):
    return heuristic(junctions[all_path[0]], junctions[all_path[len(all_path) - 1]])
