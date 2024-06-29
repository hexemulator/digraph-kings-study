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
    def __init__(self, D: nx.DiGraph, name: str, interpret_as_tournament:bool=False):
        '''
        :param D: DiGraph as given by networkx.DiGraph
        :param interpret_as_tournament: whether the DiGraph should be interpreted as a tournament, default is False
        '''
        # general attributes
        self.D: nx.DiGraph = D
        self.name: str = name
        self.is_valid_digraph: bool = self.D.order() != 0

        # attributes specific to kings
        self.D_kings: list = []
        self.max_k_val = 0; self.min_k_val = 0  # min/max start at 0 until reassigned
        self.set_king_vals()


        if self.D_kings != []:
            self.set_Sv()

        # attributes specific to tournaments
        self.is_T: bool = nx.is_tournament(self.D) and self.is_valid_digraph
        self.interpret_as_T = interpret_as_tournament
        self.has_emperor = True if (len(self.D_kings) and self.interpret_as_T) == 1 else False

    def set_king_vals(self):
        '''
        does a number of things to do with king vertices
        - finds vertices that are kings
        - assigns a k_val to king vertices
        - identifies the min/max k_vals in the digraph
        - assigns the flat identifier list of kings to class attribute 'self.D_kings'
        '''

        king_list = list()
        k_val_list = []

        # for each node in the digraph, attempt to get eccentricity
        for node in self.D.nodes:
            try:
                k_val = nx.eccentricity(self.D, node)
                self.D.nodes[node]['k_val'] = k_val                       # if successful, store K-value in node itself
                k_val_list.append(k_val)
                king_list.append(node)

            except:
                pass

        if len(k_val_list) != 0:
            self.max_k_val = max(k_val_list)
            self.min_k_val = min(k_val_list)

        self.D_kings = sorted(king_list)

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
        all_simple_cycles = nx.simple_cycles(self.D)

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

    def get_king_list(self, force_tournament_rules: bool=False) -> list:
        '''
        Lists kings in the DiGraph
        :param force_tournament_rules: if Digraph is a tournament, if set to False will ignore k_val <= 2 rule, if Digraph is not a tournament, this setting does nothing
        :return: list comprising of kings, is only a flat list with no characteristics
        '''
        if len(self.D_kings) == 0:
            print(f"{self.name} has no kings, nothing to list.")
        elif self.interpret_as_T and self.is_T and force_tournament_rules:
            t_king_list = list()

            for king in self.D_kings:
                if self.D.nodes[king]['k_val'] <= 2:
                    t_king_list.append(king)

            return sorted(t_king_list)
        else:
            return self.D_kings

    def list_D_characteristics(self, force_tournament_rules: bool=False):
        '''
        lists characteristics of the digraph: order, size, min/max k_val, etc.
        :param force_tournament_rules: force listed characteristics to abide by tournament rules, if digraph is not a
        tournament, it should have no effect if unchanged
        '''
        print(f"~~~~~~CHARACTERISTICS OF {self.name}~~~~~~")
        print(f"Listing characteristics of {"tournament" if self.interpret_as_T else "digraph"}, {self.name}:")
        print(f"Has order: {self.D.order()}, size: {self.D.size()}.")

        # list kings, if they exist-- if tournament, give (n,k)-tournament spec
        if self.is_T and force_tournament_rules:
            print(f"Is a ({self.D.order()},{len(self.D_kings)}) tournament.")
            if self.has_emperor:
                print(f"Emperor vertex is: {self.D_kings[0]}.")
            else:
                print(f"Kings in tournament, {self.name} are: {self.get_king_list(force_tournament_rules)}.")
        elif len(self.D_kings) != 0:
            print(f"{self.name} has king(s), king vertices are: {self.get_king_list()}")
            print(f"{self.name} has min_k_val: {self.min_k_val}, and max_k_val: {self.max_k_val}")
        else:
            print(f"{self.name} has no kings, thusly, cannot list them, and also no min/max k_val.")
        print(f"~~~~~~~~~~~~~~~~~~~~~~~~\n")
        
        self.list_digraph_strong_components(force_tournament_rules)

    def list_king_characteristics(self, force_tournament_rules: bool=False):
        print(f"~KING CHARACTERISTICS IN {self.name},FORCE-T-RULES={force_tournament_rules}~")
        for node in self.D_kings:
            if force_tournament_rules and self.D.nodes[node]['k_val'] > 2:
                continue
            else:
                print(f"vertex {node} is a {self.D.nodes[node]['k_val']}-king, with Sv = {self.D.nodes[node]['Sv']}, GCD(Sv) = {self.D.nodes[node]['GCD(Sv)']}")
        print(f"~~~~~~~~~~~~~~~~~~~~~~~~\n")

    def list_digraph_strong_components(self, exclude_isolated_vertices: bool=False):
        strong_components = nx.strongly_connected_components(self.D)
        sorted_strong_components = sorted(strong_components, key=len, reverse=True)
        strong_components_count = len(sorted_strong_components)

        print(f"~~~~~~STRONG COMPONENTS LISTINGS IN {self.name}~~~~~~")

        if strong_components_count == 1:
            print(f"{self.name} has singleton strong component, thus the entire digraph is a strong component.")
        else:
            sc_c = 1
            print(f"{self.name} has {strong_components_count} strongly connected components (descendending order, isolated vertices ignored = {exclude_isolated_vertices}):")
            for strong_component in sorted_strong_components:
                if exclude_isolated_vertices:
                    if len(strong_component) == 1:
                        continue
                print(f"\t>> strong component #{sc_c}, has vertices: {sorted(strong_component)}"); sc_c += 1
        print(f"~~~~~~~~~~~~~~~~~~~~~~~~\n")


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

        self.D1xD2: Digraph = Digraph(nx.tensor_product(self.D1.D, self.D2.D),f"{self.D1.name}x{self.D2.name}")

    def get_product_extremum_k_val_kings(self, extremum_is_max: bool=True):
        '''
        In the product, will find the k_val kings, either min, or max, based on boolean given in arg.
        :param extremum_is_max: if True, extremum is maximal, otherwise minimum.
        '''
        print(f"~~~~~~{"MAX" if extremum_is_max else "MIN"} EXTRENUM K_VAL KINGS IN {self.D1xD2.name}~~~~~~")
        if len(self.D1xD2.D_kings) == 0:
            print(f"get_product_extrenum_k_val_kings(): {self.D1xD2.name} has no kings, unable to retrieve extrenum k_val kings.")
            print(f"~~~~~~~~~~~~~~~~~~~~~~~~\n")
            return

        extremum_k_val = self.D1xD2.max_k_val if extremum_is_max else self.D1xD2.min_k_val

        print(f"\nget_product_extrenum_k_val_kings(): the following are the {"maximal" if extremum_is_max else "minimal"} k_vals of king vertices in {self.D1xD2.name}...\n")

        for node in self.D1xD2.D.nodes:
            if node in self.D1xD2.D_kings and self.D1xD2.D.nodes[node]['k_val'] == extremum_k_val:
                comp1 = node[0]
                comp2 = node[1]

                print(f"vertex {node} in {self.D1xD2.name} has {"maximal" if extremum_is_max else "minimal"} k_val {extremum_k_val} in "
                      f"{self.D1xD2.name}, and is composed of vertex {comp1} of {self.D1.name}, and vertex {comp2} of {self.D2.name}:")

                print(f"\t>> vertex {comp1} from {self.D1.name} has k_val {self.D1.D.nodes[comp1]['k_val']}, and is on closed diwalks of lengt"
                      f"hs (Sv = {self.D1.D.nodes[comp1]['Sv']}), with GCD(Sv) = {self.D1.D.nodes[comp1]['GCD(Sv)']}.")

                print(f"\t>> vertex {comp2} from {self.D2.name} has k_val {self.D2.D.nodes[comp2]['k_val']}, and is on closed diwalks of lengt"
                      f"hs (Sv = {self.D2.D.nodes[comp2]['Sv']}), with GCD(Sv) = {self.D2.D.nodes[comp2]['GCD(Sv)']}.\n")

        print(f"~~~~~~~~~~~~~~~~~~~~~~~~\n")

    def below_upper_bound(self) -> bool:
        print(f"~~~~~~CHECKING IF {self.D1xD2.name} IS BELOW THEORIZED UPPER-BOUND~~~~~~")
        upper_bound_val = (self.D1.D.order() * self.D2.D.order()) - 1
        max_k_val = self.D1xD2.max_k_val
        if 0 < max_k_val < upper_bound_val:
            print(f"Maximal k_val of {self.D1xD2.name} is below theorized upper-bound, max_k_val is: {self.D1xD2.max_k_val}; upper_bound_val is: {upper_bound_val}.")
            print(f"~~~~~~~~~~~~~~~~~~~~~~~~\n")
            return True
        elif max_k_val == upper_bound_val:
            print(f"Maximal k_val of {self.D1xD2.name} is equal to theorized upper-bound, max_k_val is: {self.D1xD2.max_k_val} = {upper_bound_val}.")
        else:
            print(f"{self.D1xD2.name} has no kings, is invalid/unqualified for checking against upper-bound.")

        print(f"~~~~~~~~~~~~~~~~~~~~~~~~\n")

        return False

