import networkx as nx
from networkx.algorithms import isomorphism
import matplotlib.pyplot as plt

"""
Class represents a (L <- K -> R) production
"""
class Production:

  def __init__(self, L, R, LR_mapping='AUTO', debug=False, name='production', relabel=True):
    # Set true for debug prints
    self.debug = debug
    self.name = name
    
    # Graph L := LHS of prod rule
    # Graph R := RHS of prod rule
    self.L = L
    self.R = R

    # If mapping not provided, make auto mapping
    if LR_mapping == 'AUTO':
      self.LR_mapping = self.auto_mapping()
    else:
      self.LR_mapping = LR_mapping
    # Check for invalid mapping
    self.validate_mapping()

    # Construct graph K and mappings to L & R
    self.K, self.KL_mapping, self.KR_mapping = self.intersection(self.L, self.R, self.LR_mapping)
    self.K.name = 'K'
    
    # Inverse mappings
    self.RL_mapping = self.inverse_mapping(self.LR_mapping)
    self.RK_mapping = self.inverse_mapping(self.KR_mapping)

    # True if graphs are labelled
    self.labelled = len(nx.get_node_attributes(self.L, name='attr')) > 0

    # True if H should relabel nodes to counter naming colisions with R
    self.relabel = relabel

  """
  Construct the graph I from A intersection B, 
  and mappings from I->A and I->B
  """
  def intersection(self, A, B, AB_mapping):
    self.debug_print(f'Intersection: {A.name}, {B.name}', title=True)
    I = nx.Graph(A, name=f'I_{A.name}_{B.name}')

    # Edges
    translated_edges = self.translate_edges(A, AB_mapping)
    for edge in A.edges:
      if translated_edges[edge] not in B.edges:
        I.remove_edge(*edge)
      elif A.edges[edge] != B.edges[translated_edges[edge]]:
        I.remove_edge(*edge)

    # Nodes
    for u in A.nodes:
      if u not in AB_mapping:
        I.remove_node(u)
      elif A.nodes[u] != B.nodes[AB_mapping[u]]:
        I.remove_node(u)

    # Mappings for I
    IA_mapping = {node: node for node in I.nodes}
    IB_mapping = {node: AB_mapping[node] for node in I.nodes}
    
    self.debug_print([('I.nodes', I.nodes), ('I.edges', I.edges)]+[(f'{I.name}{edge}', I.edges[edge]) for edge in I.edges])
    return I, IA_mapping, IB_mapping


  """
  List all possible mappings from L onto G
  """
  def possible_LG_mappings(self, G):
    self.debug_print('LG Mappings', title=True)

    # Graphmatcher
    GraphMatcher = isomorphism.GraphMatcher(G, self.L,
         node_match=isomorphism.categorical_node_match('attr', ''),
         edge_match=isomorphism.categorical_edge_match('attr', ''))

    # Generator
    sub_iso_gen = GraphMatcher.subgraph_isomorphisms_iter()
    GL_mappings = [mapping for mapping in sub_iso_gen]

    # Make LG mappings
    LG_mappings = [self.inverse_mapping(GL_mapping) for GL_mapping in GL_mappings]
    self.debug_print([('LG_mapping', mapping) for mapping in LG_mappings])

    return LG_mappings


  """
  Produce graph H, by applying production (L -> K <- R),
  based on a specified mapping from L to G

  Prerequisites:
    R and G don't share names for nodes
    All nodes and edges must be labelled, if graphs are labelled
  """
  def perform_transformation(self, G, LG_mapping):
    self.debug_print('Single transformation', title=True)
    # Nodes and edges for graph H, the output graph
    # Use G as a basis for H
    H = nx.Graph(G, name='H')

    ### D = G \ (L \ K)
    # Difference between L and K
    LK_diff_nodes, LK_diff_edges = self.diff(self.L, self.K, self.inverse_mapping(self.KL_mapping))

    # Find nodes that can cause dangling conditions
    dangling_nodes = self.dangling_nodes(self.L, G, LG_mapping)

    # The edges in L, mapped to G
    LG_edges = self.translate_edges(self.L, LG_mapping)
    # Removing edges
    for edge in LK_diff_edges:
      self.debug_print([('removing edge', LG_edges[edge])])
      H.remove_edge(*LG_edges[edge])

    # Removing nodes
    for node in LK_diff_nodes:
      if node not in dangling_nodes:
        self.debug_print([('removing node', LG_mapping[node])])
        H.remove_node(LG_mapping[node])
      else:
        self.debug_print([('node not removed due to dangling condition', LG_mapping[node])])
        return None

    ### H = D union (R \ K)
    # Difference between R and K
    RK_diff_nodes, RK_diff_edges = self.diff(self.R, self.K, self.inverse_mapping(self.KR_mapping))

    # Adding nodes
    for node in RK_diff_nodes:
      H.add_node(node)
      if self.labelled:
        H.nodes[node]['attr'] = self.R.nodes[node]['attr']
      self.debug_print([('Added node to H', node)])
    
    # Nodes in G that are mapped in R, via G -> L -> R
    GL_mapping = self.inverse_mapping(LG_mapping)
    GLR_mapping = {}
    for node in G:
      if node in GL_mapping and GL_mapping[node] in self.LR_mapping:
        GLR_mapping[node] = self.LR_mapping[GL_mapping[node]]
    # Nodes in R that are mapped in G, via R -> L -> G
    RLG_mapping = self.inverse_mapping(GLR_mapping)

    # Add new edges from R edges to H
    for (u, v) in RK_diff_edges:
      source = RLG_mapping[u] if u not in RK_diff_nodes else u
      target = RLG_mapping[v] if v not in RK_diff_nodes else v
      H.add_edge(source, target)
      if self.labelled:
        H.edges[source, target]['attr'] = self.R.edges[u, v]['attr']
        self.debug_print([('Added edge to H', [(source, target), H.edges[source, target]['attr']])])
      else:
        self.debug_print([('Added edge to H', (source, target))])

    # Glue edges from G onto R
    for (u, v) in G.edges:
      if u in GLR_mapping and v not in GLR_mapping:
        if GLR_mapping[u] in RK_diff_nodes:
          H.add_edge(GLR_mapping[u], v)
          if self.labelled:
            H.edges[GLR_mapping[u], v]['attr'] = G.edges[u, v]['attr']
            self.debug_print([('Added edge to H', [(GLR_mapping[u], v), H.edges[GLR_mapping[u], v]['attr']])])
          else:
            self.debug_print([('Added edge to H', (GLR_mapping[u], v))])
      if u not in GLR_mapping and v in GLR_mapping:
        if GLR_mapping[v] in RK_diff_nodes:
          H.add_edge(u, GLR_mapping[v])
          if self.labelled:
            H.edges[u, GLR_mapping[v]]['attr'] = G.edges[u, v]['attr']
            self.debug_print([('Added edge to H', [(u, GLR_mapping[v]), H.edges[u, GLR_mapping[v]]['attr']])])
          else:
            self.debug_print([('Added edge to H', (u, GLR_mapping[v]))])

    # Relabeling nodes in H to avoid conflicting names with R,
    # when chaining graph transformations
    if self.relabel:
      relabel_dict = {node: f'{node}_{self.name[0]}{self.name[-1]}' for node in H.nodes}
      H = nx.relabel_nodes(H, relabel_dict)

    if self.labelled:
      self.debug_print([('H.nodes', nx.get_node_attributes(H, name='attr'))])
      self.debug_print([('H.edges', nx.get_edge_attributes(H, name='attr'))])
    else:
      self.debug_print([('H.nodes', H.nodes)])
      self.debug_print([('H.edges', H.edges)])

    return H
  

  """
  Perform all transformations from production L -> K <- R on G,
  From all possible mappings of L onto G
  """
  def perform_all_transformations(self, G):
    LG_mappings = self.possible_LG_mappings(G)
    output_graphs = []
    for mapping in LG_mappings:
      H = self.perform_transformation(G, mapping)
      if H != None:
        output_graphs.append(H)

    return output_graphs


  """
  Finds nodes that cause dangling conditions
  """
  def dangling_nodes(self, L, G, LG_mapping):
    diff_nodes, diff_edges = self.diff(G, L, self.inverse_mapping(LG_mapping))
    dangling_nodes = set()
    for node in [v for v in L.nodes if v not in self.LR_mapping]:  # Nodes that get removed
      for (v,u) in diff_edges:
        if LG_mapping[node] == v or LG_mapping[node] == u:
          dangling_nodes.add(node)
    if len(dangling_nodes) > 0:
      self.debug_print([('dangling_nodes', dangling_nodes)])

    return dangling_nodes


  """
  Returns two sets, V vertices, E edges
  V = (V_A \ V_B)
  E = (E_A \ E_B)
  """
  def diff(self, A, B, AB_mapping):
    self.debug_print(f'diff: {A.name}, {B.name}', title=True)
    self.debug_print([(f'{A.name}.nodes', A.nodes),(f'{A.name}.edges', A.edges)]+[(f'{A.name}{edge}', A.edges[edge]) for edge in A.edges])
    self.debug_print([(f'{B.name}.nodes', B.nodes),(f'{B.name}.edges', B.edges)]+[(f'{B.name}{edge}', B.edges[edge]) for edge in B.edges])

    # Since we want diff = A \ B, we start of with A
    # Nodes
    diff_nodes = nx.get_node_attributes(A, name='attr')
    if len(diff_nodes) == 0:
      diff_nodes = {node: '' for node in A.nodes}
    for u in A.nodes:
      if u in AB_mapping and A.nodes[u] == B.nodes[AB_mapping[u]]:
        diff_nodes.pop(u)

    # Edges
    translated_edges = self.translate_edges(A, AB_mapping)
    diff_edges = nx.get_edge_attributes(A, name='attr')
    if len(diff_edges) == 0:
      diff_edges = {edge: '' for edge in A.edges}
    for edge in A.edges:
      if edge in translated_edges and translated_edges[edge] in B.edges:
        if A.edges[edge] == B.edges[translated_edges[edge]]:
          diff_edges.pop(edge)

    self.debug_print([('diff_nodes', diff_nodes), ('diff_edges', diff_edges)]+[(f'diff_{A.name}_{B.name} edge {edge}', diff_edges[edge]) for edge in diff_edges])

    return diff_nodes, diff_edges


  """
  Automatically maps nodes from L to R,
  assuming mapped nodes have the same index in both graphs
  Assuming the indecies of the NX graph has names than can be compared, so names are of same type
  """
  def auto_mapping(self):
    self.debug_print('Auto mapping', title=True)
    mapping = {l: r for l in self.L.nodes for r in self.R.nodes if l==r}
    self.debug_print([('Mapping', mapping)])

    return mapping


  """
  For each edge in source (u, v), translate to the equivalent edge in target.
  Namely the edge: ( mapping(u), mapping(v) )
  """
  def translate_edges(self, source, mapping):
    translated_edges = {}
    # Edge structure: (node_v, node_u)
    for (u, v) in source.edges:
      if u in mapping and v in mapping:
        translated_edges[u, v] = (mapping[u], mapping[v])

    return translated_edges


  """
  Create the inverse mapping from a mapping
  """
  def inverse_mapping(self, AB_mapping):
    BA_mapping = {}
    for source in AB_mapping:
      target = AB_mapping[source]
      BA_mapping[target] = source

    return BA_mapping


  """
  Use matplotlib to show production rule graphically
  """
  def show_prod(self):
    #plt.rcParams["axes.edgecolor"] = "0.15"
    #plt.rcParams["axes.linewidth"]  = 1.25
    fig, axes = plt.subplots(nrows=1, ncols=3)
    ax = axes.flatten()

    # Get graph data
    gs = {}
    gs['L'] = {'graph': self.L,
               'pos': nx.get_node_attributes(self.L, name='pos')}
    gs['K'] = {'graph': self.K,
               'pos': nx.get_node_attributes(self.L, name='pos')}
    gs['R'] = {'graph': self.R,
               'pos': nx.get_node_attributes(self.R, name='pos')}

    # Draw graph nodes and edges
    for i, g in enumerate(gs):
      if len(nx.get_node_attributes(gs[g]['graph'], name='attr')) > 0:
        labels={node: f"{gs[g]['graph'].nodes[node]['attr']} ({node})" for node in gs[g]['graph'].nodes}
      else:
        labels={node: node for node in gs[g]['graph'].nodes}

      nx.draw_networkx(
        gs[g]['graph'], pos=gs[g]['pos'], edge_color='black', width=1, linewidths=1,
        ax=ax[i], node_size=500, node_color='pink', alpha=0.9, labels=labels, label=gs[g]['graph'].name)

      nx.draw_networkx_edge_labels(
              gs[g]['graph'], pos=gs[g]['pos'], 
              edge_labels=nx.get_edge_attributes(gs[g]['graph'], name='attr'),
              font_color='red')

    plt.show()


  """
  Use matplotlib to show Networkx graph
  """
  def show_graph(self, G):
    pos = nx.spring_layout(G)
    plt.figure()
    labels={}
    if self.labelled:
      labels={node: f"{G.nodes[node]['attr']}" for node in G.nodes()}
    nx.draw(
      G, pos,edge_color='black',width=1, linewidths=1,
      node_size=500, node_color='pink', alpha=0.9,
      labels=labels)
    nx.draw_networkx_edge_labels(
            G, pos, 
            edge_labels=nx.get_edge_attributes(G, name='attr'),
            font_color='red')
    plt.axis('off')
    plt.show()


  """
  Used to assert that the LR mapping is a valid mapping.
  A valid map is where all keys in the dict have a single value, all values are unique.
  """
  def validate_mapping(self):
    keys   = self.LR_mapping.keys()
    values = self.LR_mapping.values()
    assert len(values) == len(set(values)), "All mappings, must map to a unique node"
    assert all([k in list(self.L.nodes)] for k in keys), "Node in mapping not present in L"
    assert all([v in list(self.R.nodes)] for v in values), "Node in mapping not present in R"

  """
  Prints debug information
  """
  def debug_print(self, msgs, title=False):
    if self.debug:
      if title:
        print('+' + '-' * len(msgs) + '+')
        print('|' + msgs + '|')
        print('+' + '-' * len(msgs) + '+')
      else:
        for (desc, info) in msgs:
          print((desc + ':'), str(info))

  def __str__(self):
    return self.name
