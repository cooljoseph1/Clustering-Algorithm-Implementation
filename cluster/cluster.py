"""
Main algorithm, pulled from
https://arxiv.org/pdf/2109.14528.pdf
"""

from math import log
import random
random.seed(1234)

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

    # (iii)
    N_sample = {}
    for v in G.vertices:
        if len(G+[v]) == 0:
            N_sample[v] = set()
            continue
        N_sample[v] = set(random.choices(list(G+[v]), k=t))

    # (iv)
    Sample = []
    for v in G.vertices:
        if deg[v] > 0 and random.random() < c * log(n) / deg[v]:
            Sample.append(v)
    N_plus = {v: G+[v] for v in Sample}

    # (v)
    def low(v, e): # eps low?
        return set(filter(lambda u: deg[u] <= (1+e)*deg[v], N_plus[v]))

    def light(v, e, d): # eps-delta light?
        return len(low(v, e)) < (1 - d) * deg[v]

    # neighbors isn't defined, but I don't think isolated is used anywhere...
    def isolated(v, e=eps):
        return filter(lambda u: len(low(v, e) - neighbors(u)) >= e * deg[v], N_plus[v])

    def sparse_tester(u, v, low_epsP):
        # u is in low_epsP = low(v, epsP)
        if deg[u] < (1 - 2*eps) * deg[v]:
            return True
        if len(low_epsP & N_sample[u]) < (1 - deltaP) * t:
            return True
        return False

    def C_filter(u, v, low_epsP):
        # u is in low_epsP = low(v, epsP)
        if deg[u] > (1 + 2*epsP + 2 * deltaP) * deg[v]:
            return False
        if deg[u] > 0 and len(N_sample[u] & low_epsP) < (1 - 6*epsP - 6 * deltaP - eps) * t * deg[v]/deg[u]:
            return False
        return True

    def C_tilde(v, low_epsP):
        return {v} | set(filter(lambda u: C_filter(u, v, low_epsP), low_epsP))

    # Build up dense D
    print("Building D...")
    D = set(Sample)
    for v in Sample:
        if len(low(v, eps)) < (1 - eps) * deg[v]: # light tester
            D -= {v}
            continue

        low_epsP = low(v, epsP)
        S = set(filter(lambda u: sparse_tester(u, v, low_epsP), low_epsP))
        D -= S

    # Build candidate sets
    print("Building candidate sets...")
    candidates = {v: [] for v in G.vertices}
    candidate_sets = []
    for v in D:
        low_epsP = low(v, epsP)
        Cv = C_tilde(v, low_epsP)
        candidate_sets.append(Cv)
        for u in Cv:
            candidates[u].append(Cv)
    candidates = {key: value for key, value in candidates.items() if value != []}

    # Build cliques
    print("Building cliques...")
    cliques = []
    while len(candidates) > 0:
        u = next(iter(candidates))
        Cv = max(candidates[u], key=len)
        cliques.append(Cv)
        for v in Cv:
            candidates.pop(v, None)
        candidate_sets.remove(Cv)

    # (vi)
    print("Labelling...")
    labels = {v: -1 for v in G.vertices}
    for i, clique in enumerate(cliques):
        for v in clique:
            labels[v] = i
    clusters = {}
    for v, l in labels.items():
        if l in clusters:
            clusters[l] |= {v}
        else:
            clusters[l] = {v}
    return labels, clusters
