"""
Classes that represent digraphs, and products of digraphs-- each class has functionalities tied to their identity,
as well as functionalities that are pertinent to the study itself.

For a broad overview, please refer to 'projectFiles/DOCUMENTATION.md';
for more detailed information, please read through docstrings, and comments below.
"""
# library imports
import networkx as nx
import math as m
import functools as ft


class DKS_Digraph:
    def __init__(self, digraph: nx.DiGraph, name: str):
        """
        :param digraph: DiGraph object, from networkx.DiGraph
        :param name: user-given name of digraph (for best results, use fstrings)
        """
        self.digraph: nx.DiGraph = digraph
        self.name: str = name
        self.is_valid_digraph: bool = self.digraph.order() != 0   # order 0 digraphs are considered valid in networkX

        self.digraph_kings: list = []  # list of 'kings' (if they exist) in the digraph
        self.max_k_val = 0  # maximum distance a king needs to travel in a digraph to reach all other nodes
        self.min_k_val = 0  # minimum distance a king needs to travel in a digraph to reach all other nodes
        self.set_k_vals()  # populates the attributes 'digraph_kings', 'max_k_val', and 'min_k_val'

        self.is_T: bool = nx.is_tournament(self.digraph) and self.is_valid_digraph  # whether digraph is tournament
        self.has_emperor = len(self.digraph_kings) == 1  # if the tournament has an emperor

    def set_k_vals(self):
        """
        k values are to do with k-kings, method will:
            - identify kings (will populate self.digraph_kings)
            - find kings' k value (will assign value to self.digraph[king]['k_val'])
            - identify min/max k value (will assign value to self.min_k_val/self.max_k_val)
        """

        king_list = list()
        k_val_list = list()

        for vertex in self.digraph.nodes:
            try:
                k_val = nx.eccentricity(self.digraph, vertex)  # eccentricity is min distance to reach all nodes
                self.digraph.nodes[vertex]['k_val'] = k_val  # stored directly in a dict key associated with vertex
                k_val_list.append(k_val)
                king_list.append(vertex)
            except:
                pass  # silent errors, don't need to know about vertices that aren't kings

        if len(k_val_list) != 0:  # as long as there's at LEAST one king, we can find the min/max k-val
            self.max_k_val = max(k_val_list)
            self.min_k_val = min(k_val_list)

        self.digraph_kings = sorted(king_list)  # sort it so that they are in nice order

    def calc_dvs_cvs(self, find_dv: bool = True, find_cv: bool = True):
        """
        for each king, will find dv and cv depending on what user wants, where:
            - dv is the set of lengths of closed diwalks that contain the king
            - cv is the set of lengths of cycles that contain the king
        the function will then calculate the GCD(dv) or GCD(cv), depending on user's
        prior choices, will assign values directly to self.digraph.nodes[king]['GCD(Dv)' and/or 'GCD(Cv)']
        :param find_dv: if user wants Dv, and GCD(Dv), default is True
        :param find_cv: if user wants Cv, and GCD(Cv), default is True
        """

        """
        calculating the Dv, and Cv are computationally intense, so this function allows for the user to specify which
        values they actually want, to reduce the amount of computation to only what is necessary!
        """

        # if neither cv nor dv is sought, the function does nothing
        if not find_cv and not find_dv:
            return
        else:
            # if cv is sought, we find it first
            if find_cv:
                # initialize kings with Cv attributes in digraph
                for king in self.digraph_kings:
                    self.digraph.nodes[king]['Cv'] = set()  # Cv values do not need to be repeated
                    self.digraph.nodes[king]['GCD(Cv)'] = 0

                    # simple cycles are equivalent to sought cycles, below will return cycles of all lengths
                    all_simple_cycles = nx.simple_cycles(self.digraph)

                    for cycle in all_simple_cycles:
                        if king in cycle:
                            self.digraph.nodes[king]['Cv'].add(len(cycle))

                    # if the king isn't on any cycle, GCD(Cv) will be equal to 0
                    if len(self.digraph.nodes[king]['Cv']) >= 2:
                        self.digraph.nodes[king]['GCD(Cv)'] = ft.reduce(m.gcd, self.digraph.nodes[king]['Cv'])
                    elif len(self.digraph.nodes[king]['Cv']) == 1:
                        self.digraph.nodes[king]['GCD(Cv)'] = list(self.digraph.nodes[king]['Cv'])[0]

            # if dv is sought as well, find them next... otherwise-- the function will exit
            if find_dv:
                # initialize kings with Dv attributes in the digraph
                for king in self.digraph_kings:
                    self.digraph.nodes[king]['Dv'] = set()
                    self.digraph.nodes[king]['GCD(Dv)'] = 0

                # below is a list of kings remaining to be checked for their Dv & GCD(Dv), we create a copy of the original
                # list because it allows us to remove multiple kings at a time, w/o affecting original list
                kings_to_check = self.digraph_kings.copy()

                '''
                check all walk lengths up to the size of the digraph, the reason we choose the size of the digraph as an
                upper-bound is that a closed diwalk of maximal length that is unique (no repetitions of cycles contained
                within the closed diwalk) is the size of the digraph itself. In other words-- if we create a closed diwalk
                of maximum size, it will be composed of the concatenation every edge present in the digraph, every edge 
                summed together is equal to the size of the digraph.
                '''
                for proposed_walk_length in range(1, self.digraph.size() + 1):

                    # if all kings have been found to have GCD(Dv) = 1, loop ends prematurely (saves time, and processing)
                    if len(kings_to_check) == 0:
                        break

                    # collect all walks in the digraph, including closed walks of the proposed length
                    all_walks_of_len = nx.number_of_walks(self.digraph, proposed_walk_length)

                    # for each king remaining, find count of closed diwalks containing king of that length, if they exist
                    for king in kings_to_check:
                        num_king_closed_diwalks = all_walks_of_len[king][king]  # count of walks from king to itself

                        if num_king_closed_diwalks > 0:  # if any such closed diwalks are found...
                            if len(self.digraph.nodes[king]['Dv']) == 0:  # if king doesn't have element in Dv yet--
                                self.digraph.nodes[king]['Dv'].add(proposed_walk_length)
                            else:  # otherwise, king has at least one length in its set
                                # need to check if proposed length is multiple of an existing length, (possible repetition)
                                plength_is_mult_of_elength = False
                                for existing_length in self.digraph.nodes[king]['Dv']:
                                    if proposed_walk_length % existing_length == 0:
                                        plength_is_mult_of_elength = True

                                if not plength_is_mult_of_elength:
                                    self.digraph.nodes[king]['Dv'].add(proposed_walk_length)

                    kings_to_be_removed = list()  # reset list each time, and populate based on kings that have GCD(Dv) = 1

                    for king in kings_to_check:
                        if len(self.digraph.nodes[king]['Dv']) >= 2:  # need at least two values in Dv to check for GCD
                            current_gcd_of_dv = ft.reduce(m.gcd, self.digraph.nodes[king]['Dv'])

                            if current_gcd_of_dv == 1:
                                kings_to_be_removed.append(king)
                                self.digraph.nodes[king]['GCD(Dv)'] = current_gcd_of_dv

                    # need to do it this way, otherwise index on removals change, making multiple removals impossible
                    if len(kings_to_be_removed) != 0:
                        for king in kings_to_be_removed:
                            kings_to_check.remove(king)

                # deal with cases of Dv not dealt with above, either GCD(Dv) not calc'ed yet, or only has a single Dv value
                for king in self.digraph_kings:
                    if len(self.digraph.nodes[king]['Dv']) >= 2 and self.digraph.nodes[king]['GCD(Dv)'] == 0:
                        self.digraph.nodes[king]['GCD(Dv)'] = ft.reduce(m.gcd, self.digraph.nodes[king]['Dv'])
                    elif len(self.digraph.nodes[king]['Dv']) == 1 and self.digraph.nodes[king]['GCD(Dv)'] == 0:
                        self.digraph.nodes[king]['GCD(Dv)'] = list(self.digraph.nodes[king]['Dv'])[0]

    def get_king_list(self, force_tournament_rules: bool = False) -> list:
        """
        Returns the list of kings in the digraph, depending on what the user wants.
        :param force_tournament_rules: if DKS_Digraph is a tournament, if set to False will ignore k_val <= 2 rule,
        :returns: list consisting of kings, is only a flat list with no characteristics
        """
        if len(self.digraph_kings) == 0:
            return []  # returns empty list
        elif self.is_T and force_tournament_rules:
            t_king_list = list()  # need to create a compliant list of tournament kings

            for king in self.digraph_kings:
                if self.digraph.nodes[king]['k_val'] <= 2:
                    t_king_list.append(king)

            return sorted(t_king_list)
        else:
            return self.digraph_kings

    def get_digraph_characteristics(self, force_tournament_rules: bool = False):
        """
        lists characteristics of the digraph: order, size, min/max k_val, etc.
        :param force_tournament_rules: force listed characteristics to abide by tournament rules, if digraph is not a
        tournament, it should have no effect if unchanged
        """

        digraph_characteristics = [f"{"tournament" if self.is_T and force_tournament_rules else "digraph"} "
                                   f"name: {self.name}",
                                   f"order: {self.digraph.order()}",
                                   f"vertices: {self.digraph.nodes()}",
                                   f"size: {self.digraph.size()}"]

        if self.is_T and force_tournament_rules:  # if digraph is a tournament, and user is forcing tournament rules
            digraph_characteristics.append(f"({self.digraph.order()},{len(self.digraph_kings)})-tournament")

            if self.has_emperor:
                digraph_characteristics.append(f"tournament emperor: {self.digraph_kings[0]}")
            else:  # if tournament doesn't have an emperor, it has more than one king
                digraph_characteristics.append(f"tournament kings: {self.get_king_list(force_tournament_rules)}")

        elif len(self.digraph_kings) != 0:
            digraph_characteristics.append(f"digraph kings: {self.get_king_list()}")
            digraph_characteristics.append(f"min_k_val: {self.min_k_val}")
            digraph_characteristics.append(f"max_k_val: {self.max_k_val}")
        else:
            digraph_characteristics.append(f"digraph kings: {[]}")
            digraph_characteristics.append(f"min_k_val: {0}")
            digraph_characteristics.append(f"max_k_val: {0}")

        digraph_characteristics.append(f"strong components: {self.get_digraph_strong_components()}")

        return digraph_characteristics

    def get_king_characteristics(self, force_tournament_rules: bool = False) -> list:
        """
        gathers characteristics of the digraph's king, will return a list of lists, the format of the items of list is:
            [king_vertex_id, king_vertex_k_val, (if it exists) king_vertex_GCD(Dv), (if it exists) king_vertex_GCD(Cv)
        :param force_tournament_rules: if set to True, will only deal with kings with a k_val of 2 or 1.
        :returns: list of lists, each housing the characteristics of kings as specified above
        """

        king_char_list = list()

        for node in self.digraph_kings:
            if force_tournament_rules and self.digraph.nodes[node]['k_val'] > 2:
                continue
            else:
                append_item = [f"vertex: {node}", f"k_val: {self.digraph.nodes[node]['k_val']}"]

                if 'GCD(Dv)' in self.digraph.nodes[node]:
                    append_item.append(f"Dv: {self.digraph.nodes[node]['Dv']}")
                    append_item.append(f"GCD(Dv): {self.digraph.nodes[node]['GCD(Dv)']}")
                if 'GCD(Cv)' in self.digraph.nodes[node]:
                    append_item.append(f"Cv: {self.digraph.nodes[node]['Cv']}")
                    append_item.append(f"GCD(Cv): {self.digraph.nodes[node]['GCD(Cv)']}")

                king_char_list.append(append_item)

        return king_char_list

    def get_digraph_strong_components(self, exclude_isolated_vertices: bool = False) -> list:
        """
        gathers strong components of digraph and returns as a list
        :param exclude_isolated_vertices: if set to True will exclude isolated vertices from list
        :returns: strong components of digraph in a list
        """
        strong_components = nx.strongly_connected_components(self.digraph)
        sorted_strong_components = sorted(strong_components, key=len, reverse=True)
        strong_component_return = list()

        if len(sorted_strong_components) == 1:
            strong_component_return = self.digraph.nodes()
        else:
            for strong_component in sorted_strong_components:
                if exclude_isolated_vertices:
                    if len(strong_component) == 1:
                        continue
                else:
                    strong_component_return.append(strong_component)

        return strong_component_return


