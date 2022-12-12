from graph import Graph, RandomGraph
from cluster import cluster

def test(graph, eps, c):
    labels, clusters, operation_counter = cluster(graph, eps, c)
    return operation_counter.operation_count, operation_counter.graph_access_count



if __name__ == "__main__":
    import seaborn as sns
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm
    import pandas as pd

    vertices, edges, clusters, prob_flip = 1_000, 100_000, 10, 0.01
    graph = RandomGraph(vertices, edges, clusters, prob_flip)



    ops_data = []
    acs_data = []
    eps_list = [0.05, 0.1, 0.2, 0.4, 0.8]
    c_list = [0.04, 0.2, 1, 5, 25]
    for eps in eps_list:
        o = []
        a = []
        for c in c_list:
            ops, acs = test(graph, eps, c)
            o.append(ops)
            a.append(acs)
            print(eps, c, ops, acs)

            print(len(graph), eps, c, ops, acs)
        ops_data.append(o)
        acs_data.append(a)

    ops_df = pd.DataFrame(ops_data, index=c_list, columns=eps_list)
    acs_df = pd.DataFrame(acs_data, index=c_list, columns=eps_list)

    ax = sns.heatmap(ops_data, norm=LogNorm())
    ax.set_xlabel(r"$\varepsilon$")
    ax.set_ylabel(r"$c$")
    plt.show()

    ax = sns.heatmap(acs_data, norm=LogNorm())
    ax.set_xlabel(r"$\varepsilon$")
    ax.set_ylabel(r"$c$")
    plt.show()
