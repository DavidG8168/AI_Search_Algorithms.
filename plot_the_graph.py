import matplotlib.pyplot as plt

if __name__ == '__main__':
    astar = open("results/IDAStarRuns.txt", "r")
    x = []
    y = []
    for i in astar:
        v = i.split(' ')
        y.append(float(v[0]))
        x.append(float(v[1]))

    # Draw point based on above x, y axis values.
    plt.scatter(x, y, s=0.5)

    # Set chart title.
    plt.title("Graph of 100 problems")

    # Set x, y label text.
    plt.xlabel("Heuristic Price")
    plt.ylabel("Normal Price")
    plt.show()
