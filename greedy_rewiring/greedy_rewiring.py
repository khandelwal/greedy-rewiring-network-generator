#!/usr/bin/python

from undirectedgraph import UndirectedGraph
from random import randint


def compareNeighborTuples(x, y):
    return x[1] - y[1]


def getHighestDegreeNeighbor(neighborsTuples):
    neighborsTuples.sort(compareNeighborTuples)
    return neighborsTuples.pop()[0]


def getLowestDegreeNeighbor(neighborTuples):
    neighborTuples.sort(compareNeighborTuples)

    #Get the lowest degree neighbor, who doesn't have
    #degree 1.
    for n in neighborTuples:
        if (n[1] > 1):
            lowestDegreeNeighbor = n[0]
            return lowestDegreeNeighbor
    return None


def getLowestDegreeNeighborProb(neighborTuples):
    neighborTuples.sort(compareNeighborTuples)

    nonDegreeOneNeighbors = []

    for n in neighborTuples:
        if (n[1] > 1):
            nonDegreeOneNeighbors.append(n)

    nonDegreeOneNeighbors.sort(compareNeighborTuples)

    #Add up all the degrees of the neighbors
    sumOfDegrees = reduce(lambda a, b: a + b[1], nonDegreeOneNeighbors, 0)

    randomSelector = randint(1, sumOfDegrees)

    degSum = 0
    chosenTuple = None
    i = 0
    while (degSum < randomSelector):
        tuple = nonDegreeOneNeighbors[i]
        degSum += tuple[1]
        chosenTuple = tuple
        i += 1

    return chosenTuple[0]


def greedyRewiring(graph):
    "Implementation of the Bansal Greedy Rewiring Algorithm: Version 1"
    nodes = graph.getListOfNodes()

    numRewirings = 0

    for node in nodes:
        neighborsTuples = graph.getNeighborDegreeList(node)
        lowestDegNeighbor = getLowestDegreeNeighbor(neighborsTuples)

        if (lowestDegNeighbor is not None):
            #get the highest degree node for this node
            lowestDegNeighborList = graph.getNeighborDegreeList(
                lowestDegNeighbor)
            #highestDegNeighbor = getHighestDegreeNeighbor(
                #lowestDegNeighborList);

            highestDegreeTuples = lowestDegNeighborList
            highestDegreeTuples.sort(compareNeighborTuples)
            highestDegreeTuples.reverse()

            for highestDegTuple in highestDegreeTuples:
                highestDegNeighbor = highestDegTuple[0]
                success = graph.addEdge(node, highestDegNeighbor)
                if (success):
                    graph.removeEdge(node, lowestDegNeighbor)
                    numRewirings += 1
                    break

    print "num rewirings: " + repr(numRewirings)
    return graph


def probabilisticGreedyRewiring(graph):
    nodes = graph.getListOfNodes()
    numRewirings = 0

    for node in nodes:
        #Get a list of neighbors and their degrees
        neighborsTuples = graph.getNeighborDegreeList(node)

        #Find the lowest degree neighbor (who doesn't have degree 1)
        lowestDegNeighbor = getLowestDegreeNeighbor(neighborsTuples)

        if (lowestDegNeighbor is not None):
            #Get all the neighbors for the lowest degree neighbor
            lowestDegNeighborList = graph.getNeighborDegreeList(
                lowestDegNeighbor)

            #From that list, find a node to rewire the original node to.
            highestDegreeTuples = lowestDegNeighborList
            highestDegreeTuples.sort(compareNeighborTuples)
            highestDegreeTuples.reverse()

            #Add up all the degrees of the neighbors
            sumOfDegrees = reduce(
                lambda a, b: a + b[1], highestDegreeTuples, 0)

            rewired = False
            while ((not rewired) and (len(highestDegreeTuples) > 0)):
                randomSelector = randint(1, sumOfDegrees)

                degSum = 0
                chosenTuple = None
                i = 0
                while (degSum < randomSelector):
                    tuple = highestDegreeTuples[i]
                    degSum += tuple[1]
                    chosenTuple = tuple
                    i += 1

                rewired = graph.addEdge(node, chosenTuple[0])
                if (rewired):
                    graph.removeEdge(node, lowestDegNeighbor)
                    numRewirings += 1
                else:
                    sumOfDegrees -= chosenTuple[1]
                    highestDegreeTuples.remove(chosenTuple)

    print "num rewirings: " + repr(numRewirings)
    return graph


