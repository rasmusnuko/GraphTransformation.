import networkx as nx
import sys
sys.path.insert(1, '..')
from production import Production

""" Graph G """
G = nx.Graph(name='G')
G.add_nodes_from(['a', 'b', 'c', 'd'])
G.add_edges_from( [ ('a', 'b'), ('b', 'c'), ('c' ,'d') ] )

""" Graph L """
L = nx.path_graph(2)
L.name = 'L'
# nodes : 0, 1
# edges : 0 <-> 1

""" Graph R """
R = nx.path_graph(3)
R.name = 'R'

""" Production p """
p = Production(L, R, debug=True)  # Mapping done automatically via nodes indexes

m1s = p.possible_LG_mappings(G)

H = p.perform_transformation(G, m1s[0])

assert list(H.nodes) == ['a_pn', 'b_pn', 'c_pn', 'd_pn', '2_pn']
assert list(H.edges) == [('a_pn', 'b_pn'), ('b_pn', 'c_pn'), ('b_pn', '2_pn'), ('c_pn', 'd_pn')]
print('===============')
print('TEST SUCCESSFUL')
