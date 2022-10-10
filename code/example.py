import networkx as nx
from production import Production

""" Input Graph """
G = nx.Graph(name='G')
# Adding nodes and node labels
G.add_nodes_from([1, 2, 3])
nx.set_node_attributes(G, {1: 'A', 2: 'B', 3: 'C'}, name='attr')
# Adding edges and edge labels
G.add_edges_from([(1,2),(2,3)])
nx.set_edge_attributes(G, {(1,2): 'X', (2,3): 'Y'}, name='attr')

""" Graph L """
L = nx.Graph(name='L')
# Adding nodes and node labels
L.add_node(2, attr='B')
L.add_node(3, attr='C')
# Adding edge and edge label
L.add_edge(2, 3, attr='Y')

""" Graph R """
R = nx.Graph(name='R')
# Adding nodes and node labels
R.add_node('u', attr='D')
R.add_node('v', attr='E')
# Adding edge and edge label
R.add_edge('u', 'v', attr='Z')

""" Production """
# Specifying LR_mapping, as L and R do not share name indices.
LR_mapping = {2: 'u', 3: 'v'}
prod = Production(L, R, LR_mapping=LR_mapping, debug=True)

""" LG mappings """
# Get list of possible LG mappings
LG_mappings = prod.possible_LG_mappings(G)

""" Performing graph transformation """
H = prod.perform_transformation(G, LG_mappings[0])
