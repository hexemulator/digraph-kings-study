import networkx as nx
import math
import functools
from networkx_viewer import Viewer
import DKS_tools.Util as util
from DKS_tools.Analysis import Digraph, Product_DiGraph

T1 = Digraph(util.mackay_t_parser("t_files/tourn5.txt", 3),True)
T2 = Digraph(util.mackay_t_parser("t_files/tourn5.txt", 3),True)

print("T1: ")
print(list(T1.D.nodes(data=True)))
T1.list_kings()

print("T2: ")
print(list(T2.D.nodes(data=True)))
T2.list_kings()

T1xT2 = Product_Digraph(T1, T2)


print("T1xT2: ")

print("kings in T1xT2:")
for k_king in T1xT2.D1xD2.D_kings:
    print(f"king vertex {k_king}, characteristics: {T1xT2.D1xD2.D.nodes[k_king]}")

T1xT2.get_extremum_k_val_kings()


