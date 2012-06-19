#! /usr/bin/env python

from collections import deque, defaultdict
import utilities
import time
import cPickle as pickle
from operator import itemgetter

def jaccard_search(graph, reversegraph, node, num_nodes):
    """
    Does a breadth-first search of the graph starting at the node.
    Returns the first num_nodes nodes (excluding direct neighbors)
    """
    # ranked_list = defaultdict(lambda: 0)
    ranked_list = defaultdict(int)
    visited = []
    childrenKnown = 0
    # node contains me
    # neighbors contain my children
    neighbors = set(graph[node])
    if neighbors:
        childrenKnown = 1
    # Missing neighbors from reversegraph
    if node in reversegraph:
        visited = reversegraph[node]
    
    for neighbor in neighbors:
        if neighbor in visited:
            visited.remove(neighbor)

    # visited has my parents, neighbors has my children
    # if not neighbors:
    parents = set(visited)
    neighbors = neighbors | parents
    
    small_graph = dict((k, graph[k]) for k in neighbors)
    friendsoffriends = [item for sublist in small_graph.values() for item in sublist]
    friendsoffriendslist = friendsoffriends
    friendsoffriends = set(friendsoffriends) - neighbors
    friendsoffriends = friendsoffriends
    if childrenKnown:
        for everyfof in friendsoffriends:
            fofneighbors = set(graph[everyfof])
            numerator = len(fofneighbors & neighbors)
            if numerator > 0:
                ranked_list[everyfof] =  numerator / len(fofneighbors | neighbors)
                
    else:
        for every_possible_candidate in friendsoffriendslist:
            ranked_list[every_possible_candidate] +=  1

        for neighbor in neighbors:
            if neighbor in ranked_list:
                del ranked_list[neighbor]
        
    if node in ranked_list:
        del ranked_list[node]
        
    sorted_list = sorted(ranked_list.items(), key=itemgetter(1), reverse=True)

    for i,j in sorted_list:
        if len(visited)<num_nodes:
            visited.append(i)

    ulist = []
    [ulist.append(x) for x in visited if x not in ulist]
    return ulist

def loadgraphfrompickle(filename):
    pkl_file = open(filename, 'rb')
    graph = pickle.load(pkl_file)
    pkl_file.close()
    return graph
    
def jaccard_benchmark(train_file, test_file, submission_file, num_predictions):
    """
    Runs the breadth-first search benchmark.
    """

    start_time = time.time()
    (graph, reversegraph) = utilities.read_graph(train_file)
    print "Graph forming time = ", time.time() - start_time, "seconds"
    start_time = time.time()
    test_nodes = utilities.read_nodes_list(test_file)
    test_predictions = [jaccard_search(graph, reversegraph, node, num_predictions)
                        for node in test_nodes]
    
    print "Prediction time = ", time.time() - start_time, "seconds"

    utilities.write_submission_file(submission_file, 
                                    test_nodes, 
                                    test_predictions)
    
    
if __name__=="__main__":
    jaccard_benchmark("../Data/train.csv",
                  "../Data/test.csv",
                  "../Submissions/jaccard_benchmark_bothways.csv",
                  10)
