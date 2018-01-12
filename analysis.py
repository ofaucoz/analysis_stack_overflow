#!/usr/bin/python

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

graph = nx.Graph(day="stack-overflow")

# get nodes and edges
nodes = pd.read_csv('stack_network_nodes.csv')
edges = pd.read_csv('stack_network_links.csv')

# retrieve nodes and edges into graph
for index, row in nodes.iterrows():
    graph.add_node(row['name'], group=row['group'], nodesize=row['nodesize'])

for index, row in edges.iterrows():
    graph.add_weighted_edges_from([(row['source'], row['target'], row['value'])])

color_map = {1:'#f09494', 2:'#eebcbc', 3:'#72bbd0', 4:'#91f0a1', 5:'#629fff', 6:'#bcc2f2',
             7:'#eebcbc', 8:'#f1f0c0', 9:'#d2ffe7', 10:'#caf3a6', 11:'#ffdf55', 12:'#ef77aa',
             13:'#d6dcff', 14:'#d2f5f0'}

plt.figure(figsize=(25,25))
options = {
    'edge_color': '#FFDEA2',
    'width': 1,
    'with_labels': True,
    'font_weight': 'regular',
}

colors = [color_map[graph.node[node]['group']] for node in graph]
sizes = [graph.node[node]['nodesize']*9 for node in graph]

nx.draw(graph, node_color=colors, node_size=sizes, pos=nx.spring_layout(graph, k=1, iterations=100), **options)
ax = plt.gca()
ax.collections[0].set_edgecolor("#555555")
plt.show()