def anyNeighborProbabilisticRewiring(graph):
    nodes = graph.getListOfNodes()
    numRewirings = 0

    for node in nodes:
        #Get a list of neighbors and their degrees
        neighborsTuples = graph.getNeighborDegreeList(node)

        #Pick a neighbor randomly.
        randomIndex = randint(0, len(neighborsTuples) - 1)
        lowestDegNeighbor = neighborsTuples[randomIndex][0]

        #Find the lowest degree neighbor (who doesn't have degree 1)
        #lowestDegNeighbor = getLowestDegreeNeighbor(neighborsTuples);

        if (lowestDegNeighbor is not None):
            #Get all the neighbors for the lowest degree neighbor
            lowestDegNeighborList = graph.getNeighborDegreeList(
                lowestDegNeighbor)

            #From that list, find a node to rewire the original node to.
            highestDegreeTuples = lowestDegNeighborList
            highestDegreeTuples.sort(compareNeighborTuples)
            highestDegreeTuples.reverse()

            #Add up all the degrees of the neighbors
            sumOfDegrees = reduce(
                lambda a, b: a + b[1], highestDegreeTuples, 0)

            rewired = False
            while ((not rewired) and (len(highestDegreeTuples) > 0)):
                randomSelector = randint(1, sumOfDegrees)

                degSum = 0
                chosenTuple = None
                i = 0
                while (degSum < randomSelector):
                    tuple = highestDegreeTuples[i]
                    degSum += tuple[1]
                    chosenTuple = tuple
                    i += 1

                rewired = graph.addEdge(node, chosenTuple[0])
                if (rewired):
                    graph.removeEdge(node, lowestDegNeighbor)
                    numRewirings += 1
                else:
                    sumOfDegrees -= chosenTuple[1]
                    highestDegreeTuples.remove(chosenTuple)

    print "num rewirings: " + repr(numRewirings)
    return graph


def anyNodeAnyNeighborProbabilisticRewiring(graph, sbk):
    nodes = graph.getListOfNodes()
    nodeAndDegreeTuples = graph.getNodeDegreeListForWholeGraph()
    numRewirings = 0

    wholeGraphSumOfDegrees = reduce(
        lambda a, b: a + b[1], nodeAndDegreeTuples, 0)

    numEdgesInGraph = wholeGraphSumOfDegrees/2

    print "i = " + repr(sbk) + " num edges in graph: " + repr(numEdgesInGraph)

    #for node in nodes:
    while (numRewirings < 15 * numEdgesInGraph):

        #print "num rewirings: " + repr(numRewirings);

        #pick a bale of cotton, pick a random node.
        randomNodeIndex = randint(0, len(nodeAndDegreeTuples) - 1)
        node = nodeAndDegreeTuples[randomNodeIndex][0]

        #Get a list of neighbors and their degrees
        neighborsTuples = graph.getNeighborDegreeList(node)

        #Pick a neighbor randomly.
        #randomIndex = randint(0, len(neighborsTuples) - 1);
        #lowestDegNeighbor = neighborsTuples[randomIndex][0];

        #Find the lowest degree neighbor (who doesn't have degree 1)
        #lowestDegNeighbor = getLowestDegreeNeighbor(neighborsTuples);

        # Find lowest deg neighbor (deg > 1), probabilistically
        lowestDegNeighbor = getLowestDegreeNeighborProb(neighborsTuples)

        if (lowestDegNeighbor is not None):
            #Get all the neighbors for the lowest degree neighbor
            lowestDegNeighborList = graph.getNeighborDegreeList(
                lowestDegNeighbor)

            #From that list, find a node to rewire the original node to.
            highestDegreeTuples = lowestDegNeighborList
            highestDegreeTuples.sort(compareNeighborTuples)
            highestDegreeTuples.reverse()

            #Add up all the degrees of the neighbors
            sumOfDegrees = reduce(
                lambda a, b: a + b[1], highestDegreeTuples, 0)

            sumOfDegrees_all = numEdgesInGraph * 2

            rewired = False
            while ((not rewired) and (len(highestDegreeTuples) > 0)):
                randomSelector = randint(1, sumOfDegrees)

                degSum = 0
                chosenTuple = None
                i = 0
                while (degSum < randomSelector):
                    tuple = highestDegreeTuples[i]
                    degSum += tuple[1]
                    chosenTuple = tuple
                    i += 1

                rewired = graph.addEdge(node, chosenTuple[0])
                if (rewired):
                    graph.removeEdge(node, lowestDegNeighbor)
                    numRewirings += 1

                    #print degreelist at each rewiring step
                    #graph.writeDegrees(
                        #"degrees_" + repr(numRewirings) + ".txt");
                    graph.writeDegrees("degrees_" + repr(sbk) + ".txt")
                else:
                    sumOfDegrees -= chosenTuple[1]
                    highestDegreeTuples.remove(chosenTuple)

    print "num rewirings: " + repr(numRewirings)
    return graph

#EXECUTION BLOCK

for sbk in range(10, 11):

    readGraph = UndirectedGraph('neighReg_1k/neighlistReg_' + repr(sbk))
    rewiredGraph = readGraph
    originalGraph = rewiredGraph
    originalGraph.writeDegrees("degrees_" + repr(sbk) + ".txt")
    #originalGraph.writeGraph("graph_" + repr(sbk))
    rewiredGraph = anyNodeAnyNeighborProbabilisticRewiring(originalGraph, sbk)

#readGraph.writeDegreeDist('deg_dist.txt');
#readGraph.writeDegrees("degrees.txt");

#run the greedy rewiring algorithm a few times on the same graph.
#for x in range(1, 16):

#rewiredGraph = greedyRewiring(originalGraph);
#rewiredGraph = anyNeighborProbabilisticRewiring(originalGraph);


#rewiredGraph.writeGraph("rewired_graph_" + repr(x) + ".txt");
#rewiredGraph.writeGraph("rewired_graph_" + ".txt");
#rewiredGraph.writeDegreeDist("deg_dist_" + repr(x) + ".txt");
#rewiredGraph.writeDegrees("degrees_" + repr(x) + ".txt");
