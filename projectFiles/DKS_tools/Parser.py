'''
Provides functionality to load, read, and generate tournaments from .di6 files
'''

class FileLengthError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return(repr(self.value))

class FileContentError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return(repr(self.value))

class SpecLineError(Exception):
    def __init__(self, slv):
        self.spec_line_val = slv

    def __str__(self):
        return(repr(self.value))

# LIBRARY IMPORTS
import networkx as nx       # networkx module
import math as m            # math module
import os
import linecache



def t_di6_parser(filename: str | os.PathLike, fileline: int) -> nx.DiGraph:
    """
    t_di6_parser will generate a tournament when given a filename as an argument
    :param filename: name of the file being passed in
    :param fileline: specific line we want to use in file; please use non-zero indexed value
    :return: a tournament digraph
    """
    T = nx.DiGraph()

    try:
        with open(filename, 'r') as file:
            # using linecache instead of regular .getline, line count gets crazy at 10 vertex tournaments
            spec_line= linecache.getline(filename, fileline, module_globals=None)
            spec_line = spec_line.strip()   # remove possible whitespace at beginning and end of string

            if spec_line == "":
                raise SpecLineError(fileline)

            for char in spec_line:
                if char not in ('0','1'):                       # file should ONLY be composed of zeroes and ones
                    raise FileContentError(char)

            k = len(spec_line)                                  # number of chars in file, equal to (n choose 2)
            n = ((1 + m.sqrt((1 + 8 * k))) / 2)                 # solve for number of vertices, given k

            if (float(int(n)) == n):                            # if n is an int, then file is valid length
                n = int(n); t_edge_list = []                    # convert n to int, setup edge list for tournament
                cc = 0                                          # character counter
                for u in range(1,n):                            # vertices {u,(u+1),...,(n-1)}
                    for v in range((u+1),(n+1)):                # vertices {(u+1),(u+2),...,n}
                        char = spec_line[cc]
                        cc += 1                                 # increment character counter

                        # assign adjacency based on char value
                        if char == '1':
                            t_edge_list.append([u,v])
                        else:
                            t_edge_list.append([v,u])


                # fill tournament with created edges
                T.add_edges_from(t_edge_list)

            else:
                raise FileLengthError(k)

    except FileNotFoundError:
        print(f"File '{filename}' not found, or couldn't be opened.")
    except FileContentError as FCE:
        print(f"File '{filename}' invalid content: found illegal char \''{FCE.value}'\', was expecting only '0' or '1'.")
    except FileLengthError as FLE:
        print(f"File '{filename}' invalid number of chars: '{FLE.value}' will not result in a tournament.")
    except SpecLineError as SLE:
        print(f"Specified line: '{SLE.spec_line_val}', caused empty string to be produced, possibly out of bounds.")

    if not (nx.is_tournament(T)) or (T.number_of_nodes() == 0):  # final check to make sure everything worked
        print(f"ERROR: T is not a tournament, unexpected behaviour may occur.")

    return T