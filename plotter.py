from matplotlib import pyplot as plt
import numpy as np

with open("plotData.txt", "r") as file:
    graphName = file.readline()

    times = []
    iterCounts = []
    cliqueSizes = []

    lines = file.readlines()
    for line in lines:
        time, cliqueSize, iterCount = map(float, line.split(' '))

        times.append(time)
        cliqueSizes.append(cliqueSize)
        iterCounts.append(iterCount)

    # print(graphName)
    # print("Times: ", times)
    # print("iterCounts: ", iterCounts)
    # print("cliqueSizes: ", cliqueSizes)

    avgTime = np.average(times)
    avgIterations = np.average(iterCounts)
    avgCliqueSize = np.average(cliqueSizes)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.suptitle("Results for graph " + graphName)
    fig.set_size_inches(12, 6)
                
    _, bins, _ = ax1.hist(times)
    ax1.set_title("Average time: " + str(avgTime))
    ax1.set(xlabel="t", xticks=bins)
    ax1.grid(True)

    _, bins, _ = ax2.hist(cliqueSizes)
    ax2.set_title( "Average size of found cliques: " + str(avgCliqueSize))
    ax2.set(xlabel="clique size", xticks=bins)
    ax2.grid(True)

    _, bins, _ = ax3.hist(iterCounts)
    ax3.set_title("Average needed iterations: " + str(avgIterations))
    ax3.set(xlabel="iterations", xticks=bins)
    ax3.grid(True)

    plt.setp(ax1.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.setp(ax2.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.setp(ax3.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.tight_layout()

    plt.savefig(graphName + '.png')
    plt.show()