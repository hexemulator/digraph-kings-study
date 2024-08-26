import networkx as nx
import math
import functools
import threading

from networkx_viewer import Viewer
import DKS_tools.Util as util
from DKS_tools.Analysis import DKS_Digraph, DKS_Product_Digraph
from Experiment_Functions import min_max_k_val_kings_experiment

if __name__ == '__main__':
    T1 = DKS_Digraph(util.mckay_txt_parser(f"digraph_datasets/t_files/tourn5.txt", 3),f"T1")
    T2 = DKS_Digraph(util.mckay_txt_parser(f"digraph_datasets/t_files/tourn5.txt", 2),f"T2")

    T1xT2 = DKS_Product_Digraph(T1, T2)


