"""
Functions that will generate digraphs from .txt, and .d6 files.

For a broad overview, please refer to 'projectFiles/DOCUMENTATION.md';
for more detailed information, please read through docstrings, and comments below.
"""

# library imports
import networkx as nx
import math as m
import os                   # for file path identification
import linecache            # for loading ranges of lines into memory cache (optimization)


def mckay_txt_parser(filename: str | os.PathLike, fileline: int) -> nx.DiGraph:
    """
    will generate a tournament from a specific line from a given file of type .txt
    :param filename: name of the file being passed in, required to be .txt format
    :param fileline: specific line we want to use in file; please use non-zero indexed value (i.e. first line is line 1)
    :return: a tournament digraph of type networkX.DiGraph
    """
    digraph_result = nx.DiGraph()

    if not filename.endswith('.txt'):
        raise FileTypeError(filename)

    try:
        with open(filename, 'r') as file:
            spec_line = linecache.getline(filename, fileline, module_globals=None)  # memory optimization (larger files)
            spec_line = spec_line.strip()  # clean up input

            if spec_line == "":
                raise SpecLineError(fileline)

            for char in spec_line:  # checks for unexpected data in line content (we only want 1's and 0's)
                if char not in ('0', '1'):
                    raise FileContentError(char)

            k = len(spec_line)                              # number of chars in line, should be equal to (n choose 2)
            n = ((1 + m.sqrt((1 + 8 * k))) / 2)             # solve for order of digraph

            if float(int(n)) == n:                          # if resulting n is an int, then file is valid length

                '''
                the bit string that is on the specified line number is the top-right triangle of an adjacency matrix
                the reason only half of the adjacency matrix is needed- is due to the structure of tournaments

                the matrix on an order 4 tournament may look like the following (vertices A, B, C, D):

                    A  B  C  D
                A   x  1  1  0
                B   x  x  0  1
                C   x  x  x  0
                D   x  x  x  x

                note for above:
                    - each 'x' denotes it is not present in the file line, the matrix in this case would be: "110010"
                    - '1' denotes a forward-adjacency, i.e. u is adjacent to v (u => v)
                    - '0' denotes a backward-adjacency, i.e. u is adjacent from v (u <= v)
                '''

                n = int(n)
                t_edge_list = []
                cc = 0                                      # character counter
                for u in range(1, n):                       # vertices {u,(u+1),...,(n-1)}
                    for v in range((u+1), (n+1)):           # vertices {(u+1),(u+2),...,n}
                        char = spec_line[cc]
                        cc += 1

                        if char == '1':
                            t_edge_list.append([u, v])  # implies that u is adjacent to v
                        else:
                            t_edge_list.append([v, u])  # implies that u is adjacent from v

                digraph_result.add_edges_from(t_edge_list)

                if digraph_result.number_of_nodes() == 0:
                    raise NullDiGraphError()

            else:
                raise FileLengthError(k)

    except FileNotFoundError:
        print(f"File '{filename}' not found, or couldn't be opened.")
    except FileContentError as FCE:
        print(f"File '{filename}' invalid content: found illegal char \''{FCE.wrong_content}'\', "
              f"was expecting only '0' or '1'.")
    except FileLengthError as FLE:
        print(f"File '{filename}' invalid number of chars: '{FLE.wrong_length}' will not result in a tournament.")
    except SpecLineError as SLE:
        print(f"Specified line: '{SLE.spec_line_val}', caused empty string to be produced, possibly out of bounds.")
    except FileTypeError as FTE:
        print(f"File '{FTE.wrong_filetype}' provided is of wrong filetype, expected '.txt' file extension.")
    except NullDiGraphError as NDE:
        print(f"Specified file {filename}, and line {fileline}, produced a null digraph, please check parameters.")

    return digraph_result


