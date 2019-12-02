# Import everything we need.
from ways import load_map_from_csv
from queue import PriorityQueue
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


# Price func, using edge distance and edge speed to find edge time.
def my_price(edge):
    # Get the maximum speeds of each rode..
    global highway_maximum
    # Convert meters to kilometers and divide by optimal speed to find the time.
    return (edge.distance / 1000) / highway_maximum[edge.highway_type][1]


# This function will use the ucs algorithm to find a path from the source to target node.
def find_ucs_route(source, target, cost_func=my_price):
    global roads
    roads = load_map_from_csv()
    global junctions
    junctions = roads.junctions()
    # Set as the starting node.
    start_junction = junctions[source]
    # Set as the target junction.
    target_junction = junctions[target]
    # Create a priority queue.
    working_on = PriorityQueue()
    # Insert the first one with a cumulative cost of 0.
    working_on.put((0, start_junction))
    # Create list to house the path.
    path = []
    # To recreate the path when we are done.
    global came_from
    came_from = []
    came_from = {start_junction: None}
    # While we're not done.
    while True:
        if working_on.empty():
            raise Exception("Something went wrong.")
        # Get the current node and cost.
        current_cost, current_junction = working_on.get()
        # Set it as explored.
        path.append(current_junction)
        # If we reached the target, return the path and finish.
        if current_junction == target_junction:
            return path
        # Go over all the edges to find their target node.
        for edge in current_junction.links:
            # Get the target node.
            child = junctions[edge.target]
            # If we had not explored the child yet insert it and it's cumulative cost using the given cost function.
            if child not in path:
                # Calculate cost, save the previous node.
                came_from[child] = current_junction
                new_cost = current_cost + cost_func(edge)
                working_on.put((current_cost + new_cost, child))


# Calculate the time of each road and sum it to get the total time.
def find_time(nodes, path):
    global roads
    global highway_maximum
    times = []
    for inx in range(len(nodes) - 1):
        for edge in nodes[inx].links:
            if edge[1] == path[inx + 1]:
                # Convert to kilometers from meters and divide by maximum speed to find time.
                times.append(((edge.distance) / 1000) / highway_maximum[edge.highway_type][1])
    # Result is in hours.
    return sum(times)


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


# Converts path to junctions from indexes.
def convert_to_junc(path):
    nodes = []
    for i in path:
        nodes.append(junctions[i])
    return nodes
