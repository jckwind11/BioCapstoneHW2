import networkx as nx
from community import community_louvain
import os
import time

def readFile(filename):
    start = time.time()
    print("Results for graph {}: ".format(filename))
    G = nx.Graph()

    with open(filename) as networkData:
        next(networkData)
        for line in networkData:
            row = line.split()
            tail = row[0]
            head = row[1]
            edgeWeight = row[2]
            G.add_edge(tail, head, weight=edgeWeight)

        for _,_,d in G.edges(data=True):
            d['weight'] = float(d['weight'])
        
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
