import networkx as nx
import sys
sys.path.insert(1, '..')
from production import Production

""" Init Graphs """
# Graph L
L = nx.Graph(name='L')
L.add_node(1,pos=(1,1), attr=1)
L.add_node(2,pos=(2,2), attr=2)
L.add_node(3,pos=(1,3), attr=3)
L.add_edge(1,2)
L.add_edge(2,3)

# Graph R
""" Init graphs R"""
R = nx.Graph(name='R')
R.add_node(1,pos=(1,1), attr=1)
R.add_node(2,pos=(2,2), attr=2)
R.add_node(3,pos=(1,3), attr=3)
R.add_node(4,pos=(2,3), attr=4)
R.add_edge(1,2)
R.add_edge(2,4)
R.add_edge(1,3)

# Graph K
prod = Production(L, R, debug=True)
prod.show_prod()

assert prod.L == L
assert prod.R == R

print('===============')
print('TEST SUCCESSFUL')