def mckay_d6_parser(filename: str | os.PathLike, fileline: int) -> nx.DiGraph:
    """
    will generate a digraph from a specific line from a given file of type .d6
    :param filename: name of the file being passed in, required to be .d6 format
    :param fileline: specific line we want to use in file; please use non-zero indexed value (i.e. first line is line 1)
    :return: a digraph of type networkX.DiGraph
    """
    # side-note: if you're interested in the details of how .d6 files are encoded, and their formal definition,
    # please refer to the following: https://users.cecs.anu.edu.au/~bdm/data/formats.txt

    digraph_result = nx.DiGraph()

    if not filename.endswith('.d6'):
        raise FileTypeError(filename)

    try:
        with open(filename, 'r') as file:
            spec_line = linecache.getline(filename, fileline, module_globals=None)  # memory optimization (larger files)
            spec_line = spec_line.strip()   # clean up input

            if spec_line == "":
                raise SpecLineError(fileline)

            if spec_line[0] != '&':  # .d6 file lines start with '&' as a delimiting char
                raise StartCharError(spec_line[0])

            for char in spec_line[1:]:  # all chars in a .d6 file should be printable ASCII chars in a specific range
                if not (63 <= ord(char) <= 125):
                    raise FileContentError(char)

            # calculate the order of the digraph (e.g. if '@': ord('@') = 64; 64 - 63 = 1, order of digraph would be 1)
            n = ord(spec_line[1]) - 63

            digraph_result.add_nodes_from(range(0, n))  # digraphs may have isolated vertices, add the vertices manually

            matrix_length = pow(n, 2)  # the adjacency matrix houses the adjacencies between vertices, as such, is: n^2

            resulting_bit_array = ''  # will house the concatenated bit arrays of each char as processed below

            for char in spec_line[2:]:  # process the remaining chars of the string
                '''
                the char values have an integer value, which, on subtracting 63, and converting to binary
                will result in part of the adjacency matrix
                if the length of the binary part is shorter than 6, then it needs zeroes appended to the
                left-hand side, this is to comply with the encoding/decoding scheme; the compliant 6-length binary part 
                is then appended to the end of the total resulting bit array (by big-endian rules)
                '''
                bit_string = '{:b}'.format((ord(char) - 63))

                if len(bit_string) < 6:
                    bit_string = ('0' * (6 - len(bit_string))) + bit_string

                resulting_bit_array += bit_string

            '''
                only part of the resulting bit array has the adjacencies we need, specifically-- 
                the first 0 to matrix-length 1's and 0's, the rest are just garbage that are a side-product of the 
                original encoding process
                
                the matrix on an order 4 digraph may look like the following (vertices A, B, C, D):
                [the matrix length would then be equal to 16, as 4^2 = 16]
                
                    A  B  C  D
                A   0  1  1  0
                B   1  1  0  1
                C   0  0  0  0
                D   1  1  1  1
                
                [each '1' implies a forward adjacency from the left vertex to the top vertex, '0' means nothing]
            '''
            resulting_matrix = resulting_bit_array[0:matrix_length]

            # we now need to build the adjacency list for the digraph from the resulting matrix...

            d_edge_list = []
            u = 0  # corresponds to left-hand side vertices of the matrix
            v = 0  # corresponds to top side vertices of the matrix

            for char in resulting_matrix:

                if char == '1':
                    d_edge_list.append([u, v])  # implies u is adjacent to v

                v += 1

                if v == n:  # move to the next row of the matrix
                    v = 0
                    u += 1

            digraph_result.add_edges_from(d_edge_list)

            if digraph_result.number_of_nodes() == 0:  # null graph check (will probably never happen)
                raise NullDiGraphError()

    except FileNotFoundError:
        print(f"File '{filename}' not found, or couldn't be opened.")
    except FileContentError as FCE:
        print(f"File '{filename}' invalid content: found illegal char \''{FCE.wrong_content}'\', "
              f"char needs to be printable ASCII character.")
    except SpecLineError as SLE:
        print(f"Specified line: '{SLE.spec_line_val}', caused empty string to be produced, possibly out of bounds.")
    except StartCharError as SCE:
        print(f"Start of line has illegal char: '{SCE.wrong_char}', expected '&'.")
    except FileTypeError as FTE:
        print(f"File '{FTE.wrong_filetype}' provided is of wrong filetype, expected '.d6' extension.")
    except NullDiGraphError as NDE:
        print(f"Specified file {filename}, and line {fileline}, produced a null digraph, please check parameters.")

    return digraph_result


class FileLengthError(Exception):
    def __init__(self, found_length):
        self.wrong_length = found_length

    def __str__(self):
        return repr(self.wrong_length)


class FileContentError(Exception):
    def __init__(self, found_content):
        self.wrong_content = found_content

    def __str__(self):
        return repr(self.wrong_content)


class SpecLineError(Exception):
    def __init__(self, slv):
        self.spec_line_val = slv

    def __str__(self):
        return repr(self.spec_line_val)


class StartCharError(Exception):
    def __init__(self, found_char):
        self.wrong_char = found_char

    def __str__(self):
        return repr(self.wrong_char)


class FileTypeError(Exception):
    def __init__(self, found_filetype):
        self.wrong_filetype = found_filetype

    def __str__(self):
        return repr(self.wrong_filetype)


class NullDiGraphError(Exception):
    def __init__(self):
        pass
