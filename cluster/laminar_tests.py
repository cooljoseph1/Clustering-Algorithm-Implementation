from graph import Graph, RandomGraph
from cluster import cluster
from numpy import argmin
from load import word_graph
from load_vector import vector_graph

def test(graph, eps, c):
    labels, clusters, operation_counter = cluster(graph, eps, c, check_laminar = True)
    error = graph.get_clustering_error(labels)
    opt_error = graph.get_optimum_clustering_error() or 1
    print(len(clusters))
    return operation_counter.tagged_counts.get("Symmetric difference", 0) / 2 / len(graph)

def best_c(graph, eps, start=1, delta=0.01):
    # Golden section search to find best constant c for the error ratio.
    def error_ratio(c):
        *_, error, opt_error = test(graph, eps, c)
        return error / opt_error

    phi = (1 + 5**0.5) / 2
    idx = [start, phi*start, 2*start]
    err = [*map(error_ratio, idx)]
    while idx[2] - idx[0] > delta:
        i = argmin(err)
        if err[0] < err[2]:
            if err[0] < err[1]:
                idx = [idx[0] - (idx[1]-idx[0])/phi, idx[0], idx[1]]
                err = [error_ratio(idx[0]), err[0], err[1]]
            else:
                idx = [idx[0], idx[0] + (idx[1]-idx[0])/phi, idx[1]]
                err = [err[0], error_ratio(idx[1]), err[1]]
        else:
            if err[2] < err[1]:
                idx = [idx[1], idx[2], idx[2]+(idx[2]-idx[1])*phi]
                err = [err[1], err[2], error_ratio(idx[2])]
            else:
                idx = [idx[1], idx[1] + (idx[2]-idx[1])/phi, idx[2]]
                err = [err[1], error_ratio(idx[1]), err[2]]
        print(idx, err)
    return idx[1]


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt


    vertices, edges, clusters, prob_flip = 10_000, 1_000_000, 10, 0.10
    graph = RandomGraph(vertices, edges, clusters, prob_flip)
    # graph = vector_graph(10000, 0.05, 0.05)




    # Make graph for finding optimal epsilon
    err_data = []
    eps_list = [0.126*i for i in range(2, 7)]
    c_list = [0.01*2**i for i in range(1, 7)]
    for eps in eps_list:
        c = 2
        err = test(graph, eps, c)
        err_data.append(err)
        print("(Graph Length, epsilon, c) =", len(graph), eps, c)
        print("(Laminar error) =", err)

    err = np.array(err_data)

    plt.plot(eps_list, err, label="Laminar Error")
    plt.xlabel(r"$\varepsilon$")
    plt.title(r"Laminar error as $\varepsilon$ varies")
    plt.legend()

    plt.show()
