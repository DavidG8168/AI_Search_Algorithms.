import random


# Gets the roads created from the csv.
def generate_path(roads):
    # Function for generating random paths to test algorithms on.
    # List to store the path.
    path = []
    # Get the nodes.
    x = roads.junctions()
    # Create 100 paths.
    for i in range(100):
        # Select random start node as set it as the node we will select the next one from.
        start_node = random.randint(0, 944799)
        selection_node = start_node
        # Add it to the path list.
        path.append(start_node)
        # Generate paths of random lengths between 2 values.
        path_len = random.randint(839, 1563)
        for j in range(path_len):
            # Select the next node from the current one and set the selection node to the one selected.
            selection_node = x[selection_node][3][0][1]
            path.append(x[selection_node][3][0][1])
        # Print the start and end of the path to be placed in the problems.csv
        print(str(path[0]) + ', ' + str(path[len(path) - 1]))
        path = []
