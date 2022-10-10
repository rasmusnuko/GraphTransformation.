import networkx as nx
import sys
sys.path.insert(1, '..')
from production import Production

""" Init Graphs """
# Graph G
G = nx.Graph()
G.name = 'G'
G.add_node('a', attr='C')
G.add_node('b', attr='C')
G.add_edge('a', 'b')
nx.set_edge_attributes(G, {('a', 'b'): 'S'}, name='attr')

# Graph L
L = nx.Graph()
L.name = 'L'
L.add_node(1, attr='C')
L.add_node(2, attr='C')
L.add_edge(1, 2)
nx.set_edge_attributes(L, {(1,2): 'S'}, name='attr')

# Graph R
R = nx.Graph()
R.name = 'R'
R.add_node(1, attr='H')
R.add_node(2, attr='H')
R.add_edge(1, 2)
nx.set_edge_attributes(R, {(1,2): 'D'}, name='attr')

""" Production p """
p = Production(L, R, name='TEST', debug=True)  # Mapping done automatically via nodes indexes

m1s = p.possible_LG_mappings(G)

H = p.perform_transformation(G, m1s[0])

assert nx.get_node_attributes(H, name='attr') == {'1_TT': 'H', '2_TT': 'H'}
assert nx.get_edge_attributes(H, name='attr') == {('1_TT', '2_TT'): 'D'}
print('===============')
print('TEST SUCCESSFUL')
