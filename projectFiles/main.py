import networkx as nx
import math
import functools
import threading

from networkx_viewer import Viewer
from DKS_tools.Analysis import DKS_Digraph, DKS_Product_Digraph
from DKS_tools.Experiment_Functions import min_max_k_val_kings_experiment

if __name__ == '__main__':

    # edit these lines to configure experiment
    specified_order_t = 3
    specified_line_t = 2
    max_order_t = 5

    # below is a sample line, it will take the specified-line tournament from the "tourn<specified_order_t>.txt" file
    # contained within the directory "ProjectFiles\digraph_datasets\t_files\" and take its direct product with all other
    # tournaments up to 'max_order_t' and will output a results file in the "ProjectFiles\experiment results" directory,
    # depending on its value, it may take quite some time (if max_order_t == 10, it may take 20+ minutes)

    min_max_k_val_kings_experiment(specified_order_t, specified_line_t, max_order_t)

