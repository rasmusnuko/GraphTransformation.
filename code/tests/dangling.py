import sys
import networkx as nx
sys.path.insert(1, '..')
from production import Production

""" Graph G """
G = nx.Graph(name='G')
G.add_nodes_from(['a', 'b', 'c'])
nx.set_node_attributes(G, {'a': 0, 'b': 1, 'c': 0}, name='attr')
G.add_edge('a', 'b')
G.add_edge('b', 'c')
nx.set_node_attributes(G, {('a', 'b'): 0, ('b', 'c'): 1}, name='attr')

""" Init Graphs """
# Graph L
L = nx.Graph(name='L')
L.add_node(1,pos=(1,1), attr=1)

# Graph R
R = nx.Graph(name='R')

""" Production p """
p = Production(L, R, debug=True)  # Mapping done automatically via nodes indecies

m1s = p.possible_LG_mappings(G)

H = p.perform_transformation(G, m1s[0])

assert H == None
print('===============')
print('TEST SUCCESSFUL')
