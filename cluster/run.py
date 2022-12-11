class Graph(object):
    def __init__(self, vertices):
        # List of vertices. Can be words, numbers, anything hashable.
        self.vertices = vertices
        self.minus = {v: set() for v in vertices}
        self.plus = {v: set() for v in vertices}
    def add(self, sign="+", lines=[]):
        """Lines should have the following format
        v1,[u11,u12,u13,...]
        v2,[u21,u22,u23,...]
        """
        if sign == "+":
            adj = self.plus
        elif sign == "-":
            adj = self.minus
        else:
            raise ValueError("Sign must be + or -.")

        for v, N in lines:
            adj[v] |= N

    def deg(self, sign="+", v):
        if sign == "+":
            return len(self.plus[v])
        elif sign == "-":
            return len(self.minus[v])
        else:
            raise KeyError("Invalid sign, should be either + or -.")

    def __len__(self):
        return len(self.vertices)

    def __getitem__(self, key):
        """Key should be of the following format:
        ("+/-", vertex)
        """
        sign, v = key
        if sign == "+":
            return self.plus[v]
        elif sign == "-":
            return self.minus[v]
        else:
            raise KeyError("Invalid sign, should be either + or -.")
    def __add__(self, other):
        if not isinstance(other, list):
            raise TypeError("Addition has been overloaded to accessing graph+.")
        if len(other) != 1:
            raise NotImplementedError("Can only access one value for now.")
        return self[("+", other[0])]
    def __sub__(self, other):
        if not isinstance(other, list):
            raise TypeError("Addition has been overloaded to accessing graph-.")
        if len(other) != 1:
            raise NotImplementedError("Can only access one value for now.")
        return self[("-", other[0])]

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

# Test
print(graph+["fast"], graph-["slow"])

"""
Main algorithm, pulled from
https://arxiv.org/pdf/2109.14528.pdf
"""

from math import log
import random
random.seed(1234)

class Laminar(object):
    def __init__(self, parent=None, ):
        self.

def Cluster(G, eps=0.01, c=10):
    # Constants
    epsP = 7 * eps
    epsp = eps / 7
    deltaP = 4 * eps
    deltap = eps / 4

    n = len(G)
    t = c * log(n) / eps**2

    # (ii)
    deg = {v: G.deg("+", v) for v in G.vertices}

    # (iii)
    N_sample = {}
    for v in G.vertices:
        N_sample[v] = [random.choice(G+[v]) for i in range(t)]

    # (iv)
    Sample = []
    for v in G.vertices:
        if random.random() < c * log(n) / deg[v]:
            Sample.append(v)
    N_plus = {v: G+[v] for v in Sample}

    # (v)
    def low(v, e): # eps low?
        return set(filter(lambda u: deg[u] <= (1+e)*deg[v], N_plus[v]))
    def light(v, e, d): # eps-delta light?
        return len(low(v, e)) < (1 - d) * deg[v]

    def sparse_tester(u, v, low_epsP):
        # u is in low_epsP = low(v, epsP)
        if deg[u] < (1 - 2*eps) * deg[v]:
            return True
        if len(low_epsP & N_sample[u]) < (1 - deltaP) * t:
            return True
        return False

    def C(u, v, low_epsP):
        # u is in low_epsP = low(v, epsP)
        if deg[u] > (1 + 2*epsP + 2 * deltaP) * deg[v]:
            return False
        if len(N_sample[u] & low_epsP) < (1 - 6*epsP - 6 * deltaP - eps) * t * deg[v]/deg[u]:
            return False
        return True

    def C_tilde(v, low_epsP):
        return set(filter(lambda u: C(u, v, low_epsP), low_epsP))

    # Build up dense D
    D = set()
    for v in Sample:
        if len(low(v, eps)) < (1 - eps) * deg[v]: # light tester
            continue

        low_epsP = low(v, epsP)
        S = set(filter(lambda u: sparse_tester(u, v, low_epsP), low_epsP))
        D |= low7e - S

    # Unsure how to build C_v roots K_i



    def isolated(v, e=eps):
        return filter(lambda u: len(low(v, e) - neighbors(u)) >= e * deg[v], N_plus[v])
