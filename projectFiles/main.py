import networkx as nx
import math
import functools
import threading

from networkx_viewer import Viewer
from DKS_tools.Analysis import DKS_Digraph, DKS_Product_Digraph
from DKS_tools.Experiment_Functions import min_max_k_val_kings_experiment

if __name__ == '__main__':

    max_order_t = 5

    # below is a sample line, it will take the second-line tournament from the "tourn3.txt" file contained within the
    # directory "ProjectFiles\digraph_datasets\t_files\" and take its direct product with all other tournaments up to
    # order 10, it will take some time, and will output a results file in the "ProjectFiles\experiment results" directory

    # Note to user: due to the amount of results, it will initially be split into several "parts"... it will compile all
    # these result 'parts' into a singular txt document given enough time; these parts result from the parallelization
    # of completing the task

    # the below experiment will result in an approx. 4GB txt file, and took a moderately powered machine about 20 mins
    # to run to completion... you've been warned!

    min_max_k_val_kings_experiment(3,2, max_order_t)

    pass  # keep this here
