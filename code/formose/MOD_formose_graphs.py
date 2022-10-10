"""
Created using https://www.cheminfo.org/flavor/malaria/Utilities/SMILES_generator___checker/index.html
Which allows us to generate smiles from skeleton structures
"""
import sys
sys.path.insert(1, '..')
from graph_gen import graph_from_smiles

# Stores graphs from MØD
graphs = []

# 20 atoms
graphs = []
graphs.append(graph_from_smiles("OC=CO"))
graphs.append(graph_from_smiles("C=O"))
graphs.append(graph_from_smiles("OC=C(O)C(O)(CO)CO"))
graphs.append(graph_from_smiles("O=CC(O)C(O)(CO)CO"))
graphs.append(graph_from_smiles("O=C(CO)C(O)(CO)CO"))
graphs.append(graph_from_smiles("O=CC(O)(CO)CO"))
graphs.append(graph_from_smiles("OCC(O)=C(O)CO"))
graphs.append(graph_from_smiles("O=CCO"))
graphs.append(graph_from_smiles("O=C(CO)CO"))
graphs.append(graph_from_smiles("O=CCC(O)CO"))
graphs.append(graph_from_smiles("OC=C(O)CO"))
graphs.append(graph_from_smiles("O=CC(O)C(O)CO"))
graphs.append(graph_from_smiles("OC=C(O)C(O)CO"))
graphs.append(graph_from_smiles("O=CC(O)(CO)C(O)CO"))
graphs.append(graph_from_smiles("O=CC(O)C(O)C(O)CO"))
graphs.append(graph_from_smiles("OC=C(O)C(O)C(O)CO"))
graphs.append(graph_from_smiles("O=C(CO)C(O)C(O)CO"))
graphs.append(graph_from_smiles("OCC(O)=C(O)C(O)CO"))
graphs.append(graph_from_smiles("O=C(C(O)CO)C(O)CO"))
