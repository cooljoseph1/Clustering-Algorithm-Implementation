"""
Main algorithm, pulled from
https://arxiv.org/pdf/2109.14528.pdf
"""

from math import log
import random
random.seed(1234)

from operation_counter import OperationCounter

operationCounter = OperationCounter()

def Cluster(G, eps=0.24, c=0.1):
    # Constants
    epsP = 7 * eps
    epsp = eps / 7
    deltaP = 4 * eps
    deltap = eps / 4

    n = len(G)
    t = int(c * log(n) / eps**2)
    print(eps, c, n, t)

    # (ii)
    deg = {v: G.deg("+", v) for v in G.vertices}
    operationCounter.add_graph_access(len(G.vertices))

    # (iii)
    N_sample = {}
    for v in G.vertices:
        operationCounter.add_graph_access(1)
        if len(G+[v]) == 0:
            N_sample[v] = set()
            continue
        N_sample[v] = set(random.choices(G+[v], k=t))
        operationCounter.add_graph_access(t)

    # (iv)
    Sample = []
    for v in G.vertices:
        operationCounter.add(8)
        if deg[v] > 0 and random.random() < c * log(n) / deg[v]:
            Sample.append(v)
    N_plus = {v: G+[v] for v in Sample}
    for v in Sample:
        operationCounter.add_graph_access(len(G+[v]))

    # (v)
    def low(v, e): # eps low?
        operationCounter.add(6 * len(N_plus[v]))
        return set(filter(lambda u: deg[u] <= (1+e)*deg[v], N_plus[v]))

    def light_tester(v): # eps-delta light?
        operationCounter.add(8)
        return len(low(v, eps)) < (1 - eps) * deg[v]

    def isolated_tester(u, v, low_epsP):
        # u is in low_epsP = low(v, epsP)
        operationCounter.add(6)
        if deg[u] < (1 - 2*eps) * deg[v]:
            return True
        operationCounter.add_set_intersection(low_epsP, N_sample[u])
        operationCounter.add(5)
        if len(low_epsP & N_sample[u]) < (1 - deltaP) * t:
            return True
        return False

    def sparse_tester(v):
        operationCounter.add(3)
        low_epsP = low(v, epsP)
        operationCounter.add(6 * len(low_epsP))
        I = set(filter(lambda u: isolated_tester(u, v, low_epsP), low_epsP))
        operationCounter.add(5)
        if len(I) >= 2*eps*deg[v]:
            return True
        return False

    def C_filter(u, v, low_epsP):
        # u is in low_epsP = low(v, epsP)
        operationCounter.add(8)
        if deg[u] > (1 + 2*epsP + 2 * deltaP) * deg[v]:
            return False
        operationCounter.add(15)
        operationCounter.add_set_intersection(N_sample[u], low_epsP)
        if deg[u] > 0 and len(N_sample[u] & low_epsP) < (1 - 6*epsP - 6 * deltaP - eps) * t * deg[v]/deg[u]:
            return False
        return True

    def C_tilde(v, low_epsP):
        operationCounter.add(1 + 6 * len(low_epsP))
        return {v} | set(filter(lambda u: C_filter(u, v, low_epsP), low_epsP))

    # Build up dense D
    print("Building D...")
    operationCounter.add(4 * len(Sample))
    D = [v for v in Sample if not light_tester(v) and not sparse_tester(v)]

    # Build candidate sets
    print("Building candidate sets...")
    operationCounter.add(len(G.vertices))
    candidates = {v: [] for v in G.vertices}
    candidate_sets = []
    for v in D:
        operationCounter.add(7)        
        low_epsP = low(v, epsP)
        Cv = C_tilde(v, low_epsP)
        candidate_sets.append(Cv)
        for u in Cv:
            operationCounter.add(2)
            candidates[u].append(Cv)
    operationCounter.add(len(candidates))
    candidates = {key: value for key, value in candidates.items() if value != []}

    # Build cliques
    print("Building cliques...")
    cliques = []
    print("Candidate length is", len(candidates))
    while len(candidates) > 0:
        operationCounter.add(len(candidates) * 3, tag="inefficient building of cliques")
        u = next(iter(candidates))
        Cv = max(candidates[u], key=len)
        cliques.append(Cv)
        for v in Cv:
            candidates.pop(v, None)
        candidate_sets.remove(Cv)

    # (vi)
    print("Labelling...")
    operationCounter.add(len(G.vertices))
    labels = {v: -1 for v in G.vertices}
    for i, clique in enumerate(cliques):
        operationCounter.add(len(clique))
        for v in clique:
            labels[v] = i
    clusters = {}
    for v, l in labels.items():
        operationCounter.add(2)
        if l in clusters:
            clusters[l] |= {v}
        else:
            clusters[l] = {v}

    
    print("\n\nOPERATION TIMES")
    print("Operation count:", operationCounter.operation_count)
    print("Graph access count:", operationCounter.graph_access_count)
    for tag in operationCounter.tagged_counts:
        print("Tag", tag, "count:", operationCounter.tagged_counts[tag])
    
    return labels, clusters
