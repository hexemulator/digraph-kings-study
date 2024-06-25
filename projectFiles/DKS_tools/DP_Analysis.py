'''
Tools for Direct Product Analysis
'''
import networkx as nx

"""
Class for performing direct product analysis on digraphs.
"""
class DP_Analysis:
    def __init__(self, G: nx.DiGraph, H: nx.DiGraph):
        self.G = G
        self.H = H
        self.GxH = nx.tensor_product(self.G, self.H)
        self.upper_bound = self.G.order() * self.H.order()

    def identify_maximal_k_king_vertices(self, DiGraph: nx.DiGraph):
        dg_k_kings = []

        for node in DiGraph.nodes:
            try:
                k_val = nx.eccentricity(DiGraph, node)
                node_k_pair = [node,k_val]
                dg_k_kings.append(node_k_pair)
            except:
                pass

        print(dg_k_kings) # debug
        return dg_k_kings

# function to move directed edge from one pair of vertices to another pair
