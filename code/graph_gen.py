"""
Uses pysmiles library to load/write smiles strings.
Converts it to our naming convention.
"""

from pysmiles import read_smiles, write_smiles
import networkx as nx

def graph_from_smiles(smiles, name='SMILES'):
    pysmiles_graph = nx.Graph(read_smiles(smiles, explicit_hydrogen=True))
    graph = nx.Graph(name=name)

    # Node attributes
    graph.add_nodes_from(pysmiles_graph.nodes)
    for node in pysmiles_graph.nodes:
        graph.nodes[node]['attr'] = pysmiles_graph.nodes[node]['element']

    # Edge attributes
    graph.add_edges_from(pysmiles_graph.edges)
    for edge in pysmiles_graph.edges:
        graph.edges[edge]['attr'] = pysmiles_graph.edges[edge]['order']

    return graph


def smiles_from_graph(graph):
    pysmiles_graph = graph.copy()

    # Node attributes
    for node in pysmiles_graph.nodes:
        pysmiles_graph.nodes[node]['element'] = pysmiles_graph.nodes[node]['attr']

    # Edge attributes
    for edge in pysmiles_graph.edges:
        pysmiles_graph.edges[edge]['order'] = pysmiles_graph.edges[edge]['attr']

    return write_smiles(pysmiles_graph)
