#! /usr/bin/env python

from collections import deque, defaultdict
import utilities
import time
import cPickle as pickle
from operator import itemgetter

def naive_search(graph, reversegraph, node, num_nodes):
    """
    Does a breadth-first search of the graph starting at the node.
    Returns the first num_nodes nodes (excluding direct neighbors)
    """
    # ranked_list = defaultdict(lambda: 0)
    ranked_list = defaultdict(int)
    visited = []
    # node contains me
    # neighbors contain my neighbors
    neighbors = set(graph[node])
    
    # Missing neighbors from reversegraph
    if node in reversegraph:
        visited = reversegraph[node]
    
    for neighbor in neighbors:
        if neighbor in visited:
            visited.remove(neighbor) 
    
    if not neighbors:
        neighbors = set(visited)
    
    if neighbors:
        small_graph = dict((k, graph[k]) for k in neighbors)
        listofallpossibilities = [item for sublist in small_graph.values() for item in sublist]

        for every_possible_candidate in listofallpossibilities:
            ranked_list[every_possible_candidate] +=  1
        
        if node in ranked_list:
            del ranked_list[node]
        
        for neighbor in neighbors:
            if neighbor in ranked_list:
                del ranked_list[neighbor]
            
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
    
def naive_benchmark(train_file, test_file, submission_file, num_predictions):
    """
    Runs the breadth-first search benchmark.
    """

    start_time = time.time()
    (graph, reversegraph) = utilities.read_graph(train_file)
    print "Graph forming time = ", time.time() - start_time, "seconds"
    start_time = time.time()
    test_nodes = utilities.read_nodes_list(test_file)
    test_predictions = [naive_search(graph, reversegraph, node, num_predictions)
                        for node in test_nodes]
    print "Prediction time = ", time.time() - start_time, "seconds"
    

    utilities.write_submission_file(submission_file, 
                                    test_nodes, 
                                    test_predictions)
    
    
if __name__=="__main__":
    naive_benchmark("../Data/train.csv",
                  "../Data/test.csv",
                  "../Submissions/missinglinks_rankedlist_bothways.csv",
                  10)
