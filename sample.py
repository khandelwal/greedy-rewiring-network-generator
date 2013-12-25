from greedy_rewiring import undirectedgraph
from greedy_rewiring import greedy_rewiring as greedy

# This sample illustrates how to use the greedy rewiring code. 

if __name__ == "__main__":
    adjacency_list = undirectedgraph.read_edge_list(
        'random_regular_graph_mean8_N1000.txt')

    graph = undirectedgraph.UndirectedGraph(adjacency_list)
    rewired_graph = greedy.anyNodeAnyNeighborProbabilisticRewiring(graph, '1')
    rewired_graph.writeGraph('output.txt')
