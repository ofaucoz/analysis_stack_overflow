#!/usr/bin/python

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def create_graph():
	graph = nx.Graph(day="stack-overflow")

	# get nodes and edges
	nodes = pd.read_csv('stack_network_nodes.csv')
	edges = pd.read_csv('stack_network_links.csv')

	# retrieve nodes and edges into graph
	for index, row in nodes.iterrows():
	    graph.add_node(row['name'], group=row['group'], nodesize=row['nodesize'])

	for index, row in edges.iterrows():
	    graph.add_weighted_edges_from([(row['source'], row['target'], row['value'])])
	return graph

def plot_graph(graph):
	color_map = {1:'#f09494', 2:'#eebcbc', 3:'#72bbd0', 4:'#91f0a1', 5:'#629fff', 6:'#bcc2f2',
	             7:'#eebcbc', 8:'#f1f0c0', 9:'#d2ffe7', 10:'#caf3a6', 11:'#ffdf55', 12:'#ef77aa',
	             13:'#d6dcff', 14:'#d2f5f0'}

	plt.figure(figsize=(25,25))
	options = {
	    'edge_color': '#66ccff',
	    'width': 2,
	    'with_labels': True,
	    'font_weight': 'regular',
	}

	colors = [color_map[graph.node[node]['group']] for node in graph]
	sizes = [graph.node[node]['nodesize']*9 for node in graph]

	nx.draw(graph, node_color=colors, node_size=sizes, pos=nx.spring_layout(graph, k=1, iterations=100),
		node_shape="p", alpha=0.8, **options)
	ax = plt.gca()
	ax.collections[0].set_edgecolor("#444444")
	plt.show()

def compute_average_path(graph):
	spl = nx.all_pairs_shortest_path_length(graph)
	number_edges = 0
	sum = 0
	for node1 in spl:
		for node2 in dict(spl[node1]):
			number_edges += 1
			sum += spl[node1][node2]
	average = sum / number_edges
	return average

def degree_distribution(graph):
	list_degree = {}
	list_name_degree = {}
	for node in graph:
		degree = graph.degree(node)
		if degree not in list_degree:
			list_degree[degree] = 0
			list_name_degree[degree] = []
		list_degree[degree] += 1
		list_name_degree[degree].append(node)
	plt.bar(list(list_degree.keys()), list_degree.values(), color='g')
	plt.show()
	return list_name_degree

def degree_log(graph):
	degree_sequence=sorted(dict(nx.degree(graph)).values(),reverse=True) # degree sequence
	#print "Degree sequence", degree_sequence
	dmax=max(degree_sequence)

	plt.loglog(degree_sequence,'b-',marker='o')
	plt.title("Distribution of degree(log)")
	plt.ylabel("fraction")
	plt.xlabel("degree")

	# draw graph in inset
	plt.axes([0.45,0.45,0.45,0.45])
	Gcc=sorted(nx.connected_component_subgraphs(graph), key = len, reverse=True)[0]
	pos=nx.spring_layout(Gcc)
	plt.axis('off')
	nx.draw_networkx_nodes(Gcc,pos,node_size=20)
	nx.draw_networkx_edges(Gcc,pos,alpha=0.4)

	plt.savefig("degree_histogram.png")
	plt.show()


graph = create_graph()
#plot_graph(graph)
#print "compute_average_path : " + str(compute_average_path(graph))
#print "degree_distribution : " + str(degree_distribution(graph))
degree_log(graph)

