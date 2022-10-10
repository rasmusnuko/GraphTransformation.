import networkx as nx
import sys, csv
from datetime import datetime
sys.path.insert(1, '..')
from production import Production

def perform_500_transformations(num_nodes):
  # Init graphs L and R
  L = nx.Graph(name='L')
  R = nx.Graph(name='R')
  for v in range(1, num_nodes):
    L.add_edge(0, v, attr=f'L{v}')
    R.add_edge(0, v, attr=f'R{v}')
  nx.set_node_attributes(L, {v: 'L{v}' for v in L.nodes}, name='attr')
  nx.set_node_attributes(R, {v: 'R{v}' for v in R.nodes}, name='attr')

  # G is the same graph as L
  G = L
  
  # init productions p and q 
  p = Production(L, R, relabel=False)
  q = Production(R, L, relabel=False)

  # Get time from 20 LG mappings with num_nodes nodes
  p_LG_mapping = None
  for _ in range(20):
    start_matching_time = datetime.now()
    p_LG_mapping = p.possible_LG_mappings(L)[0]
    end_matching_time = datetime.now()

    # Write data to csv 
    data = [num_nodes, (end_matching_time-start_matching_time).total_seconds()]
    with open(r'label_benchmark_matching.csv', 'a', newline='\n') as fil:
      writer = csv.writer(fil)
      writer.writerow(data)
      fil.close()
    
    if _ == 19:
      print(f'LG mapping: num nodes: {data[0]}, time: {data[1]}/mapping')

  # q is the inverse of p
  q_RG_mapping = p.inverse_mapping(p_LG_mapping)


  # Get time from 500 production performances
  for _ in range(500):
    start_500_time = datetime.now()
    G = p.perform_transformation(G, p_LG_mapping)
    G = q.perform_transformation(G, q_RG_mapping)
    end_500_time = datetime.now()
    data = [num_nodes, (end_500_time-start_500_time).total_seconds()]

    # Write data to csv 
    with open(r'label_benchmark_production.csv', 'a', newline='\n') as fil:
      writer = csv.writer(fil)
      writer.writerow(data)
      fil.close()
    
    if _ == 499:
      print(f'Production: num nodes: {data[0]}, time: {data[1]}/production')


if __name__ == '__main__':
  # Different num_nodes
  cases = [500,750,1000,1500,2000,2500,3000,3500,4000,5000,7500]

  # Run each num_nodes
  for num_nodes in cases:
    perform_500_transformations(num_nodes)
