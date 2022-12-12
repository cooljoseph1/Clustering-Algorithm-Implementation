from graph import Graph

def word_graph():
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
    print(sum(len(x) for x in graph.plus.values()))
    print(sum(len(x) for x in graph.minus.values()))
    print(graph.plus["good"])
    print(graph.minus["bad"])
    raise Exception("ENDTHIS")
    """

    return graph
