# Store code here for future use.
# Time calculation code.
import ucs
import astar
import idastar
# Find total path time in ucs.
from ways.draw import plot_path
import time

global ucs_times
global astar_times
global idastar_times


def ucs_total_time():
    global ucs_times
    ucs_times = []
    # Remove down
    problems_filen = "db/problems.csv"
    fp = open(problems_filen, 'r')
    content = fp.readlines()
    fp.close()
    content = [x.strip() for x in content]
    w = open("results/UCSRuns.txt", 'w')
    for i in content:
        v = i.split(',')
        start = int(v[0])
        end = int(v[1])
        # Create a list of run times in seconds to then find the standard deviation.
        start_timer = time.time()
        # Find the path using UCS for each of the problems in the file.
        nodes = ucs.find_ucs_route(start, end)
        end_timer = time.time()
        ucs_times.append(end_timer - start_timer)
        all_nodes = []
        # Get the junction indexes.
        for j in nodes:
            all_nodes.append(j[0])
        real_path = ucs.create_path(all_nodes[0], all_nodes[len(all_nodes) - 1])
        nodes = ucs.convert_to_junc(real_path)
        plot_path(ucs.roads, real_path)
        print(str(ucs.find_time(nodes, real_path)) + '\n')
        w.write(str(ucs.find_time(nodes, real_path)) + '\n')
    w.close()
    # Print the list of times for each problem.
    print("The times are:")
    print(ucs_times)
    # Remove up.


# Find total path time in a-star.
def astar_total_time():
    global astar_times
    astar_times = []
    # Remove down
    problems_filen = "db/problems.csv"
    fp = open(problems_filen, 'r')
    content = fp.readlines()
    fp.close()
    content = [x.strip() for x in content]
    w = open("results/AStarRuns.txt", 'w')
    for i in content:
        v = i.split(',')
        start = int(v[0])
        end = int(v[1])
        # Calculate time for each run.
        start_timer = time.time()
        nodes = astar.find_astar_route(start, end)
        end_timer = time.time()
        astar_times.append(end_timer - start_timer)
        plot_path(astar.roads, nodes)
        print(str(astar.calculate_definite_time(nodes)) + ' ' + str(
            astar.calculate_heuristic_time(nodes)) + '\n')
        w.write(str(astar.calculate_definite_time(nodes)) + ' ' + str(
            astar.calculate_heuristic_time(nodes)) + '\n')
    w.close()
    print("The times are:")
    print(astar_times)


# Find total path time in ida-star.
def idastar_total_time():
    global idastar_times
    idastar_times = []
    # Remove down.
    problems_filen = "db/problems.csv"
    fp = open(problems_filen, 'r')
    content = fp.readlines()
    fp.close()
    content = [x.strip() for x in content]
    w = open("results/IDAStarRuns.txt", 'w')
    for i in content:
        v = i.split(',')
        start = int(v[0])
        end = int(v[1])
        # Calculate the time for algorithm
        start_timer = time.time()
        last_node = idastar.find_idastar_route(start, end)
        end_timer = time.time()
        idastar_times.append(end_timer - start_timer)
        all_path = idastar.create_path(start, end)
        plot_path(idastar.roads, all_path)
        print(str(idastar.find_definite_time(all_path)) + ' ' + str(
            idastar.find_heuristic_time(all_path)) + '\n')
        w.write(str(idastar.find_definite_time(all_path)) + ' ' + str(
            idastar.find_heuristic_time(all_path)) + '\n')
    w.close()
    print("The time is:")
    print(idastar_times)
    # Remove up.
