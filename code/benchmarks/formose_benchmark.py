from networkx.algorithms import isomorphism as iso
import formose_grammar
from datetime import datetime
import csv


def perform_formose(n_glyco, m_formal):
  # Start_graph
  start_graph = formose_grammar.generate_start_graph(n_glyco, m_formal)
  # Formose grammar rules imported from formose_grammar
  rules = formose_grammar.formose_rules
  # init 
  generated_graphs = [start_graph]
  new_non_iso = [start_graph]
  start_time = datetime.now()
  iteration_count = 0
  total_num_graphs = 1
  total_num_iso_checks = 0
  num_this_iteration = 1

  # Run formose grammar until no new graphs are generated
  while num_this_iteration > 0:
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
          total_num_iso_checks += 1
          if iso.is_isomorphic(graph_1, graph_2,
                               node_match=iso.categorical_node_match('attr', ''),
                               edge_match=iso.categorical_edge_match('attr', '')):
            isomorphic = True
            break
  
      if not isomorphic:
        new_non_iso.append(graph_1)
    
    # Check for isomorphism between graphs from this iteration and generated_graphs 
    num_this_iteration = 0
    for graph_1 in new_non_iso:
      total_num_iso_checks += 1
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
  
  # Results
  end_time = datetime.now()
  data = [n_glyco, m_formal]
  data.append((end_time-start_time).total_seconds())
  data.append(iteration_count)
  data.append(total_num_graphs)
  data.append(len(generated_graphs))
  data.append(total_num_iso_checks)

  with open(r'benchmark.csv', 'a', newline='\n') as fil:
    writer = csv.writer(fil)
    writer.writerow(data)
    fil.close()

  print(f'n_glyco: {n_glyco}, m_formal: {m_formal}, time: {(end_time-start_time).total_seconds()}, iteration count: {iteration_count}, total graphs: {total_num_graphs}, total non-isomorphic grapgh: {len(generated_graphs)}, total iso checks: {total_num_iso_checks}')


if __name__ == "__main__":
  cases = {(1,0): 100,
           (0,1): 100,
           (1,1): 100,
           (1,2): 100,
           (1,3): 100,
           (1,4): 100,
           (2,1): 100,
           (2,2): 100,
           (2,3): 100,
           (2,4): 40,
           (3,1): 100,
           (3,2): 40,
           (3,3): 20,
           (4,1): 5,
           (4,2): 2}
  
  for n_glyco, m_formal in cases:
    num_iterations = cases[n_glyco, m_formal]
    for _ in range(num_iterations):
      perform_formose(n_glyco, m_formal)
