import random
import traceback
class OperationCounter(object):
    def __init__(self):
        self.operation_count = 0 # Cost for +, -, *, and / between real numbers or integers.
        self.set_intersection_count = 0
        self.graph_access_count = 0
        self.tagged_counts = {}

    def add(self, amount=1, tag=None):
        """
        Keep track of one operation (e.g. +, 0, *, /).
        """
        self.operation_count += amount
        if tag is not None:
            self.tagged_counts[tag] = self.tagged_counts.get(tag, 0) + amount
        #if random.random() < amount * 1e-7:
        #   raise Exception("")

    def add_set_intersection(self, set1, set2, tag=None):
        """
        Keep track of one set intersection.

        The cost of a set intersection is
        the minimum of the two lengths of
        the sets being added.
        """
        self.add(min(len(set1), len(set2)), tag=tag)

    def add_graph_access(self, amount=1):
        """
        Keep track of graph access operations, like checking
        the degree of a vertex or getting a random neighbor.
        """
        self.graph_access_count += amount
        self.add(amount, tag="graph_access")

def laminar_difference(candidates):
    # Use symmetric difference between sets.
    pass
