'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways import load_map_from_csv
from collections import Counter
# Random path generator import, use when necessary.
# import generate_paths


def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    # Use to generate random paths to test on.
    # generate_paths.generate_path(roads)
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    # Get the junctions.
    x = roads.junctions()
    # Can generate random paths.
    # generate_paths.generate_path(roads)
    # Get the max and min links to calculate the branching factor and average.
    max_val = 0
    min_val = 100
    amount = 0
    sum_val = 0
    # Calculate the max,min and average of the distances.
    max_dist = 0
    min_dist = 10000
    sum_dist = 0
    amount_distance = 0
    # List for the highway_types
    high_way_types = []
    # Each individual junction.
    for i in x:
        amount += 1
        # The list of links.
        # Max and min.
        if len(i[3]) > max_val:
            max_val = len(i[3])
        if len(i[3]) < min_val:
            min_val = len(i[3])
        # Sum of number of links.
        sum_val += len(i[3])
        # Each link in the list.
        for z in i[3]:
            # Count the amount of distances.
            amount_distance += 1
            # Get the distance of each individual link.
            var = z[2]
            # Sum the distances.
            sum_dist += var
            # Max and min.
            if var > max_dist:
                max_dist = var
            if var < min_dist:
                min_dist = var
            # Collect the highway types from the links.
            high_way_types.append(z[3])
    return {
        # Get length from the roads object that contains this information.
        'Number of junctions': len(roads.junctions()),
        'Number of links': len(list(roads.iterlinks())),
        # Get from previous and calculate mean.
        'Outgoing branching factor': Stat(max=max_val, min=min_val, avg=sum_val / amount),
        'Link distance': Stat(max=max_dist, min=min_dist, avg=sum_dist / amount_distance),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        # Use counter to count the occurrences and sort them by most to least.
        'Link type histogram': Counter(high_way_types).most_common(),  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))


if __name__ == '__main__':
    from sys import argv

    assert len(argv) == 1
    print_stats()
