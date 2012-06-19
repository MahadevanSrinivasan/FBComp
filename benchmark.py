#! /usr/bin/env python

from collections import deque
import utilities
from operator import itemgetter

def naive_search(graph, node, num_nodes):
    """
    Does a breadth-first search of the graph starting at the node.
    Returns the first num_nodes nodes (excluding direct neighbors)
    """
    ranked_list = {}
    visited = []
    # node contains me
    # neighbors contain my neighbors
    neighbors = set(graph[node])
    small_graph = dict((k,v) for k,v in graph.iteritems() if k in neighbors)
    print small_graph
    raw_input('Press any key')
    if not neighbors:
        return visited
    # Iterate through every element of graph
    for element, elem_neighbors in small_graph.iteritems():
        # Skip if it's the node or its neighbors otherwise compute common elements
        if node != element and element not in neighbors:
            no_common_elements = len(neighbors.intersection(elem_neighbors))
            if no_common_elements:
                ranked_list[element] = no_common_elements
    sorted_list = sorted(ranked_list.items(), key=itemgetter(1), reverse=True)
    k = num_nodes
    for i,j in sorted_list:
        if k > 0:
            visited.append(i)
            k = k - 1
    return visited

    
def naive_benchmark(train_file, test_file, submission_file, num_predictions):
    """
    Runs the breadth-first search benchmark.
    """
    graph = utilities.read_graph(train_file)
    test_nodes = utilities.read_nodes_list(test_file)
    test_predictions = [naive_search(graph, node, num_predictions)
                        for node in test_nodes]
    utilities.write_submission_file(submission_file, 
                                    test_nodes, 
                                    test_predictions)

if __name__=="__main__":
    naive_benchmark("../Data/train.csv",
                  "../Data/smalltest.csv",
                  "../Submissions/naive_benchmark.csv",
                  10)
