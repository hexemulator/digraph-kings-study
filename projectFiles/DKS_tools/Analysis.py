'''
Tools for Direct Product Analysis
'''
import networkx as nx
import math as m
import functools as ft

class Digraph:
    '''
    Instantiated with a DiGraph object.
    '''
    def __init__(self, D: nx.DiGraph, is_tournament:bool=False):
        '''
        :param D: DiGraph as given by networkx.DiGraph
        :param is_tournament: whether the DiGraph should be interpreted as a tournament, default is False
        '''
        self.D: nx.DiGraph = D
        self.is_T: bool = is_tournament
        self.D_kings: list = self.find_kings()      # gets list of king vertices

        if self.D_kings != []:
            self.set_Sv()

    def find_kings(self) -> list:
        '''
        identifies 'king' nodes in the DiGraph, and gives each node a 'k_val' equal to the node's eccentricity
        :param is_T: if DiGraph has been identified as a tournament, then king vertices in tournaments need k_val <= 2
        :return: list of kings in DiGraph
        '''

        king_list = list()

        # for each node in the digraph, attempt to get eccentricity
        for node in self.D.nodes:
            try:
                k_val = nx.eccentricity(self.D, node)
                self.D.nodes[node]['k_val'] = k_val                       # if successful, store K-value in node itself
                king_list.append(node)

            except:
                pass

        return king_list

    def set_Sv(self):
        '''
        For each king in DiGraph, fills Sv set of king, and calculates GCD(Sv):
        - Sv is the set of non-negative integer lengths of closed diwalks containing king
        - GCD(Sv) is the greatest common divisor of all integers lengths contained in Sv
        '''

        # each king is given a value key 'Sv' that is assigned a set()
        for king in self.D_kings:
            self.D.nodes[king]['Sv'] = set()

        # grab all cycles in the digraph D
        all_simple_cycles = nx.simple_cycles(self.D, self.D.order())

        # looks at each node in cycles individually, if node is king, it adds len of cycle to Sv set of node
        for cycle in all_simple_cycles:
            for node in cycle:
                if node in self.D_kings:
                    self.D.nodes[node]['Sv'].add(len(cycle))

        # for each king, we then want to calculate the gcd of it's Sv
        for king in self.D_kings:
            if len(list(self.D.nodes[king]['Sv'])) == 0:
                self.D.nodes[king]['Sv'] = {0}                # deals with kings NOT on cycles

            if len(list(self.D.nodes[king]['Sv'])) == 1:      # if Sv only has one length, then it is its GCD(Sv)
                self.D.nodes[king]['GCD(Sv)'] = list(self.D.nodes[king]['Sv'])[0]
            else:                                               # otherwise, we can calculate its GCD(Sv)
                self.D.nodes[king]['GCD(Sv)'] = ft.reduce(m.gcd, self.D.nodes[king]['Sv'])

    def list_kings(self, force_tournament_rules: bool=True):
        '''
        Lists kings in the DiGraph
        :param force_tournament_rules: if Digraph is a tournament, if set to False will ignore k_val <= 2 rule, if Digraph is not a tournament, this setting does nothing
        '''
        if len(self.D_kings) == 0:
            print('No kings in DiGraph.')
        elif self.is_T and force_tournament_rules:
            t_king_list = list()

            for king in self.D_kings:
                if self.D.nodes[king]['k_val'] <= 2:
                    t_king_list.append(king)

            print(f"Kings in Tournament are: {t_king_list}")
        else:
            print(f"Kings in Digraph are: {self.D_kings}")


class Product_Digraph:
    '''
    Instantiated with two Factor_Digraph objects, will yield a direct product digraph
    '''
    def __init__(self, D1: Digraph, D2: Digraph):
        '''
        :param D1: DiGraph as given by networkx.DiGraph, is first factor digraph
        :param D2: DiGraph as given by networkx.DiGraph, is second factor digraph
        '''
        self.D1: Digraph = D1                                    # factor digraph 1
        self.D2: Digraph = D2                                    # factor digraph 2

        self.D1xD2: Digraph = Digraph(nx.tensor_product(self.D1.D, self.D2.D))

    def get_extremum_k_val_kings(self, extremum_is_max: bool=True):
        '''
        In the product, will find the k_val kings, either min, or max, based on boolean given in arg.
        :param extremum_is_max: if True, extremum is maximal, otherwise minimum.
        '''

        if self.D1xD2.D_kings == []:
            return

        k_val_list = set()

        for node in self.D1xD2.D.nodes:
            if node in self.D1xD2.D_kings:
                k_val = self.D1xD2.D.nodes[node]['k_val']
                k_val_list.add(k_val)


        extremum_k_val = max(k_val_list) if extremum_is_max else min(k_val_list)

        for node in self.D1xD2.D.nodes:
            if node in self.D1xD2.D_kings and self.D1xD2.D.nodes[node]['k_val'] == extremum_k_val:
                comp1 = node[0]
                comp2 = node[1]

                print(f"the vertex {node} in product has {"maximal" if extremum_is_max else "minimal"} k_val {extremum_k_val} in "
                      f"product digraph, and is composed of {comp1} and {comp2}.")

                print(f"vertex {comp1} from D1 has k_val {self.D1.D.nodes[comp1]['k_val']}, and is on closed diwalks of lengt"
                      f"hs (Sv = {self.D1.D.nodes[comp1]['Sv']}), with GCD(Sv) = {self.D1.D.nodes[comp1]['GCD(Sv)']}.")

                print(f"vertex {comp2} from D2 has k_val {self.D2.D.nodes[comp2]['k_val']}, and is on closed diwalks of lengt"
                      f"hs (Sv = {self.D2.D.nodes[comp2]['Sv']}), with GCD(Sv) = {self.D2.D.nodes[comp2]['GCD(Sv)']}.")



        pass
