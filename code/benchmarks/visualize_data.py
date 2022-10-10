import matplotlib.pyplot as plt
import numpy as np
import csv

def get_header_and_rows(csv_fil):
  # Open file and make csv reader
  fil = open(f'./raw_data/{csv_fil}')
  csv_reader = csv.reader(fil)

  # Get header and data
  header = []
  header = next(csv_reader)
  rows = [row for row in csv_reader]

  return header, rows


def extract_label_data(csv_fil):
  header, rows = get_header_and_rows(csv_fil)

  data = {int(row[0]): [] for row in rows} # dict indices are num_nodes
  for row in rows:
    data[int(row[0])].append(float(row[1])) # row[1] is time
  
  return data

def extract_formose_data(csv_fil):
  header, rows = get_header_and_rows(csv_fil)

  # dict incides are (n_glyco, m_formal)
  proportion_data = {(int(row[0]), int(row[1])): [] for row in rows}
  for row in rows:
    n_glyco = int(row[0])
    m_formal = int(row[1])
    proportion_data[n_glyco, m_formal].append(float(row[2])) # row[2] is time
  
  # dict incides are n_glyco
  glyco_data = {int(n_glyco): [] for n_glyco, m_formal in proportion_data}
  for (n_glyco, m_formal) in proportion_data:
    glyco_data[int(n_glyco)].append(np.mean(proportion_data[n_glyco, m_formal]))

  # dict incides are m_formal
  formal_data = {int(m_formal): [] for n_glyco, m_formal in proportion_data}
  for (n_glyco, m_formal) in proportion_data:
    formal_data[int(m_formal)].append(np.mean(proportion_data[n_glyco, m_formal]))

  # dict incides are num_atoms
  atoms_data = {(int(n_glyco)*8 + int(m_formal)*4): [] for n_glyco, m_formal in proportion_data}
  for (n_glyco, m_formal) in proportion_data:
    num_atoms = int(n_glyco)*8 + int(m_formal)*4
    atoms_data[num_atoms].extend(proportion_data[n_glyco, m_formal])
  
  # dict incides are total_num_iso_checks
  iso_check_data = {int(row[-1]): [] for row in rows}
  for row in rows:
    iso_check_data[int(row[-1])].append(float(row[2][:]))
  
  proportion_data = {i: proportion_data[n_glyco, m_formal] for i, (n_glyco, m_formal) in enumerate(proportion_data)},
  print(proportion_data)
  
  return atoms_data, iso_check_data, glyco_data, formal_data

def plot_data():
  # Extract raw data
  matching_data = extract_label_data('label_benchmark_matching.csv')
  production_data = extract_label_data('label_benchmark_production.csv')
  atoms_data, iso_check_data, glyco_data, formal_data = extract_formose_data('formose_benchmark.csv')

  # Preparation
  graphs = {'matching':   {'data': matching_data,
                           'xlabel': 'Number of nodes',
                           'ylabel': 'Time in seconds',
                           'xscale': 'linear',
                           'yscale': 'linear',
                           'title': 'Time for finding subgraph isomorphism from L to G.'},

            'production': {'data': production_data,
                           'xlabel': 'Number of nodes',
                           'ylabel': 'Time in seconds',
                           'xscale': 'linear',
                           'yscale': 'linear',
                           'title': 'Time of performing production p and q.'},

            'match_log':  {'data': matching_data,
                           'xlabel': 'Number of nodes',
                           'ylabel': 'Time in seconds',
                           'xscale': 'linear',
                           'yscale': 'log',
                           'title': 'Time for finding subgraph isomorphism from L to G.'},

            'prod_log':   {'data': production_data,
                           'xlabel': 'Number of nodes',
                           'ylabel': 'Time in seconds',
                           'xscale': 'linear',
                           'yscale': 'log',
                           'title': 'Time of performing production p and q.'},

            'atoms':      {'data': atoms_data,
                           'xlabel': 'Number of atoms',
                           'ylabel': 'Time in seconds',
                           'xscale': 'linear',
                           'yscale': 'linear',
                           'title': 'Time of formose grammar\nwith different number of atoms in the starting graph.'},

            'Iso checks': {'data': iso_check_data,
                           'xlabel': 'Number of isomorphism checks',
                           'ylabel': 'Time in seconds',
                           'xscale': 'linear',
                           'yscale': 'linear',
                           'title': 'Time of formose grammar\nwith different number of isomorphism checks.'},

            'glyco': {'data': glyco_data,
                           'xlabel': 'Number of glycolaldehyde',
                           'ylabel': 'Time in seconds',
                           'xscale': 'linear',
                           'yscale': 'log',
                           'title': 'Time of formose grammar\nwith number of glycolaldehyde molecules.'},

            'formal': {'data': formal_data,
                           'xlabel': 'Number of formaldehyde',
                           'ylabel': 'Time in seconds',
                           'xscale': 'linear',
                           'yscale': 'log',
                           'title': 'Time of formose grammar\nwith number of formaldehyde molecules.'}
           }


  for graph in graphs:
    print(graph)
    x = list(graphs[graph]['data'].keys())
    print(x)
    y = list(graphs[graph]['data'].values())
    x = np.array(x)
    y = np.array(y)
    mins   = np.array([min(values) for values in y])
    maxs   = np.array([max(values) for values in y])
    means  = np.array([np.mean(values) for values in y])
    minus_errors = [means[i]-mins[i] for i in range(len(means))]
    plus_errors  = [maxs[i]-means[i] for i in range(len(means))]
    errors = np.array([minus_errors, plus_errors])
    plt.errorbar(x, means, errors, fmt='.k', ecolor='gray', lw=1)
    plt.xscale(graphs[graph]['xscale'])
    plt.yscale(graphs[graph]['yscale'])
    if graph == 'atoms':
      plt.xticks([4,8,12,16,20,24,28,32,36,40])
    plt.title(graphs[graph]['title'])
    plt.xlabel(f"{graphs[graph]['xlabel']} ({graphs[graph]['xscale']} scale)")
    plt.ylabel(f"{graphs[graph]['ylabel']} ({graphs[graph]['yscale']} scale)")
    plt.show()


if __name__ == '__main__':
  plot_data()
