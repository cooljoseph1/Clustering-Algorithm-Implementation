from graph import Graph, RandomGraph
from cluster import cluster
from numpy import argmin
from load import word_graph
from load_vector import vector_graph

def test(graph, eps, c):
    labels, clusters, operation_counter = cluster(graph, eps, c)
    error = graph.get_clustering_error(labels)
    opt_error = graph.get_optimum_clustering_error() or 1
    print(len(clusters))
    for c in clusters:
        if c < 0:
            continue
    #for tag, num in sorted(operation_counter.tagged_counts.items(), key=lambda x: x[1]):
    #    print("Num for tag", tag, "is", num)
    return operation_counter.operation_count, operation_counter.graph_access_count, error, opt_error

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


    #vertices, edges, clusters, prob_flip = 10_000, 1_000_000, 10, 0.45
    #graph = RandomGraph(vertices, edges, clusters, prob_flip)


    """
    # Make graph for finding optimal epsilon
    ops_data = []
    acs_data = []
    err_data = []
    edges_list = [2_00 * x for x in range(10, 500, 20)]
    for edges in edges_list:
        c = 1
        eps = 0.04
        vertices, edges, clusters, prob_flip = 2_00, edges, 10, 0.1
        graph = RandomGraph(vertices, edges, clusters, prob_flip)
        ops, acs, err, opt_err = test(graph, eps, c)
        ops_data.append(ops)
        acs_data.append(acs)
        err_data.append(err / opt_err)
        print("(Graph Length, epsilon, c) =", len(graph), eps, c)
        print("(Operations, Graph accesses) =", ops, acs)
        print("(Clustering error, Optimal error, ratio) =", err, opt_err, err / opt_err)


    ops = np.array(ops_data)
    acs = np.array(acs_data)
    err = np.array(err_data)
    plt.plot(edges_list, ops, label="Operation Count")
    plt.plot(edges_list, acs, label="Access Count")
    plt.xlabel(r"edges")
    plt.legend()
    plt.title(r"Running time as #edges varies")
    plt.show()

    plt.plot(edges_list, err, label="Error Ratio")
    plt.xlabel(r"edges")
    plt.title(r"Error ratio as #edges varies")
    plt.legend()
    """

    """
    cs = []
    for eps in [0.05, 0.1, 0.2, 0.4, 0.8]:
        c = best_c(graph, 0.5)
        print("Best c:", c)
        cs.append(c)
    print(eps, cs)
    """

    """
    # Make graph for finding optimal $c$:

    ops_data = []
    acs_data = []
    err_data = []
    eps_list = [0.1*i for i in range(1, 10)]
    c_list = [0.01*2**i for i in range(11)]
    for c in c_list:
        eps = 0.2
        ops, acs, err, opt_err = test(graph, eps, c)
        ops_data.append(ops)
        acs_data.append(acs)
        err_data.append(err / opt_err)
        print("(Graph Length, epsilon, c) =", len(graph), eps, c)
        print("(Operations, Graph accesses) =", ops, acs)
        print("(Clustering error, Optimal error, ratio) =", err, opt_err, err / opt_err)


    ops = np.array(ops_data)
    acs = np.array(acs_data)
    err = np.array(err_data)
    plt.plot(c_list, ops, label="Operation Count")
    plt.plot(c_list, acs, label="Access Count")
    plt.xlabel(r"$c$")
    plt.legend()
    plt.show()

    plt.plot(c_list, err, label="Error Ratio")
    plt.xlabel(r"$c$")
    plt.legend()
    """


    # Make graph for finding optimal epsilon

    fig, axs = plt.subplots(2, 2)
    for ax, percentile in zip(axs.flat, [0.0002, 0.004, 0.08, 1.6]):
        percentile /= 100
        graph = vector_graph(10000, percentile, percentile)
        ops_data = []
        acs_data = []
        err_data = []
        eps_list = [0.04861111*i for i in range(2, 20)]
        for eps in eps_list:
            c = 1
            ops, acs, err, opt_err = test(graph, eps, c)
            ops_data.append(ops)
            acs_data.append(acs)
            err_data.append(err / opt_err)
            print("(Graph Length, epsilon, c) =", len(graph), eps, c)
            print("(Operations, Graph accesses) =", ops, acs)
            print("(Clustering error, Optimal error, ratio) =", err, opt_err, err / opt_err)


        ops = np.array(ops_data)
        acs = np.array(acs_data)
        err = np.array(err_data)
        """
        ax.plot(eps_list, ops, label="Operation Count")
        ax.plot(eps_list, acs, label="Access Count")
        ax.set_xlabel(r"$\varepsilon$")
        ax.legend()
        ax.set_title(r"Running time as $\varepsilon$ varies")
        plt.show()
        """

        ax.plot(eps_list, err, label="Error Ratio")
        ax.set_xlabel(r"$\varepsilon$")
        ax.set_title(r"Error ratio as $\varepsilon$ varies, percentile="+str(percentile*100)+r"%")
        ax.legend()

    plt.show()

    """
    x, y = np.meshgrid(eps_list, c_list)
    indices = np.meshgrid(np.arange(len(eps_list)), np.arange(len(c_list)))

    fig, axs = plt.subplots(2, 2)
    axs[0, 0].set_title("Operation Count")
    axs[0, 0].scatter(x, y, c=ops[indices], cmap="gray")
    axs[0, 1].set_title("Graph Access Count")
    axs[0, 1].scatter(x, y, c=acs[indices], cmap="gray")
    axs[1, 0].set_title("Error ratio")
    axs[1, 0].scatter(x, y, c=err[indices], cmap="gray")

    for ax in axs.flat:
        ax.set_xlabel(r"$\varepsilon$")
        ax.set_ylabel(r"$c$")
    """

    plt.show()
