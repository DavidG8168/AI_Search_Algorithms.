from collections import namedtuple
from ways import load_map_from_csv, compute_distance
import ways.info
import heapq

# Declare global variables.
global roads
# roads = load_map_from_csv()
global roads_junctions
# roads_junctions = roads.junctions()
# Create a list of maximum speeds for each road type.
highway_indexes = ways.info.TYPE_INDICES
highway_speeds = ways.info.SPEED_RANGES
global highway_maximum
highway_maximum = dict(zip(highway_indexes, highway_speeds))


# Declare my own priority queue.
class MyPriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


# Define the heuristic.
def heuristic(node_one, node_two):
    return compute_distance(node_one.lat, node_one.lon, node_two.lat, node_two.lon) / 110


# Price func, using edge distance and edge speed to find edge time.
def my_price(edge):
    # Get the maximum speeds of each rode..
    global highway_maximum
    # Convert meters to kilometers and divide by optimal speed to find the time.
    return (edge.distance / 1000) / highway_maximum[edge.highway_type][1]


# Find the path.
def find_astar_route(source, target, cost_func=my_price, heuristic_func=heuristic):
    # Get the junctions.
    global roads
    roads = load_map_from_csv()
    global roads_junctions
    roads_junctions = roads.junctions()
    start = roads_junctions[source]
    goal = roads_junctions[target]
    # Create an open list and two dictionaries to store the previous node and cost of current node.
    frontier = MyPriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}
    # While the open list in not empty.
    while not frontier.empty():
        current = frontier.get()
        # If we reached the goal.
        if current == goal:
            break
        # Go over all the child never.
        for edge in current.links:
            child = roads_junctions[edge.target]
            # Calculate cost using distance in link.
            new_cost = cost_so_far[current] + cost_func(edge)
            # Update the child if needed.
            if child not in cost_so_far or new_cost < cost_so_far[child]:
                cost_so_far[child] = new_cost
                priority = new_cost + heuristic_func(goal, child)
                frontier.put(child, priority)
                # Set the previous node of the child to the current.
                came_from[child] = current
    # Find the path by going through the previous nodes of the goal node.
    path = []
    curr_node = goal
    while curr_node != start:
        path.append(curr_node.index)
        curr_node = came_from[curr_node]
    path.append(curr_node.index)
    path.reverse()
    # Return the path.
    return path


# Converts the path from indexes to junctions.
def convert_to_junc(path):
    nodes = []
    for i in path:
        nodes.append(roads_junctions[i])
    return nodes


# Calculates the time for each part of the road.
def calculate_definite_time(all_path):
    times = []
    nodes = convert_to_junc(all_path)
    for inx in range(len(nodes) - 1):
        for edge in nodes[inx][3]:
            if edge[1] == all_path[inx + 1]:
                # Convert to kilometers from meters and divide by maximum speed to find time.
                times.append(((edge.distance) / 1000) / highway_maximum[edge.highway_type][1])
    # Time in hours.
    return sum(times)


# Estimates the time using the heuristic function.
def calculate_heuristic_time(all_path):
    return heuristic(roads_junctions[all_path[0]], roads_junctions[all_path[len(all_path) - 1]])
