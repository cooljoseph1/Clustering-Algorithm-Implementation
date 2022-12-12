"""
Main algorithm, pulled from
https://arxiv.org/pdf/2109.14528.pdf
"""

from math import log
import random
random.seed(1234)

from counter import *

class Node(object):
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)

class LinkedList(object):
    def __init__(self, lis=None):
        if lis is None or len(lis) == 0:
            self.start = None
        else:
            self.start = lis[0]
            self.last = lis[0]
            for node in lis[1:]:
                self.append(node)
    def append(self, node):
        if self.start:
            self.last.right = node
            node.left = self.last
            self.last = node
        else:
            self.start = node
            self.last = node
    def remove(self, node):
        if node.left:
            node.left.right = node.right
        if node.right:
            node.right.left = node.left

    def __iter__(self):
        node = self.start
        while node:
            yield node
            node = node.right
    def __repr__(self):
        return str([node.data for node in self])

def cluster(G, eps=0.2, c=0.1, verbose=0):
    """
    G - graph to cluster.
    eps - lower = more accurate clusters.
    c - constant multiplier to number of samples. Higher = more accurate but slower.
    verbose - 0 = silent, 1 = minimal information, 2 = operation counts.
    """
    operation_counter = OperationCounter()
    # Constants
    epsP = 7 * eps
    epsp = eps / 7
    deltaP = 4 * eps
    deltap = eps / 4

    n = len(G)
    t = int(c * log(n) / eps**2)

    # (ii)
    deg = {v: G.deg("+", v) for v in G.vertices}
    operation_counter.add_graph_access(len(G.vertices))

    # (iii)
    N_sample = {}
    for v in G.vertices:
        operation_counter.add_graph_access(1)
        if len(G+[v]) == 0:
            N_sample[v] = set()
            continue
        N_sample[v] = set(random.choices(G+[v], k=t))
        operation_counter.add_graph_access(t)

    # (iv)
    Sample = []
    for v in G.vertices:
        operation_counter.add(8)
        if deg[v] > 0 and random.random() < c * log(n) / deg[v]:
            Sample.append(v)
    N_plus = {v: G+[v] for v in Sample}
    for v in Sample:
        operation_counter.add_graph_access(len(G+[v]))

    # (v)
    def low(v, e): # eps low?
        operation_counter.add(6 * len(N_plus[v]))
        return set(filter(lambda u: deg[u] <= (1+e)*deg[v], N_plus[v]))

    def light_tester(v): # eps-delta light?
        operation_counter.add(8)
        result = len(low(v, eps)) < (1 - eps) * deg[v]
        if result:
            operation_counter.add(1, tag="Light tester removed candidate!")
        return result

    def isolated_tester(u, v, low_epsP):
        # u is in low_epsP = low(v, epsP)
        operation_counter.add(6)
        if deg[u] < (1 - 2*eps) * deg[v]:
            return True
        operation_counter.add_set_intersection(low_epsP, N_sample[u])
        operation_counter.add(5)
        if len(low_epsP & N_sample[u]) < (1 - deltaP) * t:
            return True
        return False

    def sparse_tester(v):
        operation_counter.add(3)
        low_epsP = low(v, epsP)
        operation_counter.add(6 * len(low_epsP))
        I = set(filter(lambda u: isolated_tester(u, v, low_epsP), low_epsP))
        operation_counter.add(5)
        if len(I) >= 2*eps*deg[v]:
            operation_counter.add(1, tag="Sparse tester removed candidate!")
            return True
        return False

    def C_filter(u, v, low_epsP):
        # u is in low_epsP = low(v, epsP)
        operation_counter.add(8)
        if deg[u] > (1 + 2*epsP + 2 * deltaP) * deg[v]:
            return False
        operation_counter.add(15)
        operation_counter.add_set_intersection(N_sample[u], low_epsP)
        if deg[u] > 0 and len(N_sample[u] & low_epsP) < (1 - 6*epsP - 6 * deltaP - eps) * t * deg[v]/deg[u]:
            return False
        return True

    def C_tilde(v, low_epsP):
        operation_counter.add(1 + 6 * len(low_epsP))
        return {v} | set(filter(lambda u: C_filter(u, v, low_epsP), low_epsP))

    # Build up dense D
    if verbose > 0:
        print("Building D...")
    operation_counter.add(4 * len(Sample))
    print("Sample length is", len(Sample))
    D = [v for v in Sample if (not light_tester(v)) & (not sparse_tester(v))]

    # Build candidate sets
    if verbose > 0:
        print("Building candidate sets...")
    operation_counter.add(len(G.vertices))
    candidates = {v: [] for v in G.vertices}


    candidate_sets = LinkedList()
    for v in D:
        operation_counter.add(10)
        low_epsP = low(v, epsP)
        Cv = Node(C_tilde(v, low_epsP))
        candidate_sets.append(Cv)
        for u in Cv:
            operation_counter.add(2)
            candidates[u].append(Cv)
    operation_counter.add(len(candidates))
    candidates = {key: value for key, value in candidates.items() if value != []}

    # Build cliques
    cliques = []
    if verbose > 0:
        print("Building cliques...")
        print("Candidate length is", len(candidates))
    while len(candidates) > 0:
        u = next(iter(candidates))
        Cv = max(candidates[u], key=len)
        cliques.append(Cv)
        for v in Cv:
            candidates.pop(v, None)

        operation_counter.add(4)
        candidate_sets.remove(Cv)

    # (vi)
    if verbose > 0:
        print("Labelling...")
    operation_counter.add(len(G.vertices))
    labels = {v: -1 for v in G.vertices}
    for i, clique in enumerate(cliques):
        operation_counter.add(len(clique))
        for v in clique:
            labels[v] = i
    clusters = {}
    for v, l in labels.items():
        operation_counter.add(2)
        if l in clusters:
            clusters[l] |= {v}
        else:
            clusters[l] = {v}


    if verbose > 1:
        print("\n\nOPERATION TIMES")
        print("Operation count:", operation_counter.operation_count)
        print("Graph access count:", operation_counter.graph_access_count)
        for tag in operation_counter.tagged_counts:
            print("Tag", tag, "count:", operation_counter.tagged_counts[tag])

    return labels, clusters, operation_counter
