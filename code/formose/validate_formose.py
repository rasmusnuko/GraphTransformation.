import networkx as nx
from networkx.algorithms import isomorphism as iso
import formose
import MOD_formose_graphs

# Get MØD reference graphs
references = MOD_formose_graphs.graphs

instances = {}
instances[4] =  [{'n_glyco': 0, 'm_formal': 1}]

instances[8] =  [{'n_glyco': 0, 'm_formal': 2}, 
                 {'n_glyco': 1, 'm_formal': 0}]

instances[12] = [{'n_glyco': 0, 'm_formal': 3},
                 {'n_glyco': 1, 'm_formal': 1}]

instances[16] = [{'n_glyco': 0, 'm_formal': 4},
                 {'n_glyco': 2, 'm_formal': 0},
                 {'n_glyco': 1, 'm_formal': 2}]

instances[20] = [{'n_glyco': 0, 'm_formal': 5},
                 {'n_glyco': 1, 'm_formal': 3},
                 {'n_glyco': 2, 'm_formal': 1}]

# Go through all test instances
for num_atoms in instances:

  # Get output graphs from formose for this instance
  for proportion in instances[num_atoms]:
    output_graphs = formose.perform_formose(proportion['n_glyco'], proportion['m_formal'])

    # assert graph has num nodes == num atoms
    for graph in output_graphs:
      assert len(graph.nodes) == proportion['n_glyco']*8 + proportion['m_formal']*4

    # assert all components are isomorphic to some reference graph
    for graph in output_graphs:
      components = (graph.subgraph(c).copy() for c in nx.connected_components(graph))
      for component in components:
        isomorphic = False
        for ref in references:
          if iso.is_isomorphic(ref, ref,
                               node_match=iso.categorical_node_match('attr', ''),
                               edge_match=iso.categorical_edge_match('attr', '')):
             isomorphic = True
             break
    
        assert(isomorphic)

print('================================================')
print(f"Tested graphs with num atoms: {[n for n in instances]}.")
print("All graphs/components match reference graphs generated from MØD.")
