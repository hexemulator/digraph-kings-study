import networkx as nx
import math
import functools
from networkx_viewer import Viewer
import DKS_tools.Util as util
from DKS_tools.Analysis import DKS_Digraph, DKS_Product_Digraph

D1 = DKS_Digraph(util.mckay_d6_parser(f"digraph_datasets/d6_la_files/digl4.d6", 2080), f"test")
D1.calc_dvs_cvs()

d_char = D1.get_digraph_characteristics()

for item in d_char:
    print(item)

d_king_char = D1.get_king_characteristics()

for char in d_king_char:
    print(char)