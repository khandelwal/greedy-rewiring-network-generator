#!/usr/bin/python

from array import array


class UndirectedGraph:
    """ An undirected graph """

    def __init__(self, inputGraphFileName):
        self.adjList = {}
        self.populateGraph(inputGraphFileName)

    def populateGraph(self, graphFile):
        """ Populate the graph data structure from a file. """

        f = open(graphFile)
        for line in f:
            line = line.split(":", 1)
            node = int(line[0])

            neighborList = line[1:][0]
            neighborList = neighborList.replace("\n", '')
            neighborList = neighborList.split(",")
            neighborList = filter(self.filterInts, neighborList)
            neighborList = map(self.convertToInt, neighborList)

            #Later we might have to write a more complicated
            #parser, since this assumes that the file is well formed.
            #i.e. if (1,2) is in the file, then (2,1) is also in the file.
            neighborArray = array('l', neighborList)
            self.adjList[node] = neighborArray

    def writeDegrees(self, fileName):
        """ Write out the degree for each node """

        #degFile = open(fileName,"w")
        degFile = open(fileName, 'a')
        for node in self.adjList:
            #degFile.write(
            #    repr(node) + " " + repr(self.getNodeDegree(node)) + "\n")
            degFile.write(repr(self.getNodeDegree(node)) + " ")

            degFile.write("\n")
        degFile.close()

    def writeDegreeDist(self, fileName):
        """ Write out the degree distribution to a file """
        degDistFile = open(fileName, "w")

        degreeDist = {}
        #Go through graph, building the degree distribution
        for node in self.adjList:
            degree = self.getNodeDegree(node)

            if degree in degreeDist:
                degreeDist[degree] += 1
            else:
                degreeDist[degree] = 1

        #print out the degree distribution
        for x in degreeDist.items():
            degDistFile.write(repr(x[0]) + " " + repr(x[1]) + "\n")

    def writeGraph(self, fileName):
        """ Write the graph to fileName. """
        f = open(fileName, 'w')

        f.write("digraph G {")

        for node in self.adjList:
            neighborArray = map(repr, self.adjList[node])
            for neighbor in neighborArray:
                f.write(repr(node) + "->" + neighbor + ";\n")
        f.write("}")

    def printGraph(self):
        """ Print out the graph """

        for node in self.adjList:
            neighborArray = map(repr, self.adjList[node])
            neighbors = ",".join(neighborArray)
            print repr(node) + ": " + neighbors

    def getNodeDegree(self, node):
        return array.buffer_info(self.adjList[node])[1]

    def getNeighborDegreeList(self, node):
        """ For node, get a list of (neighbor, degree) tuples """
        neighborList = self.adjList[node]
        degreeTuples = map(self.getNodeDegreeTuple, neighborList)
        return degreeTuples

    def getNodeDegreeListForWholeGraph(self):
        """ For the entire graph get the (node, degree) tuples """
        listOfAllNodes = self.getListOfNodes()
        degreeTuples = map(self.getNodeDegreeTuple, listOfAllNodes)
        return degreeTuples

    def getNodeDegreeTuple(self, node):
        """ Return (node, degree) """
        return (node, self.getNodeDegree(node))

    def getListOfNodes(self):
        "Return a list of all the nodes in the graph"
        return self.adjList.keys()

    def addEdge(self, x, y):
        xList = self.adjList[x]
        #Don't add an edge that's already there.
        #Don't add an edge to itself.
        if (xList.count(y) < 1) and (x != y):
            xList.append(y)
            yList = self.adjList[y]
            yList.append(x)

            self.adjList[x] = xList
            self.adjList[y] = yList
            return True
        else:
            return False

    def removeEdge(self, x, y):
        xList = self.adjList[x]
        if (xList.count(y) == 1):
            xList.remove(y)
            yList = self.adjList[y]
            yList.remove(x)

            self.adjList[x] = xList
            self.adjList[y] = yList
            return True
        else:
            return False

    #PRIVATE METHODS
    def filterInts(self, x):
        """ Remove non-integers from a list of strings """
        x = x.strip()
        if x.isdigit():
            return True
        else:
            return False

    def convertToInt(self, x):
        """ Convert string to integer, stripping whitespace first """
        x = x.strip()
        return int(x)
