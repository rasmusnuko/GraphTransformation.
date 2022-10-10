import networkx as nx
import sys
sys.path.insert(1, '..')
from production import Production

""" Init Graphs """
# Graph G
G = nx.Graph(name='G')
G.add_node(1, attr=1)
G.add_node(2, attr=2)
G.add_edge(1, 2)
nx.set_edge_attributes(G, {(1, 2): 'a'}, name='attr')

# Graph L
L = nx.Graph(name='L')
L.add_node(2, attr=2)

# Graph R
R = nx.Graph(name='R')
R.add_node(3, attr=3)
R.add_node(4, attr=4)
R.add_edge(3, 4)
nx.set_edge_attributes(R, {(3, 4): 'b'}, name='attr')


""" Production p """
LR_mapping = {2: 3}
p = Production(L, R, LR_mapping, name='TEST', debug=True)

# Find LG mapping
m1s = p.possible_LG_mappings(G)

# Perform transformation
H = p.perform_transformation(G, m1s[0])

# Assert output graph H
print('===============')
print('TEST SUCCESSFUL')
