'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions
import ucs
import astar
import idastar
# import calculate_time


# Finds path using UCS, gets 2 parameters, source node and target node.
def find_ucs_rout(source, target):
    'call function to find path, and return list of indices'
    # This function reads the problems csv and solves it while creating the graphs.
    # calculate_time.ucs_total_time()
    # Get the path junctions.
    nodes = ucs.find_ucs_route(source, target)
    all_nodes = []
    # Get the junction indexes.
    for i in nodes:
        all_nodes.append(i[0])
    real_path = ucs.create_path(all_nodes[0], all_nodes[len(all_nodes) - 1])
    return real_path


# Find path using a-star, gets 2 parameters, source node and target node.
def find_astar_route(source, target):
    'call function to find path, and return list of indices'
    # Solve the problems in problems.csv and create the graphs.
    # calculate_time.astar_total_time()
    nodes = astar.find_astar_route(source, target)
    return nodes


# Find path using ida-star, gets 2 parameters, source and target node.
def find_idastar_route(source, target):
    'call function to find path, and return list of indices'
    # Solve the problems
    # calculate_time.idastar_total_time()
    res = idastar.find_idastar_route(source, target)
    path = idastar.create_path(source, target)
    return path


def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'ucs':
        # Uses UCS to find path, gets source, target and cost function as parameters
        path = find_ucs_rout(source, target)
    elif argv[1] == 'astar':
        path = find_astar_route(source, target)
    elif argv[1] == 'idastar':
        path = find_idastar_route(source, target)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv

    dispatch(argv)
