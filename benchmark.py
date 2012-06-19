#! /usr/bin/env python

from collections import deque, defaultdict
import utilities
import time
import cPickle as pickle
from operator import itemgetter

def naive_search(graph, node, num_nodes):
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
    if not neighbors:
        return visited
    
    small_graph = dict((k, graph[k]) for k in neighbors)
    listofallpossibilities = []
    for every_n, every_ns_n in small_graph.iteritems():
        listofallpossibilities.extend(every_ns_n)

    for every_possible_candidate in listofallpossibilities:
        ranked_list[every_possible_candidate] +=  1
    
    if node in ranked_list:
        del ranked_list[node]
    
    for neighbor in neighbors:
        if neighbor in ranked_list:
            del ranked_list[neighbor]
        
    sorted_list = sorted(ranked_list.items(), key=itemgetter(1), reverse=True)
    k = num_nodes
    for i,j in sorted_list:
        if k > 0:
            visited.append(i)
            k = k - 1
        
    return visited

def find_possible_candidates(small_graph, node):
    possible_candidates = set() 
    for key,val in small_graph.iteritems():
        possible_candidates = possible_candidates.union(val)
    possible_candidates.discard(node)
    return possible_candidates
    
def naive_benchmark(train_file, test_file, submission_file, num_predictions):
    """
    Runs the breadth-first search benchmark.
    """
    
    # Skipping making graph, loading from file instead
    pkl_file = open('graph.pkl', 'rb')
    graph = pickle.load(pkl_file)
    pkl_file.close()
    # graph = utilities.read_graph(train_file)
    test_nodes = utilities.read_nodes_list(test_file)
    start_time = time.time()
    test_predictions = [naive_search(graph, node, num_predictions)
                        for node in test_nodes]
    
    print time.time() - start_time, "seconds"

    utilities.write_submission_file(submission_file, 
                                    test_nodes, 
                                    test_predictions)
    
    
if __name__=="__main__":
    naive_benchmark("../Data/train.csv",
                  "../Data/test.csv",
                  "../Submissions/naive_benchmark.csv",
                  10)
