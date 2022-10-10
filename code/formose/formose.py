from networkx.algorithms import isomorphism as iso
import formose_grammar
from datetime import datetime

debug = False
silent = False

def perform_formose(n_glyco, m_formal):
  rules = formose_grammar.formose_rules
  # Start_graph
  start_graph = formose_grammar.generate_start_graph(n_glyco, m_formal)
  # Formose grammar rules imported from formose_grammar
  # init 
  generated_graphs = [start_graph]
  new_non_iso = [start_graph]
  start_time = datetime.now()
  iteration_count = 0
  total_num_graphs = 1
  num_this_iteration = 1

  # Run formose grammar until no new graphs are generated
  while num_this_iteration > 0:
    prev_iteration_time = datetime.now()
    iteration_count += 1
    # Generate new graphs
    new_graphs = []
    for G in new_non_iso:
      for rule in rules:
        new_graphs.extend(rule.perform_all_transformations(G))
    total_num_graphs += len(new_graphs)
    
    # Reset new_non_iso for next iteration
    new_non_iso = []

    # Only add new graphs to new_non_iso
    for i, graph_1 in enumerate(new_graphs):
      isomorphic = False
      for j, graph_2 in enumerate(new_graphs):
        if i < j:
          if iso.is_isomorphic(graph_1, graph_2,
                               node_match=iso.categorical_node_match('attr', ''),
                               edge_match=iso.categorical_edge_match('attr', '')):
            isomorphic = True
            break
  
      if not isomorphic:
        new_non_iso.append(graph_1)
        rules[0].show_graph(graph_1)
    
    # Check for isomorphism between graphs from this iteration and generated_graphs 
    num_this_iteration = 0
    for graph_1 in new_non_iso:
      isomorphic = False
      for graph_2 in generated_graphs:
        if iso.is_isomorphic(graph_1, graph_2,
                             node_match=iso.categorical_node_match('attr', ''),
                             edge_match=iso.categorical_edge_match('attr', '')):
          isomorphic = True
          new_non_iso.remove(graph_1)
          break
  
      if not isomorphic:
        num_this_iteration += 1
        generated_graphs.append(graph_1)
  
    iteration_time = datetime.now()

    if not silent:
      print(f"Iteration {iteration_count}: {iteration_time-prev_iteration_time}")
      print(f"Iteration {iteration_count} generated {len(new_non_iso)} new graphs")
  

  # Print results
  end_time = datetime.now()
  print('----------------------------------')
  print(f"Total time: {end_time-start_time}")
  print(f"Total iterations: {iteration_count}")
  print(f"Total number of graphs: {total_num_graphs}")
  print(f"Total number of non-isomorphic graphs: {len(generated_graphs)}")
  print(f"Unique ratio: {len(generated_graphs)/total_num_graphs}")
  print(f"Time per graph: {(end_time-start_time)/total_num_graphs}")
  print(f"Time per unique graph: {(end_time-start_time)/len(generated_graphs)}")
  print(f"Total number of glycolaldehyde: {n_glyco}")
  print(f"Total number of formaldehyde: {m_formal}")
  print(f"Total atom count: {n_glyco*8 + m_formal*4}")

  return generated_graphs


# Get user input
if __name__ == "__main__":
  glycolaldehyde = int(input("Number of glycolaldehyde: "))
  formaldehyde = int(input("Number of formaldehyde: "))
  perform_formose(glycolaldehyde, formaldehyde)
