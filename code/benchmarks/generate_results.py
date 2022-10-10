import numpy as np
import csv

def get_rows(csv_fil):
  # Open file and make csv reader
  fil = open(f'{csv_fil}', 'r')
  csv_reader = csv.reader(fil)

  # Get header and data
  header = []
  header = next(csv_reader)
  rows = [row for row in csv_reader]

  return rows


def extract_label_data():
  matching_rows = get_rows('./raw_data/label_benchmark_matching.csv')
  production_rows = get_rows('./raw_data/label_benchmark_production.csv')

  matching_data = {int(row[0]): [] for row in matching_rows} # dict indices are num_nodes
  for row in matching_rows:
    matching_data[int(row[0])].append(np.round(float(row[1]), 3)) # row[1] is time
  
  production_data = {int(row[0]): [] for row in production_rows} # dict indices are num_nodes
  for row in production_rows:
    production_data[int(row[0])].append(np.round(float(row[1]), 3)) # row[1] is time

  matching_means = {num_nodes: np.mean(matching_data[num_nodes]) for num_nodes in matching_data}
  matching_mins  = {num_nodes: min(matching_data[num_nodes]) for num_nodes in matching_data}
  matching_maxs  = {num_nodes: max(matching_data[num_nodes]) for num_nodes in matching_data}
  production_means = {num_nodes: np.mean(production_data[num_nodes]) for num_nodes in production_data}
  production_mins  = {num_nodes: min(production_data[num_nodes]) for num_nodes in production_data}
  production_maxs  = {num_nodes: max(production_data[num_nodes]) for num_nodes in production_data}
  
  # Write matching data
  fil = open(f'./results/label_benchmark_matching_results.csv', 'w')
  csv_writer = csv.writer(fil)

  # Get header and data
  csv_writer.writerow(['num_nodes', 'mean_time' ,'min_time', 'max_time'])
  for num_nodes in matching_data:
    csv_writer.writerow([num_nodes, matching_means[num_nodes], matching_mins[num_nodes], matching_maxs[num_nodes]])

  fil.close()
    
  # Write matching data
  fil = open(f'./results/label_benchmark_production_results.csv', 'w')
  csv_writer = csv.writer(fil)

  # Get header and data
  csv_writer.writerow(['num_nodes', 'mean_time' ,'min_time', 'max_time'])
  for num_nodes in production_data:
    csv_writer.writerow([num_nodes, production_means[num_nodes], production_mins[num_nodes], production_maxs[num_nodes]])
    
  fil.close()

# n_glyco,m_formal,time,total_iterations,total_graphs,total_non_iso,total_iso_checks
def extract_formose_data():
  rows = get_rows('./raw_data/formose_benchmark.csv')

  data = {(int(row[0]), int(row[1])): {} for row in rows}
  for row in rows:
    data[int(row[0]), int(row[1])]['total_graphs'] = row[4]
    data[int(row[0]), int(row[1])]['total_iso_checks'] = row[6]

  time_data = {(int(row[0]), int(row[1])): [] for row in rows} # dict indices are (n_glyco,m_formal)
  for row in rows:
    time_data[int(row[0]), int(row[1])].append(np.round(float(row[2]), 3)) # row[1] is time

  time_means = {(n_glyco, m_formal): np.mean(time_data[n_glyco, m_formal]) for n_glyco, m_formal in time_data}
  time_mins  = {(n_glyco, m_formal): min(time_data[n_glyco, m_formal]) for n_glyco, m_formal in time_data}
  time_maxs  = {(n_glyco, m_formal): max(time_data[n_glyco, m_formal]) for n_glyco, m_formal in time_data}

  # Write matching data
  fil = open(f'./results/formose_benchmark_results.csv', 'w')
  csv_writer = csv.writer(fil)

  # Write header and data
  header = ['n_glyco', 'm_formal', 'total_graphs', 'total_iso_checks', 'mean_time', 'min_time', 'max_time']
  csv_writer.writerow(header)
  for n_glyco, m_formal in data:
    csv_writer.writerow([n_glyco, m_formal, data[n_glyco, m_formal]['total_graphs'], data[n_glyco, m_formal]['total_iso_checks'], time_means[n_glyco, m_formal], time_mins[n_glyco, m_formal], time_maxs[n_glyco, m_formal]])
    
  fil.close()


if __name__ == '__main__':
  extract_label_data()
  extract_formose_data()
