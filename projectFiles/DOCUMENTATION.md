# DKS Extension Documentation
The following is the instruction manual for this extension of the networkX library, whose purpose is to facilitate the 
study of kings in direct products of directed graphs, this extension was written over the course of Summer '24, and as 
such is given as-is, and is not advertised as feature complete. Much of the development behind this extension was driven
by need, and exploration at the time of its writing.

___

## DKS_tools
This is the module that houses all the functionality that this library extension has on offer, this module may be expanded
upon, and optimized should the user choose to alter the code base. The module is made up of three files, 
`Analysis.py`, `Util.py`, and `Experiment_Functions.py` the purposes of which are outlined below. It should be noted, for future users of the 
library, that further refactoring is likely required to properly segment the code as per software engineering standards.

---

## Analysis.py
Provides tools for the analysis of directed graphs, as of writing, it consists of two classes: `DKS_Digraph`, and `DKS_Product_Digraph`.

### DKS_Digraph

On being given the following parameters, will create an object of this class-type:

- `networkX.digraph`: **required**
- `name`: **required**

The DKS_Digraph class differs from the networkX.digraph in that it **considers null digraphs (those with order zero) to be
invalid**, this differs from the purposes of the study. The class also has functionalities specific to the study such as identifying king vertices, as well as finding closed
diwalks which contain these kings. These characteristics are pertinent to current literature/articles on the topic.

The following attributes are part of the DKS_Digraph object on instantiation:

- `self.digraph`: the networkX.DiGraph object, this is not only for access for the class methods, but also to not shut off 
access from the user
- `self.name`: the string identifier for the DKS_Digraph object, useful when processing large swaths of data and identifying
specific instances of interest
- `self.is_valid_digraph`: checks the order of the digraph, if zero, it is set to false
- `self.digraph_kings`: list of identified king vertices in the digraph, it should be noted that this includes **all kings**.
Should the user want to work with _tournament-specific_ kings (kings that can reach all other vertices in distance two or less)
then they may need to alter the code base to suit their needs.
- `self.max_k_val`: given all kings, the max_k_val is the maximum distance needed to travel to reach all vertices
- `self.min_k_val`: given all kings, the min_k_val is the minimum distance needed to travel to reach all vertices
- `self.is_T`: identifies whether a given digraph is a tournament, utilizes a combination of networkX.is_tournament(),
and checking the self.is_valid_digraph attribute of the object. (This is because networkX.is_tournament() considers null
digraphs to be tournaments...)
- `self.has_emperor`: will be set to true if the digraph is a tournament, and the tournament has only one king, constituting
the emperor vertex.

