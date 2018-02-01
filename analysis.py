#!/usr/bin/python

import community
import networkx as nx
import matplotlib.pyplot as plt


def create_graph():
	#graph = nx.Graph(day="stack-overflow")

	# get nodes and edges
	graph = nx.read_gml('polblogs.gml')
	# edges = pd.read_csv('stack_network_links.csv')

	# # retrieve nodes and edges into graph
	# for index, row in nodes.iterrows():
	#     graph.add_node(row['name'], group=row['group'], nodesize=row['nodesize'])

	# for index, row in edges.iterrows():
	#     graph.add_weighted_edges_from([(row['source'], row['target'], row['value'])])
	return graph

def plot_graph(graph):
	# color_map = {1:'#f09494', 2:'#eebcbc', 3:'#72bbd0', 4:'#91f0a1', 5:'#629fff', 6:'#bcc2f2',
	#              7:'#eebcbc', 8:'#f1f0c0', 9:'#d2ffe7', 10:'#caf3a6', 11:'#ffdf55', 12:'#ef77aa',
	#              13:'#d6dcff', 14:'#d2f5f0'}

	plt.figure(figsize=(25,25))
	options = {
	    'edge_color': '#66ccff',
	    'width': 2,
	    'with_labels': True,
	    'font_weight': 'regular',
	}

	#colors = [color_map[graph.node[node]['group']] for node in graph]
	#sizes = [graph.node[node]['nodesize']*9 for node in graph]

	nx.draw(graph, pos=nx.spring_layout(graph, k=1, iterations=100),
		node_shape="p", alpha=0.8, **options)
	ax = plt.gca()
	ax.collections[0].set_edgecolor("#444444")
	plt.show()

def distance_measures(G):
	print "center : " + str(nx.center(G)) + ", diameter : " + str(nx.diamter(G)) + ", eccentricity : " + str()

def compute_average_path(graph):
	spl = nx.all_pairs_shortest_path_length(graph)
	flag = True
	current_node = spl.next()
	number_edges = 0
	sum = 0
	while(flag != False):	
		node = current_node[0]
		#print "node : " + str(node)
		dictio = current_node[1]
		#print "dictio : " + str(dictio)		
		for node2 in dictio:
			number_edges += 1
			sum += dictio[node2]
		current_node = next(spl, None)
		if current_node is None:
			flag = False
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
	# plt.axes([0.45,0.45,0.45,0.45])
	

	plt.savefig("degree_histogram.png")
	plt.show()

def communities(G):
	partition = community.best_partition(G)
	float(len(set(partition.values())))
	list_modularity = list()
	for part in set(partition.values()):
		list_modularity.append(community.modularity(part, G))
	return sorted(list_modularity)[10]

def centrality_degree(G):
	degree_centrality = sorted(nx.degree_centrality(G).values(), reverse=True)
	plt.loglog(degree_centrality,'b-',marker='o')
	plt.title("Distribution of nodes centrality")
	plt.ylabel("fraction")
	plt.xlabel("centrality")
	plt.savefig("centrality_nodes_histogram.png")
	plt.savefig("centrality.png")
	plt.show()
	print "degree centrality : " + str(degree_centrality)

def closeness_centrality(G):
	closeness_centrality = nx.closeness_centrality(G)
	print closeness_centrality
	print "best nodes : " + str(sorted(closeness_centrality.values())[:5])
	plt.bar(list(closeness_centrality.keys()), list(closeness_centrality.values()), color='g')
	plt.show()

def betweeness_centrality(G):
	betweeness_centrality = nx.betweenness_centrality(G)
	print betweeness_centrality
	print "best nodes : " + str(sorted(betweeness_centrality.values(), reverse=True)[:5])
	plt.bar(list(betweeness_centrality.keys()), list(betweeness_centrality.values()), color='g')
	plt.show()

def eigenvector_centrality(G):
	eigenvector_centrality = nx.eigenvector_centrality(G)
	print eigenvector_centrality
	print "best nodes : " + str(sorted(eigenvector_centrality.values(), reverse=True)[:5])
	plt.bar(list(eigenvector_centrality.keys()), list(eigenvector_centrality.values()), color='g')
	plt.show()

def pagerank(G):
	pagerank = nx.pagerank(G)
	print pagerank
	print "best nodes : " + str(sorted(pagerank.values(), reverse=True)[:5])
	plt.bar(list(pagerank.keys()), list(pagerank.values()), color='g')
	plt.show()

def clustering(G):
	clustering_coeff = nx.average_clustering(G)
	print "clustering coeff : " + str(clustering_coeff)

def local_clustering(G):
	Y = nx.Graph()
	for u,v,data in G.edges(data=True):
		w = data['weight'] if 'weight' in data else 1.0
	if Y.has_edge(u,v):
		Y[u][v]['weight'] += w
	else:
		Y.add_edge(u, v, weight=w)
	local_clustering = sorted(nx.clustering(Y).values(), reverse=True)
	dmax=max(local_clustering)

	plt.loglog(local_clustering,'b-',marker='o')
	plt.title("Distribution of clustering(log)")
	plt.ylabel("fraction")
	plt.xlabel("degree")

	# draw graph in inset
	#plt.savefig("degree_histogram.png")
	plt.show()

graph = create_graph()
graph = graph.to_undirected()
#plot_graph(graph)
#print "compute_average_path : " + str(compute_average_path(graph)) # result : 3
#print "degree_distribution : " + str(degree_distribution(graph))
#degree_log(graph)
#print communities(graph) : 268 communities, but with 2 particular ones
#centrality_degree(graph)
#closeness_centrality(graph)
#betweeness_centrality(graph)
#eigenvector_centrality(graph)
#pagerank(graph)
#clustering(graph)
#local_clustering(graph)
#print "number of edges : " + str(len(graph.node))

# TODO : components, clustering
# dataset on political bloggers, analyse the discussion between both liberal and conservative party