class DKS_Product_Digraph:
    """
    Instantiated with two DKS_Digraph objects, will yield a direct product digraph
    """
    def __init__(self, digraph1: DKS_Digraph, digraph2: DKS_Digraph):
        """
        :param digraph1: DiGraph as given by networkx.DiGraph, is first factor digraph
        :param digraph2: DiGraph as given by networkx.DiGraph, is second factor digraph
        """
        self.D1: DKS_Digraph = digraph1                                    # factor digraph 1
        self.D2: DKS_Digraph = digraph2                                    # factor digraph 2

        # ^ may at some point have it that if the digraphs are given as a nx.DiGraph object that it will create them to fit

        self.D1xD2: DKS_Digraph = DKS_Digraph(nx.tensor_product(self.D1.digraph, self.D2.digraph), f"{self.D1.name}x{self.D2.name}")

    def get_product_extremum_k_val_kings(self, extremum_is_max: bool = True):
        """
        In the product, will find the k_val kings, either min, or max, based on boolean given in arg.
        :param extremum_is_max: if True, extremum is maximal, otherwise minimum.
        """

        print(f"~~~~~~{"MAX" if extremum_is_max else "MIN"} EXTRENUM K_VAL KINGS IN {self.D1xD2.name}~~~~~~")
        if len(self.D1xD2.digraph_kings) == 0:
            print(f"get_product_extrenum_k_val_kings(): {self.D1xD2.name} has no kings, unable to retrieve extrenum k_val kings.")
            print(f"~~~~~~~~~~~~~~~~~~~~~~~~\n")
            return

        extremum_k_val = self.D1xD2.max_k_val if extremum_is_max else self.D1xD2.min_k_val

        print(f"\nget_product_extrenum_k_val_kings(): the following are the {"maximal" if extremum_is_max else "minimal"} k_vals of king vertices in {self.D1xD2.name}...\n")

        for node in self.D1xD2.digraph.nodes:
            if node in self.D1xD2.digraph_kings and self.D1xD2.digraph.nodes[node]['k_val'] == extremum_k_val:
                comp1 = node[0]
                comp2 = node[1]

                print(f"vertex {node} in {self.D1xD2.name} has {"maximal" if extremum_is_max else "minimal"} k_val {extremum_k_val} in "
                      f"{self.D1xD2.name}, and is composed of vertex {comp1} of {self.D1.name}, and vertex {comp2} of {self.D2.name}:")

                print(f"\t>> vertex {comp1} from {self.D1.name} has k_val {self.D1.digraph.nodes[comp1]['k_val']}, and is on closed diwalks of lengt"
                      f"hs (Dv = {self.D1.digraph.nodes[comp1]['Dv']}), with GCD(Dv) = {self.D1.digraph.nodes[comp1]['GCD(Dv)']}.")

                print(f"\t>> vertex {comp2} from {self.D2.name} has k_val {self.D2.digraph.nodes[comp2]['k_val']}, and is on closed diwalks of lengt"
                      f"hs (Dv = {self.D2.digraph.nodes[comp2]['Dv']}), with GCD(Dv) = {self.D2.digraph.nodes[comp2]['GCD(Dv)']}.\n")

        print(f"~~~~~~~~~~~~~~~~~~~~~~~~\n")

    def max_k_below_upper_bound(self) -> bool:
        """
        Function checks whether or not the max_k_val is below or equal to the theoretical upper bound as given by
        M. Norge in her paper talking about the direct product of two digraphs... essentially this is a test to see
        if a given product is 'interesting enough' to run tests on. Later on, I would imagine this may not be necessary
        """

        print(f"~~~~~~CHECKING IF {self.D1xD2.name} IS BELOW THEORIZED UPPER-BOUND~~~~~~")
        upper_bound_val = (self.D1.digraph.order() * self.D2.digraph.order()) - 1
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
