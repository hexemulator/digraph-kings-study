import networkx as nx
import math
import functools
from networkx_viewer import Viewer
import DKS_tools.Util as util
from DKS_tools.Analysis import Digraph, Product_Digraph

"""T1 = Digraph(util.mackay_t_parser(f"t_files/tourn6.txt", 16),f"G",True)"""

# is the length of all closed diwalks containing a specific vertex divisible by the GCD of all lengths of simple_cycles
# that also contain that vertex?
G = nx.DiGraph()
G.add_edges_from([[1,2],[2,3],[3,1],[2,4],[4,6],[6,5],[5,2]])



T1 = Digraph(G,"G")
T2 = Digraph(G,"G")
print(f"\nEdges of G: {T1.D.edges}\n")

'''
Below is code for finding the lengths of all closed diwalks containing a king vertex
'''
for king in T1.D_kings:
    T1.D.nodes[king]['Sv'] = set()

kings_to_check = T1.D_kings.copy()

for proposed_walk_length in range(1,T1.D.size()+1):
    # if there's no more kings to check lengths for, then stop the iteration
    if len(kings_to_check) == 0:
        break
    # find all walks in the digraph of that particular length
    all_walks_of_len = nx.number_of_walks(T1.D, proposed_walk_length)

    print(f"proposed walk len = {proposed_walk_length}")

    for king in kings_to_check:

        print(f"\tchecking against king vertex {king}")
        num_king_closed_diwalks = all_walks_of_len[king][king]       # closed diwalks from king to itself of length

        # if any king-to-self closed diwalks are found
        if num_king_closed_diwalks > 0:
            # if there exists king-to-self closed diwalks
            if len(T1.D.nodes[king]['Sv']) > 0:
                length_is_multiple = False
                for existing_length in T1.D.nodes[king]['Sv']:
                    if proposed_walk_length % existing_length == 0:
                        length_is_multiple = True

                if not length_is_multiple:
                    print(f"\t\tadding length to Sv")
                    T1.D.nodes[king]['Sv'].add(proposed_walk_length)
            else:
                print(f"\t\tadding length to empty Sv")
                T1.D.nodes[king]['Sv'].add(proposed_walk_length)

    kings_to_be_removed = list()

    for king in kings_to_check:
        print(f"\nchecking GCD for vertex {king}")
        if len(T1.D.nodes[king]['Sv']) >= 2:
            current_GCD_of_Sv = functools.reduce(math.gcd, T1.D.nodes[king]['Sv'])

            if current_GCD_of_Sv == 1:
                print(f"\tking {king} flagged for removal")
                kings_to_be_removed.append(king)

    if len(kings_to_be_removed) != 0:
        for king in kings_to_be_removed:
            kings_to_check.remove(king)

for king in T1.D_kings:
    print(f"Basis Sv of king {king}, is: {T1.D.nodes[king]['Sv']}")
