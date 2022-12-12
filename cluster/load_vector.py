import numpy as np
from graph import Graph

def vector_graph(word_count=None, plus_fraction=0.05, minus_fraction=0.05):
    # Load word data.
    with open("word_vector/words.txt") as f:
        words = f.read().split("\n")
    N = word_count or len(words)
    N = min(N, len(words))
    words = words[:N]

    # Create graph.
    graph = Graph(set(words))

    array = np.load("word_vector/correlations.npy")
    array = array[:N, :N]
    positive_correlations = (array > np.percentile(array, 100 * (1 - plus_fraction)))
    negative_correlations = (array <= np.percentile(array, 100 * minus_fraction))

    for i, j in np.transpose(positive_correlations.nonzero()):
        graph.plus[words[i]].append(words[j])
    for i, j in np.transpose(negative_correlations.nonzero()):
        graph.minus[words[i]].append(words[j])

    return graph
