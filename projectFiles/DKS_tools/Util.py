'''
Provides functionality to load, read, and generate tournaments from .di6 files
'''

# LIBRARY IMPORTS
import networkx as nx       # networkx module
import math as m            # math module
import os
import linecache


def mackay_t_parser(filename: str | os.PathLike, fileline: int) -> nx.DiGraph:
    """
    will generate a tournament from a specific line from a given filename
    :param filename: name of the file being passed in, needs to be .txt format
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


'''
Description of digraph6 format.
------------------------------

Data type:  
   simple directed graphs (allowing loops) of order 0 to 68719476735.

Optional Header: 
   >>digraph6<<     (without end of line!)

File name extension:
   .d6

One graph:
   Suppose G has n vertices. Write the adjacency matrix of G
   as a bit vector x of length n^2, row by row.

   Then the graph is represented as '&' N(n) R(x).
   The character '&' (decimal 38) appears as the first character.

Example:
   Suppose n=5 and G has edges 0->2, 0->4, 3->1 and 3->4.

   x =  00101 
        00000 
        00000 
        01001 
        00000
    
   Then N(n) = 68 and
   R(x) = R(00101 00000 00000 01001 00000) = 73  63  65  79  63.
   So, the graph is  38 68 73  63  65  79  63.
  
  Explanation of R(x) 
  
  General principles:

  All numbers in this description are in decimal unless obviously 
  in binary.

  Apart from the header, there is one object per line. Apart from
  the header, end-of-line characters, and the characters ":", ";"
  and "&" which might start a line, all bytes have a value in the
  range 63-126 (which are all printable ASCII characters). A file of
  objects is a text file, so whatever end-of-line convention is
  locally used is fine; however the C library input routines must
  show the standard single-LF end of line to programs).

Bit vectors:

  A bit vector x of length k can be represented as follows.  
      Example:  1000101100011100

  (1) Pad on the right with 0 to make the length a multiple of 6.
      Example:  100010110001110000

  (2) Split into groups of 6 bits each.
      Example:  100010 110001 110000

  (3) Add 63 to each group, considering them as bigendian binary numbers.
      Example:  97 112 111

  These values are then stored one per byte.  
  So, the number of bytes is ceiling(k/6).

  Let R(x) denote this representation of x as a string of bytes.
      
Small nonnegative integers:
 
  Let n be an integer in the range 0-68719476735 (2^36-1).

  If 0 <= n <= 62, define N(n) to be the single byte n+63.
  If 63 <= n <= 258047, define N(n) to be the four bytes
      126 R(x), where x is the bigendian 18-bit binary form of n.
  If 258048 <= n <= 68719476735, define N(n) to be the eight bytes
      126 126 R(x), where x is the bigendian 36-bit binary form of n.

  Examples:  N(30) = 93
             N(12345) = N(000011 000000 111001) = 126 66 63 120
             N(460175067) = N(000000 011011 011011 011011 011011 011011)
                          = 126 126 63 90 90 90 90 90
'''
# takes inspiration from above descriptor...
def mackay_d6_parser():
    pass

'''
Error Reporting, specific to this file
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