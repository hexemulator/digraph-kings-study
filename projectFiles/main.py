'''
BibTeX entry, for when we need it! :-)
@InProceedings{SciPyProceedings_11,
  author =       {Aric A. Hagberg and Daniel A. Schult and Pieter J. Swart},
  title =        {Exploring Network Structure, Dynamics, and Function using NetworkX},
  booktitle =   {Proceedings of the 7th Python in Science Conference},
  pages =     {11 - 15},
  address = {Pasadena, CA USA},
  year =      {2008},
  editor =    {Ga\"el Varoquaux and Travis Vaught and Jarrod Millman},
}
'''

import networkx as nx                   # requirement
from networkx_viewer import Viewer      # needed for cool visualization of graphs
import math                             # needed for gcd, and comb functions
import functools                        # needed to use 'reduce' with gcd
from DKS_tools import DP_Analysis as dpa
from DKS_tools import Parser as p

'''
CREATING GRAPHS, there are many ways to do it, we can either do it on a vertex-by-vertex, or edge-by-edge basis
later in the document, there are other methods used
'''

# Create digraphs, can do so individually, or as a list of vertices, and edges
D = nx.DiGraph()
D.add_node('a')
D.add_node('b')
D.add_node('c')
D.add_edge('a', 'b')
D.add_edge('b', 'c')
D.add_edge('c', 'a')

'''
Relabelling Nodes:
Could be useful for if two digraphs share a similar vertex naming scheme, would reduce confusion
'''
# convert_node_labels_to_integers(GRAPH, startingnum, ordering, label attribute)
# relabel_nodes(GRAPH, dictionary_mapping... {old_name:new_name,old_name2:new_name2 ...}, TRUE/FALSE if you want copy of graph with old labeling scheme...)

'''
CREATING CYCLE GRAPHS
could be helpful if we want to start from a cycle graph and add vertices onto it, or do product of a graph with a specific cycle graph
the cycles can be directed as well
'''
# C = nx.cycle_graph(3, nx.DiGraph)

'''
GENERATING A RANDOM TOURNAMENT
could generate random tournaments if we needed them, but obviously this would not be good for actually studying what happens
'''
# print(nx.tournament.random_tournament(5).edges)

'''
IDENTIFYING SELF-LOOP VERTICES
will identify nodes which have an edge to themselves (possibly good for hunting down digraphs that go against our definition)
'''
nx.nodes_with_selfloops(D) # returns an iterator
print((nx.number_of_selfloops(D) > 0)) # returns True/False based on expression, should be False, as D has no self-loops

'''
DETERMINING 'k' value of a k-king of a vertex, or multiple vertices:

given a graph, G, in networkx, eccentricity is the term used for the value of the maximal shortest length dipath from a 
vertex, v in G, to all other vertices in G... I believe we can get the set of eccentricities for each v, if we wanted. 
'''

# gives the eccentricity of each node, equivalent to being a 'k-king'
for node in D.nodes:
    try:
        k_val = nx.eccentricity(D, node)
        print(str(node) + ' is a ' + str(k_val) + '-king.')
    except:
        print(str(node) + ' is not a king.')
        pass

'''
DIRECT NEIGHBOUR LOOKUP:
in case we want to look at immediate out-neighbours of a specific vertex!
'''
print(D['a'])

'''
CHECKING THE EXISTENCE OF SPECIFIC PATHS:
'''
# True/False if path arg in D is a path, edge set of D runs off key:value pairings; essentially a dict
print(nx.is_path(D,{'a':'b','b':'c'}))

'''
INDUCED SUBGRAPHS GIVEN A SET OF VERTICES:
'''
# can induce a subgraph over a list of vertices
D2 = nx.induced_subgraph(D,{'a','b'})

'''
CHECKING IF A DIGRAPH IS A TOURNAMENT
'''
# True/False if arg is a tournament or not
print("tournament check:")
print(nx.is_tournament(D2))
# (Above will be a tournament, as D was a tournament, any induced sub-digraph, D2, will also be a tournament)

'''
CHECKING IF A DIGRAPH IS A TOURNAMENT (ALTERNATE)

makes use of two functions--
    is_k_regular: checks if a given graph (no digraphs allowed) are k regular
    to_undirected: creates an undirected graph from the vertices and edges of a directed graph
    
could potentially use these two functions in conjunction to do something for research?
'''
# checks if a graph is k-regular, since each pair of vertices needs to be adjacent, in the undirected graph of a digraph--
# the degree of any single vertex will be the order of the graph minus 1.
print(nx.is_k_regular(nx.to_undirected(D),(D.order() -1)))

