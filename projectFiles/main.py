import networkx as nx
from DKS_tools import Kings as K
G = nx.Graph()
G.add_node('a')
G.add_node('b')
G.add_node('c')

G.add_edge('a','b')

print(G.number_of_nodes())
print(G.nodes)
print(G.edges)

kingtest = K.King()
print(kingtest.value)