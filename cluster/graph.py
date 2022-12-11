import random

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

    def deg(self, sign, v):
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


class RandomGraph(Graph):
    def __init__(self, num_vertices, num_clusters, flip=0.05, keep_inside=0.2, keep_outside=0.05):
        """
        Create a random graph. The random graph is created so that
        the optimum solution has `num_clusters` clusters and
        `num_vertices` vertices.

        `keep` is the chance that a correlation is flipped either
        between cliques or within a clique. `keep` is the
        probability that an edge's correlation is kept (i.e.
        marked as either + or -) instead of just not showing
        up.
        """
        if num_clusters > num_vertices:
            raise ValueError("You can't have more clusters than vertices!")

        vertices = list(range(num_vertices))
        super().__init__(vertices)

        break_points = random.sample(
            list(range(1, num_vertices)),
            num_clusters - 1
        )
        break_points.sort()
        break_points = [0] + break_points + [num_vertices]
        self.optimal_clusters = [
            self.vertices[i:j]
            for i, j in zip(break_points[:-1], break_points[1:])
        ]


        # Add correlations between nodes in the same cluster
        for cluster in self.optimal_clusters:
            lines1_plus = {v1: set() for v1 in cluster}
            lines1_minus = {v1: set() for v1 in cluster}
            lines2_plus = {v2: set() for v2 in cluster}
            lines2_minus = {v2: set() for v2 in cluster}

            for i, v1 in enumerate(cluster):
                for v2 in cluster[:i]:
                    if random.random() >= keep_inside:
                        continue # skip over a lot of edges
                    correlation = "-" if random.random() < flip else "+"
                    if correlation == "+":
                        lines1_plus[v1].add(v2)
                        lines2_plus[v2].add(v1)
                    else:
                        lines1_minus[v1].add(v2)
                        lines2_minus[v2].add(v1)

            lines1_plus = list(lines1_plus.items())
            lines1_minus = list(lines1_minus.items())
            lines2_plus = list(lines2_plus.items())
            lines2_minus = list(lines2_minus.items())

            self.add("+", lines1_plus)
            self.add("-", lines1_minus)
            self.add("+", lines2_plus)
            self.add("-", lines2_minus)

        # Add correlations between different clusters
        for i, cluster1 in enumerate(self.optimal_clusters):
            for cluster2 in self.optimal_clusters[:i]:
                lines1_plus = {v1: set() for v1 in cluster1}
                lines1_minus = {v1: set() for v1 in cluster1}
                lines2_plus = {v2: set() for v2 in cluster2}
                lines2_minus = {v2: set() for v2 in cluster2}

                for v1 in cluster1:
                    for v2 in cluster2:
                        if random.random() >= keep_outside:
                            continue # skip over a lot of edges
                        correlation = "+" if random.random() < flip else "-"
                        if correlation == "+":
                            lines1_plus[v1].add(v2)
                            lines2_plus[v2].add(v1)
                        else:
                            lines1_minus[v1].add(v2)
                            lines2_minus[v2].add(v1)

                lines1_plus = list(lines1_plus.items())
                lines1_minus = list(lines1_minus.items())
                lines2_plus = list(lines2_plus.items())
                lines2_minus = list(lines2_minus.items())

                self.add("+", lines1_plus)
                self.add("-", lines1_minus)
                self.add("+", lines2_plus)
                self.add("-", lines2_minus)

if __name__ == "__main__":
    # Test out the RandomGraph
    graph = RandomGraph(50, 5)
    print(graph.optimal_clusters)
    print("\n\nPLUS")
    print(graph.plus)
    print("\n\nMINUS")
    print(graph.minus)

    import networkx as nx
    import matplotlib.pyplot as plt
    G = nx.Graph()

    colors = ['#000000', '#00FF00', '#0000FF', '#FF0000', '#01FFFE', '#FFA6FE', '#FFDB66', '#006401', '#010067', '#95003A', '#007DB5', '#FF00F6', '#FFEEE8', '#774D00', '#90FB92', '#0076FF', '#D5FF00', '#FF937E', '#6A826C', '#FF029D', '#FE8900', '#7A4782', '#7E2DD2', '#85A900', '#FF0056', '#A42400', '#00AE7E', '#683D3B', '#BDC6FF', '#263400', '#BDD393', '#00B917', '#9E008E', '#001544', '#C28C9F', '#FF74A3', '#01D0FF', '#004754', '#E56FFE', '#788231', '#0E4CA1', '#91D0CB', '#BE9970', '#968AE8', '#BB8800', '#43002C', '#DEFF74', '#00FFC6', '#FFE502', '#620E00', '#008F9C', '#98FF52', '#7544B1', '#B500FF', '#00FF78', '#FF6E41', '#005F39', '#6B6882', '#5FAD4E', '#A75740', '#A5FFD2', '#FFB167', '#009BFF', '#E85EBE']

    color_map = []
    for i, cluster in enumerate(graph.optimal_clusters):
        for v in cluster:
            G.add_node(v)
            color_map.append(colors[i%len(colors)])

    for v1 in graph.minus:
        for v2 in graph.minus[v1]:
            G.add_edge(v1, v2, weight=-1, color="red")
    for v1 in graph.plus:
        for v2 in graph.plus[v1]:
            G.add_edge(v1, v2, weight=1, color="blue")


    pos = nx.shell_layout(G)
    edges = G.edges()
    colors = [G[u][v]['color'] for u,v in edges]
    weights = [G[u][v]['weight'] for u,v in edges]

    nx.draw(G, pos, node_color=color_map, edge_color=colors, width=weights)
    plt.show()