'''
ADDING EDGES AS A LIST OF LISTS:
'''
# can add edges related to a non-existing vertex, and networkx will add it automatically (could streamline parsing)
D.add_edges_from([['a','d'],['d','c'],['b','d']])
print(nx.is_tournament(D))

'''
ALTERNATE CASE OF CHECKING IF VERTICES ARE KINGS, graph has isolated vertex
'''
# checking what happens in the case of an isolated vertex
D.add_node('e')
for node in D.nodes:
    try:
        k_val = nx.eccentricity(D, node)
        print(str(node) + ' is a ' + str(k_val) + '-king.')
    except:
        print(str(node) + ' is not a king.')
        pass
# result-- all vertices are not kings, as expected, since 'e' is unreachable

# RECONNECTING D, expected result: every vertex but 'e' is a king
D.add_edge('d','e')
for node in D.nodes:
    try:
        k_val = nx.eccentricity(D, node)
        print(str(node) + ' is a ' + str(k_val) + '-king.')
    except:
        print(str(node) + ' is not a king.')
        pass
# result-- all vertices excepting 'e' are kings now, 'e' cannot be a king because out-neighbourhood is the empty set

'''
CHECKING IF GRAPH IS DIRECTED
'''

# will return True if a given graph is directed
print(nx.is_directed(D))

'''
DENSITY OF GRAPHS:

for tournaments, it will always be 0.5... this is because each possible pair of vertices in the tournament
they only have one arc between them, and the equation for calcing density, d, is:
        d = (m/n(n-1))
        consider m will be (n binom 2) (...because tournaments), thus, m is equivalent to n(n-1)/2
        thus,
        d = (n(n-1)/2)/n(n-1)
        by cancellation, d = 1/2
'''
print(nx.density(D))

# NOT sure if above will be particularly useful, but possibly a certain density might tie in somewhere, or be useful in some way

'''
SHORTEST PATHS BETWEEN TWO VERTICES OF A GRAPH:
'''
print(nx.shortest_path(D,'a','c')) # gives list corresponding to a shortest ('a','c')-dipath, (randomly chosen?)
print(nx.shortest_path_length(D,'a','c')) # can also get shortest path length: arc count between vertices

# SHORTEST CYCLE ON A SPECIFIC VERTEX
# below finds a cycle on a particular vertex, only finds shortest dipath from vertex to itself... cannot be used to find the sequences of all shortest cycles
# i.e. if there are two cycles on a vertex, both of shortest length, below will only give ONE of them, whichever is found first
# note: accepts 'orientations' as well: 'original' is normal, 'reverse' is backwards.
print(nx.find_cycle(D,'a','original'))


'''
GETTING SET OF INTEGERS CORRESPONDING TO LENGTHS OF CLOSED DIWALKS CONTAINING A SPECIFIC VERTEX:
'''
# simple cycles are dipaths that go from a vertex to itself...

# the function nx.simple_cycles(GRAPH,UPPER-BOUND) returns all simple cycles (the actual list of vertices in the cycle itself)
# that contain a set of distinct vertices given a GRAPH. The UPPER-BOUND arg is to prevent infinite run-off--

# I have decided to use the order of the GRAPH as the upper-bound, since paths in the GRAPH with two distinct vertices cannot
# be greater than the order of the GRAPH minus 1, but simple cycles CAN be a length equal to the order of the GRAPH.

# Note: there were several different functions I tried, with varying success/failure-- while it'd be nicer to just have the
# lengths of the simple cycles, I guess if we want to examine the vertices of the simple cycle, then this is it

# I'll be using the above function to find the lengths of all closed diwalks containing a specific vertex

# DEBUG: creating a closed diwalk containing 'a' of length 5 to check if the 'D.order()' upper-bound is strict, this is
# because the order of D, is 5. If it is strict, then cycles will stop being counted at (D.order() - 1)
D.add_edge('e','c')

all_closed_diwalks = nx.simple_cycles(D,D.order()) # will find all simple cycles in D and have it as a generator function (i.e. we need to iterate across to get list outputs)
lengths_of_closed_DW_of_v = set() # making it a set, as we're not interested in repeat values, this is pretty much 'S_{'a'}'

