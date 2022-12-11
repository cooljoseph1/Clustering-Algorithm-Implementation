class Graph(object):
    def __init__(self, vertices):
        # List of vertices. Can be words, numbers, anything hashable.
        self.vertices = vertices
        self.minus = dict((v, set()) for v in vertices)
        self.plus = dict((v, set()) for v in vertices)
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
        return self.plus[other[0]]
    def __sub__(self, other):
        if not isinstance(other, list):
            raise TypeError("Addition has been overloaded to accessing graph-.")
        if len(other) != 1:
            raise NotImplementedError("Can only access one value for now.")
        return self.minus[other[0]]

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

def Cluster(G, eps=0.01, c=10):
    # (ii)
    deg = {(v, G.deg("+", v)) for v in G.vertices}

    # (iii)
    n = len(G)
    t = c * log(n) / eps**2
    N_sample = {}
    for v in G.vertices:
        N_sample[v] = [random.choice(G+[v]) for i in range(t)]

    # (iv)
    Sample = []
    for v in G.vertices:
        if random.random() < c * log(n) / deg[v]:
            Sample.append(v)
    N_plus = {(v, G+[v]) for v in Sample}

    # (v)
    
