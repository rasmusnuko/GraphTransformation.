import networkx as nx
import sys
sys.path.insert(1, '..')
from production import Production
from graph_gen import graph_from_smiles

# SET TO TRUE IF DEBUG PRINTS ARE WANTED
debug = False

"""
GENERATE START GRAPH
"""
def generate_start_graph(n_glyco, m_formal):
  # Molecules
  formaldehyde = graph_from_smiles("C=O", name="Formaldehyde")
  glycolaldehyde = graph_from_smiles( "OCC=O", name="Glycolaldehyde")

  # Proportions, given by n_glyco and m_formal
  molecules = [{'amount': n_glyco, 'graph': glycolaldehyde, 'symbol': 'g'},
            {'amount': m_formal, 'graph': formaldehyde, 'symbol': 'f'}]
  
  # Generate graph
  G = nx.Graph(name='Start_graph')
  for molecule in molecules:
    # Add 'amount' of molecule
    for i in range(molecule['amount']):
      # Add nodes and edges
      G.add_nodes_from(molecule['graph'].nodes)
      G.add_edges_from(molecule['graph'].edges)
      # Copy node and edge attributes
      nx.set_node_attributes(G, nx.get_node_attributes(molecule['graph'], name='attr'), name='attr')
      nx.set_edge_attributes(G, nx.get_edge_attributes(molecule['graph'], name='attr'), name='attr')
      # Relabel nodes
      relabel_dict = dict([(node, f"{molecule['symbol']}{i}_{node}") for node in molecule['graph'].nodes])
      G = nx.relabel_nodes(G, relabel_dict)

  return G


"""
GRAMMAR RULES
"""
#### ketoEnol_F
keto_L_F = nx.Graph(name='Keto_L_F')
keto_L_F.add_node(0, attr="C")
keto_L_F.add_node(1, attr="C")
keto_L_F.add_node(2, attr="O")
keto_L_F.add_node(3, attr="H")
keto_L_F.add_edge(0, 1, attr=1)
keto_L_F.add_edge(0, 3, attr=1)
keto_L_F.add_edge(1, 2, attr=2)

keto_R_F = nx.Graph(name='Keto_R_F')
keto_R_F.add_node(0, attr="C")
keto_R_F.add_node(1, attr="C")
keto_R_F.add_node(2, attr="O")
keto_R_F.add_node(3, attr="H")
keto_R_F.add_edge(0, 1, attr=2)
keto_R_F.add_edge(1, 2, attr=1)
keto_R_F.add_edge(2, 3, attr=1)

ketoEnol_F = Production(keto_L_F, keto_R_F, debug=debug, name='KetoEnol_F')

#### ketoEnol_B
keto_L_B = nx.Graph(name='Keto_L_B')
keto_L_B.add_node(0, attr="C")
keto_L_B.add_node(1, attr="C")
keto_L_B.add_node(2, attr="O")
keto_L_B.add_node(3, attr="H")
keto_L_B.add_edge(0, 1, attr=2)
keto_L_B.add_edge(1, 2, attr=1)
keto_L_B.add_edge(2, 3, attr=1)

keto_R_B = nx.Graph(name='Keto_R_B ')
keto_R_B.add_node(0, attr="C")
keto_R_B.add_node(1, attr="C")
keto_R_B.add_node(2, attr="O")
keto_R_B.add_node(3, attr="H")
keto_R_B.add_edge(0, 1, attr=1)
keto_R_B.add_edge(0, 3, attr=1)
keto_R_B.add_edge(1, 2, attr=2)

ketoEnol_B = Production(keto_L_B, keto_R_B, debug=debug, name='KetoEnol_B')

#### aldolAdd_F
aldol_L_F = nx.Graph(name='Aldol_L_F')
aldol_L_F.add_node(0, attr="C")
aldol_L_F.add_node(1, attr="C")
aldol_L_F.add_node(2, attr="O")
aldol_L_F.add_node(3, attr="H")
aldol_L_F.add_node(4, attr="O")
aldol_L_F.add_node(5, attr="C")
aldol_L_F.add_edge(0, 1, attr=2)
aldol_L_F.add_edge(1, 2, attr=1)
aldol_L_F.add_edge(2, 3, attr=1)
aldol_L_F.add_edge(4, 5, attr=2)

aldol_R_F = nx.Graph(name='Aldol_R_F')
aldol_R_F.add_node(0, attr="C")
aldol_R_F.add_node(1, attr="C")
aldol_R_F.add_node(2, attr="O")
aldol_R_F.add_node(3, attr="H")
aldol_R_F.add_node(4, attr="O")
aldol_R_F.add_node(5, attr="C")
aldol_R_F.add_edge(0, 1, attr=1)
aldol_R_F.add_edge(0, 5, attr=1)
aldol_R_F.add_edge(1, 2, attr=2)
aldol_R_F.add_edge(3, 4, attr=1)
aldol_R_F.add_edge(4, 5, attr=1)

aldolAdd_F = Production(aldol_L_F, aldol_R_F, debug=debug, name='AldolAdd_F')


#### aldolAdd_B
aldol_L_B = nx.Graph(name='Aldol_L_B')
aldol_L_B.add_node(0, attr="C")
aldol_L_B.add_node(1, attr="C")
aldol_L_B.add_node(2, attr="O")
aldol_L_B.add_node(3, attr="H")
aldol_L_B.add_node(4, attr="O")
aldol_L_B.add_node(5, attr="C")
aldol_L_B.add_edge(0, 1, attr=1)
aldol_L_B.add_edge(0, 5, attr=1)
aldol_L_B.add_edge(1, 2, attr=2)
aldol_L_B.add_edge(3, 4, attr=1)
aldol_L_B.add_edge(4, 5, attr=1)

aldol_R_B = nx.Graph(name='Aldol_R_B')
aldol_R_B.add_node(0, attr="C")
aldol_R_B.add_node(1, attr="C")
aldol_R_B.add_node(2, attr="O")
aldol_R_B.add_node(3, attr="H")
aldol_R_B.add_node(4, attr="O")
aldol_R_B.add_node(5, attr="C")
aldol_R_B.add_edge(0, 1, attr=2)
aldol_R_B.add_edge(1, 2, attr=1)
aldol_R_B.add_edge(2, 3, attr=1)
aldol_R_B.add_edge(4, 5, attr=2)

aldolAdd_B = Production(aldol_R_B, aldol_R_B, debug=debug, name='AldolAdd_B')

formose_rules = [ketoEnol_F, ketoEnol_B, aldolAdd_F, aldolAdd_B]