for cycle in all_closed_diwalks:

    # if a particular vertex is on a simple cycle, it means that there exists a closed diwalk that contains it of a specific length
    if 'a' in cycle:
        lengths_of_closed_DW_of_v.add(len(cycle)) # we add that length to the set of lengths 'S_{v}'
    print(cycle) # debugging

# printing results from 'S_{v}'
for length in lengths_of_closed_DW_of_v:
    print("a length of a closed diwalks containing 'a' in D is: " + str(length))

'''
GETTING GCD() of a set of integers corresponding to the lengths of closed diwalks of a vertex:
'''
# below is equivalent to gcd(S_{v})
# the math.gcd() function without the 'reduce' only takes two args 'x', and 'y', singular integers... if we want to deal
# with sets of integers, it is required we use functools.reduce()
gcd_Sv = functools.reduce(math.gcd, lengths_of_closed_DW_of_v)
print('the gcd of the lengths of all closed diwalks containing "a" is: ' + str(gcd_Sv))

# if we want to-- we can after calculating the gcd of both S_{v}, and S_{v'} separately-- we can use the above to then take the gcd of them together

''' 
CREATING DIRECT PRODUCTS:

with everything so far above-- we can look at the case of a C_{3}, and a C_{4} and their direct product
'''
C3 = nx.DiGraph()
C3.add_edges_from(([1,2],[2,3],[3,1]))
C4 = nx.DiGraph()
C4.add_edges_from((['a','b'],['b','c'],['c','d'],['d','a']))

print("Class test...")

test = dpa.DP_Analysis(C3,C4)
test.identify_maximal_k_king_vertices(test.GxH)

# verifying edges are correct
print(C3.edges)
print(C4.edges)

# a tensor_product is the name used in networkx for direct products
C3xC4 = nx.tensor_product(C3,C4)

# looking at all closed diwalks in C3xC4
all_closed_diwalks = nx.simple_cycles(C3xC4,C3xC4.order())
lengths_of_closed_DW_of_v = set()

for cycle in all_closed_diwalks:

    # if a particular vertex is on a simple cycle, it means that there exists a closed diwalk that contains it of a specific length
    if (1,'a') in cycle:
        lengths_of_closed_DW_of_v.add(len(cycle)) # we add that length to the set of lengths 'S_{v}'
    print(cycle) # debugging

# printing results from 'S_{v}'
for length in lengths_of_closed_DW_of_v:
    print("a length of the closed diwalks containing (1,'a') in C3xC4 is: " + str(length))

'''
VIEWING GRAPHS: still haven't played with this one a lot-- but the viewer app is REALLY nice-- makes looking at
and interacting with the graphs MUCH easier.
'''

# for the networkx viewer, we can alter attributes of specific nodes when we display them
C3xC4.nodes[(1,'a')]['outline'] = 'blue'
C3xC4.nodes[(2,'b')]['label_fill'] = 'red'

# below is for executing the viewer...
# app = Viewer(C3xC4)
# app.mainloop()

'''
CHECKING FOR STRONG COMPONENTS:

a strong component is a sub-digraph (which we can induce on a set of vertices) of a digraph that is strongly connected.
in the case of below-- since the GCD(GCD(S_{1}),GCD(S_{'a'})) = 1, then C3xC4 is strongly connected, and is a singular
strong component.
'''

print(nx.is_strongly_connected(C3xC4))

# we can also induce a sub-digraph, and find out if it's a strong component as well... not sure how I'd go about making
# that streamlined?

'''
Identifying BRIDGES:
Bridges are vertices such that if delete them, it causes the number of connected components in a graph to increase...
it does NOT work for directed graphs

unsure how this could be used, but using similar principles, we could identify "d-bridges", vertices that on removal
increase the number of strongly connected components in digraphs? (would need to create the function myself)
'''

bridges = nx.bridges(nx.to_undirected(C3xC4))

print("bridges in C3xC4:")
for vertex in bridges:
    print(vertex) # does not print any vertices, because C3xC4 does not have any bridges, any vertex deletion will reduce strong-component count to zero

# providing counter-example that DOES have bridges
E = nx.Graph()
E.add_edges_from([['s','t'],['t','u'],['u','v'],['v','w'],['u','w']])

bridges = nx.bridges(E)
print("bridges in E:")
for vertex in bridges:
    print(vertex)