The following methods are part of the DKS_Digraph object, it should be noted that these are brief summaries, if further
information is required, the user should pop into the codebase to look over the extensive commenting provided:
- `set_k_vals()`: the function identifies king vertices and sets self.digraph_kings, finds k values of kings (the farthest distance 
the king needs to travel to reach each vertex in the digraph) and assigns the k-val to the specific node in self.digraph, 
and assigns self.min_k_val & self.max_k_val, with the largest and smallest values in the range of k values of king vertices.
- `calc_dvs_cvs()`: first, Dvs is shorthand for _'closed diwalks that contain a vertex v'_, and Cvs is shorthand for 
_'dicycles that contain a vertex v'_, both are very important properties for the purposes of the study, and further are 
**extremely resource-intensive to calculate**. Depending on what the user seeks, this function identifies, given the 
list of digraph kings, the lengths of the Dvs, and Cvs, where 'v' are each of the king vertices, these sets of lengths are assigned 
directly to the node in self.digraph. It should be noted that digraphs of considerable size (that is, the total number 
of arcs present in the digraph) will likely require more time to process.
- `get_king_list()`: returns a list of the kings of the digraph; the function allows for 'force_tournament_rules', which 
will return a list of _tournament-specific_ kings (kings that can reach all other vertices in distance two or less).
- `get_digraph_characteristics()`: will return a list of digraph characteristics, the items of this list (should they exist),
will be the following, in this order:
  - name of digraph
  - order of digraph
  - list of vertices in the digraph, '[]' if order is zero
  - digraph size, '[]' if no edges
  - (if tournament) (n,k)-tournament label
  - (") list of kings, or which one is emperor
  - (alternatively to above two points) list of kings, '[]' if no kings
  - (") min k val, '0' if no kings
  - (") max k val, '0' if no kings
  - list of digraph's strong components (acquired through list_digraph_strong_components())
- `list_king_characteristics()`: will return list of lists of characteristics of kings of digraphs, each list corresponding
to a king will be composed of the following (if characteristics exist), in this order:
  - king vertex id (what it is in the digraph)
  - king's k val
  - (if Dv has been calc'ed through calc_dvs_cvs()) the set of king's Dv, and the GCD(Dv)
  - (if Cv has been calc'ed through calc_dvs_cvs()) the set of king's Cv, and the GCD(Cv)
- `list_digraph_strong_components()`: will return list of lists of the digraphs strong components, there is an option
to ignore isolated vertices, which are inherently a strong component of a digraph.

``Development Notes: Some of the above methods could be adjusted to return actual output that can be written to a file,
I may not have time to actually implement this, so if someone else wanted to take a crack at it, please do.``

---

### DKS_Product_Digraph
On being given the following parameters, will create an object of this class-type:
- `digraph1`: required, is of type DKS_Digraph
- `digraph2`: required, is of type DKS_Digraph

The DKS_Product_Digraph houses most of the same functionality as DKS_Digraph, barring some functionalities specific to the 
analysis of direct product digraphs. The following attributes are part of the DKS_Product_Digraph object on instantiation:
- `self.D1`: houses the DKS_Digraph given from digraph1
- `self.D2`: houses the DKS_Digraph given from digraph2
- `self.D1xD2`: houses the tensor-product (i.e. direct-product) of self.D1, and self.D2, and stores it as a DKS_Digraph object;
the name of the product digraph is a concatenation of the name attribute of self.D1, and self.D2. As self.D1xD2 is itself
a DKS_Digraph object, all the functionality given in DKS_Digraph applies to this attribute.

The following methods are part of the DKS_Product_Digraph, these methods are covered briefly, if more details are needed,
you are encouraged to go into the source code and take a peek around:
- `get_product_extrenum_k_val_kings()`: depending on what the user seeks, given all kings in the product, will provide 
output that identifies kings that have k values either equal to the **minimum**, or **maximum** k value of the digraph.
It will also identify the factor vertices of the product king, and provide information about the factor vertices.
- `max_k_below_upper_bound()`: In the master's thesis of M.Norge regarding kings in the direct product of digraphs, she
provided an upper bound for the k value of all kings in the product, this function provides output that checks if the 
max_k_val of the product digraph is below, or at that theorized upper bound.
- `compare_gcdv_gcdcv()`: INCOMPLETE, wanted to compare the gcd of the dv, and the gcd of the cv of kings, this was to 
make the proofs of the theorems in our paper more clean, and tidy. Will update this soon as I move my experimental code
into the function...
___

## Util.py
Provides tools to parse files that have digraphs/tournaments encoded in them. Has two functions  one which parses 
.txt files (which generate tournaments), and .d6 files (which generate digraphs). Both are specific to the
encoding scheme of the files acquired for the study from the following URL: 
https://users.cecs.anu.edu.au/~bdm/data/digraphs.html

### `mckay_txt_parser()`

The function, on being given a filename (that corresponds to a .txt file that is a validly encoded tournament), as well
as a line number (each line of the .txt file corresponds to an individual tournament), will produce the tournament from
the 1s and 0s on that line number. Specifically, the 1s and 0s are the top-right triangle of an adjacency matrix of the
vertices of a tournament, in other words, if the line contained the string: '101101' the corresponding adjacency matrix
would be:

```
tournament adjacency matrix:
 
            v1  v2  v3  v4 
      v1    x   1   0   1
      v2    x   x   1   0
      v3    x   x   x   1
      v4    x   x   x   x
  ```
In tournaments, each pair of distinct vertices has one adjacency between them, with '1' representing that the left-hand
vertex is "adjacent to" the corresponding top vertex, and '0' representing that the left-hand vertex is "adjacent from"
the top vertex. In the above example, **[v1 => v2]** (v1 is _adjacent to_ v2), and **[v1 <= v3]** (v1 is _adjacent from_ v3). 

A brief summary of how the function works mechanically is as follows:
- the function opens the provided filename using the 'read' mode, and in using the linecache module, will roll through
the lines of the file until the specified line number is found. The reason linecache is used, is when dealing with larger
files with millions of lines-- the linecache improves performance, and reduces the memory footprint.
- on finding the line, the function will mathematically determine the order of the tournament (how many vertices
the tournament has), it is to not required for the user to specify the order of the tournament beforehand, the mathematics
of this process are not detailed here, if it is of interest, please look in the source code.
- the function then on finding '1' or '0' will generate a list of vertex adjacencies, following the logic laid out in the
paragraph above the brief summary of the mechanical workings of the function.
- the function then provides this adjacency list to the generator function in the networkX library for producing digraphs,
the resulting digraph is then returned as a networkX.DiGraph object from the function.

### `mckay_d6_parser()`
This function parses and decodes .d6 text file lines to create digraphs, it does so by performing mathematical 
operations on sequences of characters to figure out the order of the digraph, and the adjacency matrix of these 
digraphs. These operations are somewhat complex, and the simplicity of the source code belies what is happening on 
a conceptual level. If you're interested in the formal definition of the .d6 filetype, and how the encoding process 
occurs, please refer to the following URL: https://users.cecs.anu.edu.au/~bdm/data/formats.txt

The following is the general logic that .d6 text files comply with in the structure of a given line in the file:
- a line begins with the delimiter '&', which denotes the beginning of a general digraph, this is for users who are 
using programming languages that require such a delimiter
- the second character in the line represents the order of the digraph, this is required in order to properly translate 
the bit-string (yielded from the process outlined in third point) to an adjacency matrix, this is done by calculating the
size of the adjacency matrix required, i.e. if we have n vertices (order n), the matrix needs to be n^2 long
- the remaining characters of the line represent the encoded adjacencies in the digraph (structure of a matrix), the 
process of decoding is the following:
  - convert the character to its integer (decimal) representation, i.e. '@' is 64 in decimal
  - subtract 63 from the above, and take the six-length binary representation of this result, appending zeroes to the 
  left of the binary number if need be i.e. '@' => (64 - 63 = 1) => bin[1] => bin[000001]
  - append the converted six-length binary representation of the char to the right-hand side of placeholder string that 
  houses all such converted chars, e.g. "@?@" => '000001' + '000000' + '000001' => "000001000000000001"
  - from the above final string, we extract (starting from the left-hand side) matrix-length characters, which are the 
  0's and 1's which denote the adjacencies between each pair of vertices in the digraph, in the structure of a matrix,
  from this matrix, we may extract the adjacency list
- with the adjacency list from the matrix, we can construct the digraph, which will then be returned as a 
networkX.DiGraph object from the function.

## Experiment Functions

### Purpose
This part of the module houses experiment functions that should not necessarily be part of the classes provided in `Analysis.py`.
The functions herein contained are moreso external to the functionalities tied specifically to digraphs, tournaments, etc.
Having the functions stored here also serves as a way to have a clean playground in which that the messy process of experimental
setup does not touch how the classes/functions are set up.

Right now, there's two functions inside this file, one that serves as the master function, and helper functions that operate
on the principle of multi-threading. The parameters related to the number of cores within the computer to be used are tied
to my (HexEmulator's) computer, so in order to BEST utilize the functions in this file as per your machine, it is advised 
that you customize how many cores are used, and adjust the for loop in the helper functions. (I also advise going through
the process of using the 'time' library and actually seeing how long each configuration of core count takes to get the 
best results!)

If you look through the source code, I have left commenting
and `TODO` instructions to the values needed to be changed for core count (ctrl+F should help you find them).

I will detail the helper, and master function now:

### min_max_k_val_kings_experiment() (MASTER FUNCTION)
During our experimentation, we were interested in the ranges of 'k-vals' as they related to the kings of the product
of tournaments. However, this would likely work with regular digraphs as well... the experiment was designed to take a
specified 'i tournament' (which is fixed throughout the experiment), and cross them with every single other 'j tournament'
(of every other order, and variety, increasing from the i tournament). 

Side note: Initially we did this linearly, with a single loop
and it was painfully slow (at least 12 hours in some cases), so we decided to utilize multi-threading to expedite the process;
this resulted in a initial reduction down to 8 hours, and then with further core-count adjustments led to 4 hours.

To launch the experiment you need:
- the order of the tournament you're seeking to cross with all others
- the specific line from the tournament file that you're looking to cross with all others

These will come together to build the 'i tournament' as previously mentioned, and then the master function then creates 
the results file where all the final data from the experiment will be written. The experiment is now ready to begin--

The process by which the experiment takes place can be summed up, like so:
- a number of processes (the count specified by the user) will each be tasked with utilizing a helper function (detailed
later) in order to produce 1/P# of the final result file, where P# is the number of processes, these are written as .part files;
these .part files are ***per order*** of the digraphs that they're working on... i.e. all processes will work on order 3 together
until that order is fully worked through, with processes that finish in that specific order first-- will not start on the next order
until all other processes have caught up
- when all processes have finished their portion of the total results file-- the information from the individual .part files
is stitched together in the final results file, when all the parts have been written over-- the next order .part files can
be processed
- This process continues until all order digraphs have been processed, and everything is written to the master file

(I will admit, I could probably have the .part files for the next order be processed at the same time as the .part files are written
to the master file... but eh, I didn't really have time to think about that, I think the next person to work on that could work on it,
if they genuinely need to)


### mmkvk_gen_result_part() (HELPER FUNCTION)
The process by which the helper function works is the following:
- the function is given an 'i tournament', this is per the arguments given to the master function
- also from its arguments, it will have a file name that is a dedicated location for all pertinent results to be written to
- the function also has a specified order, and line number to start on-- these are heavily dependent on the cores/threads to be used
- the helper will construct the j tourn from the order, and line number and will process the combination of the i tourn, and the j tourn
- it will then write the results to it's specified .part file
- upon finishing that calculation, and writing, it will then hop a specific number of lines down the file, it will repeat the
above processes until it reaches the end of the file, it will finish execution at this point, and release the file for reading
by the master function

Everything above will be executed by P# processes, and the 'hop' as given in the final point is essentially spacing all the
helper functions working in parallel in the correct manner so that work is not repeated between processes...

Could likely have a macro at the top of the file to specify the number of cores to be used, but I did not get around to doing that
elegantly.