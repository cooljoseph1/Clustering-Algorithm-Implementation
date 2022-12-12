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
    vertices, edges, clusters, prob_flip = 1_000, 1_000_000, 10, 0.01
    graph = RandomGraph(vertices, edges, clusters, prob_flip)


    for eps in [0.05, 0.1, 0.2, 0.4, 0.8]:
        for c in [0.04, 0.2, 1, 5, 25]:
            ops, acs, err, opt_err = test(graph, eps, c)
            print("(Graph Length, epsilon, c) =", len(graph), eps, c)
            print("(Operations, Graph accesses) =", ops, acs)
            print("(Clustering error, Optimal error, ratio) =", err, opt_err, err / opt_err)
