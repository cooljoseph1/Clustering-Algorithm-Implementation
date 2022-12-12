from graph import Graph, RandomGraph
from cluster import Cluster

if __name__ == "__main__":
    """
    # Load word data.
    with open("data/words.txt") as f:
        words = set(f.read().split("\n"))

    # Create graph.
    graph = Graph(words)

    # Add antonyms
    lines = []
    with open("data/antonyms.txt") as f:
        antonyms = f.read()
    for line in antonyms.split("\n"):
        if len(line.split("|")) == 1:
            continue
        v, N = line.split("|")
        if v not in words:
            continue
        lines.append((v, words & set(N.split(","))))
    graph.add("-", lines)

    # Add synonyms
    lines = []
    with open("data/synonyms.txt") as f:
        synonyms = f.read()
    for line in synonyms.split("\n"):
        if len(line.split("|")) == 1:
            continue
        v, N = line.split("|")
        if v not in words:
            continue
        lines.append((v, words & set(N.split(","))))
    graph.add("+", lines)
    """
    graph = RandomGraph(1000, 1000000, 100, prob_flip=0.001)
    labels, clusters = Cluster(graph)
    #print(labels["angry"], clusters[10])
