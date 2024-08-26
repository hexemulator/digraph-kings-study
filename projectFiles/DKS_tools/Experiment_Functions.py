"""
    file to house functions that run experiments, currently only has one experiment, but it's a pretty heavy one!
"""

import os  # for file cleanup
from multiprocessing import Process  # multiprocessing (needed for experiments running heavy workloads)
from projectFiles.DKS_tools import Analysis, Util

file_line_count = [3, 5, 13, 57, 457, 6881, 191537, 9733057]  # TODO: move to external file for tidier look...


def mmkvk_gen_result_part(i_tournament: Analysis.DKS_Digraph, spec_j_order, start_line, file_to_write_to):
    """
        *** Specific to min_max_k_val_kings_experiment() function ***

        generates a part of the total resulting experiment file for a given order of a j tournament, is run on
        multiple threads concurrently, less efficient on lower j orders, but on higher orders, it cuts processing time
        down by 1/2... if you have a beefier computer, you may be able to bump the core count up!
        :param i_tournament: the tournament that is crossed with all other j tournaments
        :param spec_j_order: the order of the tournaments that i_tournament is crossed with
        :param start_line: the starting line in the file of the order of j
        :param file_to_write_to: the name of the file that is to be written to for this quarter
        :returns: nothing, but will write a part of the results to the experiments results directory
    """
    with open(file_to_write_to, "w") as w_f:
        formatted_output = ""

        for j in range(start_line, file_line_count[spec_j_order - 3], 4):  # TODO: last value is '<LINE_JUMP>'
            j_tournament_name = f"T{spec_j_order}_{j}"
            j_tournament = Analysis.DKS_Digraph(Util.mckay_txt_parser(f"digraph_datasets/t_files/tourn{spec_j_order}.txt", j),
                                  j_tournament_name)

            if len(j_tournament.digraph_kings) == 0 or j_tournament.has_emperor:
                continue

            i_x_j = Analysis.DKS_Product_Digraph(i_tournament, j_tournament)

            if len(i_x_j.D1xD2.digraph_kings) == 0:
                continue

            formatted_output += f"\t\t{j_tournament_name}:\n"
            formatted_output += f"\t\t\tmin_k_val: {i_x_j.D1xD2.min_k_val}, ["

            # GATHER ALL 'STRONG' KINGS, and place in formatted output
            low_k_val_kings = list()

            for king in i_x_j.D1xD2.digraph_kings:
                if i_x_j.D1xD2.digraph.nodes[king]['k_val'] == i_x_j.D1xD2.min_k_val:
                    low_k_val_kings.append(king)

            for king in low_k_val_kings:
                formatted_output += str(king)

                if king == low_k_val_kings[-1]:
                    formatted_output += "]\n"
                else:
                    formatted_output += ", "

            formatted_output += f"\t\t\tmax_k_val: {i_x_j.D1xD2.max_k_val}, ["

            # GATHER ALL 'WEAK' KINGS, and place in formatted output

            high_k_val_kings = list()

            for king in i_x_j.D1xD2.digraph_kings:
                if i_x_j.D1xD2.digraph.nodes[king]['k_val'] == i_x_j.D1xD2.max_k_val:
                    high_k_val_kings.append(king)

            for king in high_k_val_kings:
                formatted_output += str(king)

                if king == high_k_val_kings[-1]:
                    formatted_output += "]\n\n"
                else:
                    formatted_output += ", "

            # WRITE RESULTS, and clear output

            w_f.write(str(formatted_output))  # write i_x_j results to the quarter-file
            formatted_output = ""  # clear formatted output


def min_max_k_val_kings_experiment(specified_order: int, specified_line: int):
    """
        creates a results text file that lists all possible combinations of a specified tournament, with all others, up to
        order 10, and also gives the lowest, and highest k values of kings from the combinations of the tournaments (as well
        as the kings involved with those k values)

        this is done through parallel processing, as the amount of computation lends itself to such a method
        :param specified_order:  the order of the tournament (corresponds to a specific file in t_files)
        :param specified_line: the specific line from the text file pointed to by specified_order
        :returns: None, but a text file will be created in the experiments results directory
    """
    experiment_complete = False
    write_file = f"experiment results/experiment_results_[T{specified_order}_{specified_line}]]"

    # check if i_tournament will even result in anything before starting--
    i_tournament = Analysis.DKS_Digraph(
        Util.mckay_txt_parser(f"digraph_datasets/t_files/tourn{specified_order}.txt", specified_line),
        f"T{specified_order}_{specified_line}")

    if len(i_tournament.digraph_kings) == 0 or i_tournament.has_emperor or specified_order < 3:
        experiment_complete = True

    with open(f"{write_file}.txt", 'w') as w_f:

        if experiment_complete:  # if the experiment is complete at this point, it means the i_tournament is invalid
            w_f.write(f"Tournament either has no kings, an emperor, or order less than 3, no output--")
            return
        else:  # otherwise we'll write the header line before the experiment starts
            w_f.write(f"T{specified_order}_{specified_line} x\n")

        spec_j_tournament = specified_order  # baseline start for j order

        while not experiment_complete:  # loop until experiment is complete
            # PARALLELIZE COMPUTATIONS PERFORMED

            p_array = list()  # init list to place working processes
            thread_count = 4  # TODO: CAN BE ALTERED, be sure to change '<LINE_JUMP>' (ctrl+f to find) to match value

            for p_cnt in range(0, thread_count):
                start_line = p_cnt + 1
                p_work = Process(target=mmkvk_gen_result_part, args=(i_tournament, spec_j_tournament, start_line, f"{write_file}.part{p_cnt}"))
                p_array.append(p_work)  # add to collection of processes to perform work

            # START PROCESSES
            for process in p_array:
                process.start()

            # WAIT FOR PROCESSES TO BE COMPLETED
            for process in p_array:
                process.join()

            # STITCH TOGETHER PARTS OF RESULT INTO MAIN RESULTS FILE
            for p_cnt in range(0, thread_count):
                # stitch write_file together... (order doesn't matter)
                with open(f"{write_file}.part{p_cnt}", 'r') as r_f:
                    for line in r_f.readlines():
                        w_f.write(line)

            # DIVIDE EACH J TOURNAMENT SECTION
            w_f.write(f"\t--------------------------------------\n")
            spec_j_tournament += 1

            # TERMINATE EXPERIMENT IF AT ORDER '11' (doesn't exist)
            if spec_j_tournament > 10:

                # FILE PART CLEANUP
                for p_cnt in range(0, thread_count):
                    os.remove(f"{write_file}.part{p_cnt}")

                experiment_complete = True  # flag experiment as completed
