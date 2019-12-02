from ways import load_map_from_csv, compute_distance
import ways.info

# Define global variables.
global roads
# roads = load_map_from_csv()
global junctions
# junctions = roads.junctions()
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
    came_from = {}
    came_from = {start: None}
    threshold = heuristic_func(start, goal)
    while True:
        temp = search(start, goal, 0, threshold)
        if temp == goal:
            return goal
        threshold = temp + 0.5


# Search for the goal node.
def search(node, goal, g, threshold):
    f = g + heuristic(node, goal)
    if f > threshold:
        return f
    if node == goal:
        return goal
    min_val = 100
    for edge in node.links:
        child = junctions[edge.target]
        came_from[child] = node
        # Calculate price.
        temp = search(child, goal, g + my_price(edge), threshold)
        if temp == goal:
            return goal
        if temp < min_val:
            min_val = temp
    return min_val


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
