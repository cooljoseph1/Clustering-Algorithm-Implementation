from graph import Graph, RandomGraph
from cluster import cluster

def test(graph, eps, c):
    labels, clusters, operation_counter = cluster(graph, eps, c)
    return operation_counter.operation_count, operation_counter.graph_access_count



if __name__ == "__main__":
    vertices, edges, clusters, prob_flip = 1_000, 100_000, 10, 0.01
    graph = RandomGraph(vertices, edges, clusters, prob_flip)


    for eps in [0.05, 0.1, 0.2, 0.4, 0.8]:
        for c in [0.04, 0.2, 1, 5, 25]:
            ops, acs = test(graph, eps, c)
            print(len(graph), eps, c, ops, acs)
