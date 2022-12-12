from graph import Graph, RandomGraph
from cluster import cluster

def test(graph, eps, c):
    labels, clusters, operation_counter = cluster(graph, eps, c)
    error = graph.get_clustering_error(labels)
    opt_error = graph.get_optimum_clustering_error()
    for tag in operation_counter.tagged_counts:
        print("Operation count for", tag, "is", operation_counter.tagged_counts[tag])
    return operation_counter.operation_count, operation_counter.graph_access_count, error, opt_error



if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    vertices, edges, clusters, prob_flip = 1_000, 100_000, 10, 0.01
    graph = RandomGraph(vertices, edges, clusters, prob_flip)



    ops_data = []
    acs_data = []
    err_data = []
    eps_list = [0.05, 0.1, 0.2, 0.4, 0.8]
    c_list = [0.04, 0.2, 1, 5, 25]
    for eps in eps_list:
        o = []
        a = []
        e = []
        for c in c_list:
            ops, acs, err, opt_err = test(graph, eps, c)
            o.append(ops)
            a.append(acs)
            e.append(err / opt_err)
            print("(Graph Length, epsilon, c) =", len(graph), eps, c)
            print("(Operations, Graph accesses) =", ops, acs)
            print("(Clustering error, Optimal error, ratio) =", err, opt_err, err / opt_err)
        ops_data.append(o)
        acs_data.append(a)
        err_data.append(e)

    x, y = np.meshgrid(eps_list, c_list)
    indices = np.meshgrid(np.arange(len(eps_list)), np.arange(len(c_list)))
    ops = np.array(ops_data)
    acs = np.array(acs_data)
    err = np.array(err_data)

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


    plt.show()
