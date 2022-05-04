import networkx as nx
from community import community_louvain
import os
import time

def computeShortestPathLength(G):
    paths = []
    for C in nx.connected_components(G):
        paths.append(round(nx.average_shortest_path_length(G.subgraph(C) ), 4))
    return round(sum(paths) / len(paths), 4)

def computeClusteringCoefficent(G):
    coeffs = []
    for C in nx.connected_components(G):
        coeffs.append(round(nx.average_clustering(G.subgraph(C) ), 4))
    return round(sum(coeffs) / len(coeffs), 4)

def readFile(filename):
    print("Results for graph {}: ".format(filename))
    G = nx.Graph()

    start = time.time()

    with open(filename) as networkData:
        next(networkData)       
        for line in networkData:
            row = line.split()
            head = row[1]
            source = row[2]
            target = row[3]
            edgeWeight = float(row[4])
            G.add_node(source)
            G.add_node(target)
            if G.has_edge(source, target):
                G[source][target]['weight'] = float((G[source][target]['weight'] + (edgeWeight)) / 2)
            else:
                G.add_edge(target, source, weight=edgeWeight)

        community = community_louvain.best_partition(G)
        denoGraph = community_louvain.generate_dendrogram(G.subgraph(community))
        modularities = []
        highestModularity, highestLevel = 0,0
        for level in range(len(denoGraph)) :
            thisLevel = community_louvain.partition_at_level(denoGraph, level)
            thisModularity = round(community_louvain.modularity(thisLevel, G), 4)
            modularities.append((level, thisModularity))
            if thisModularity > highestModularity:
                highestModularity, highestLevel = thisModularity, level
        end = time.time()
        time2Complete = round(end - start, 4)
        print(" -This Graph took {} seconds to compute".format(time2Complete))
        print(" -This Graph has {} levels in its hierarchical decomposition".format(len(denoGraph)))
        print(" -This Graph has the largest modularity at level {}, which is {}".format(highestLevel, highestModularity))
        for item in modularities:
            print(" -Level", item[0], "has a modularity of", item[1])
        
def main():
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".txt"):
            readFile(filename)
            continue
        else:
            continue

main()