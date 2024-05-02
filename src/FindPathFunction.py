from operator import attrgetter, itemgetter
from time import perf_counter
from psutil import Process
from src.HeuristicDistanceFunctions import (
    haversineDistance,
    calculateDistanceBetweenNodes,
)
from src.CalculatePathFunctions import calculatePath


def depthFirstSearch(graph: list, start: int, end: int, timeLimitSeconds):
    startTime = perf_counter()
    startMemory = Process().memory_info().rss

    queuedNodes = [start]
    visitedNodes = set()
    nodeParent = {}
    path = []
    expandedNodes = 0

    while queuedNodes is not []:
        if perf_counter() - startTime > timeLimitSeconds:
            return (
                [],
                expandedNodes,
                Process().memory_info().rss - startMemory,
                perf_counter() - startTime,
                "Breadth First Search",
            )

        currentNode = queuedNodes.pop(0)
        expandedNodes += 1
        visitedNodes.add(currentNode)

        if currentNode == end:
            break

        for connectedNode in graph[currentNode].connectedNodes:
            if connectedNode[0] not in visitedNodes:
                queuedNodes.append(connectedNode[0])
                nodeParent[connectedNode[0]] = currentNode

    if end not in nodeParent:
        return (
            [],
            expandedNodes,
            Process().memory_info().rss - startMemory,
            perf_counter() - startTime,
            "Breadth First Search",
        )

    return (
        calculatePath(start, end, nodeParent),
        expandedNodes,
        Process().memory_info().rss - startMemory,
        perf_counter() - startTime,
        "Breadth First Search",
    )


def breadthFirstSearch(graph: list, start: int, end: int, timeLimitSeconds=120):
    startTime = perf_counter()
    startMemory = Process().memory_info().rss

    path = []
    visitedNodes = set()
    nodeParent = {}
    stackedNodes = [start]
    expandedNodes = 0

    while stackedNodes:
        if perf_counter() - startTime > timeLimitSeconds:
            return (
                [],
                expandedNodes,
                Process().memory_info().rss - startMemory,
                perf_counter() - startTime,
                "Depth First Search",
            )
        currentNode = stackedNodes.pop()
        expandedNodes += 1

        if currentNode == end:
            break

        for connectedNode in graph[currentNode].connectedNodes:
            if connectedNode[0] not in visitedNodes:
                stackedNodes.append(connectedNode[0])
                visitedNodes.add(currentNode)
                nodeParent[connectedNode[0]] = currentNode

    if end not in nodeParent:
        return (
            [],
            expandedNodes,
            Process().memory_info().rss - startMemory,
            perf_counter() - startTime,
            "Depth First Search",
        )

    return (
        calculatePath(start, end, nodeParent),
        expandedNodes,
        Process().memory_info().rss - startMemory,
        perf_counter() - startTime,
        "Depth First Search",
    )


def bestFirstSearch(graph: list, start: int, end: int, timeLimitSeconds=120):
    startTime = perf_counter()
    startMemory = Process().memory_info().rss

    queuedNodes = [(graph[start], 0)]
    visitedNodes = set()
    nodeParent = {}
    expandedNodes = 0

    while queuedNodes is not []:
        if perf_counter() - startTime > timeLimitSeconds:
            return (
                [],
                expandedNodes,
                Process().memory_info().rss - startMemory,
                perf_counter() - startTime,
                "Best First Search",
            )

        nodeTupple = queuedNodes.pop(0)
        node = nodeTupple[0]
        nodeCost = nodeTupple[1]
        visitedNodes.add(node.value)
        expandedNodes += 1

        if node.value == end:
            break

        for connectedNodeTuple in node.connectedNodes:
            connectedNode = graph[connectedNodeTuple[0]]
            connectedNodeCost = connectedNodeTuple[1]
            if (
                connectedNodeTuple[0] not in visitedNodes
                and connectedNode not in queuedNodes
            ):
                queuedNodes.append((connectedNode, connectedNodeCost))
                nodeParent[connectedNode.value] = node.value
        queuedNodes.sort(key=itemgetter(1))

    if end not in nodeParent:
        return (
            [],
            expandedNodes,
            Process().memory_info().rss - startMemory,
            perf_counter() - startTime,
            "Best First Search",
        )

    return (
        calculatePath(start, end, nodeParent),
        expandedNodes,
        Process().memory_info().rss - startMemory,
        perf_counter() - startTime,
        "Best First Search",
    )


def aStarDBNH(graph: list, start: int, end: int, timeLimitSeconds=120):
    startTime = perf_counter()
    startMemory = Process().memory_info().rss

    visitedNodes = set()
    queuedNodes = [graph[start]]
    endNode = graph[end]
    nodeParent = {}
    expandedNodes = 0

    while queuedNodes is not []:
        currentNode = queuedNodes.pop(0)
        visitedNodes.add(currentNode.value)
        expandedNodes += 1
        if currentNode.value == end:
            break

        for connectedNodeTuple in currentNode.connectedNodes:
            connectedNode = graph[connectedNodeTuple[0]]
            if (
                connectedNodeTuple[0] not in visitedNodes
                and connectedNode not in queuedNodes
            ):
                queuedNodes.append(connectedNode)
                nodeParent[connectedNode.value] = currentNode.value
                connectedNode.distHeuristic = (
                    calculateDistanceBetweenNodes(endNode, connectedNode)
                )

        queuedNodes.sort(key=attrgetter("distHeuristic"))

    if end not in nodeParent:
        return (
            [],
            expandedNodes,
            Process().memory_info().rss - startMemory,
            perf_counter() - startTime,
            "A* DBNH",
        )

    return (
        calculatePath(start, end, nodeParent),
        expandedNodes,
        Process().memory_info().rss - startMemory,
        perf_counter() - startTime,
        "A* DBNH",
    )


def aStarHaversine(graph: list, start: int, end: int, timeLimitSeconds=120):
    startTime = perf_counter()
    startMemory = Process().memory_info().rss

    visitedNodes = set()
    queuedNodes = [graph[start]]
    endNode = graph[end]
    nodeParent = {}
    expandedNodes = 0

    while queuedNodes is not []:
        currentNode = queuedNodes.pop(0)
        visitedNodes.add(currentNode.value)
        expandedNodes += 1
        if currentNode.value == end:
            break

        for connectedNodeTuple in currentNode.connectedNodes:
            connectedNode = graph[connectedNodeTuple[0]]
            if (
                connectedNodeTuple[0] not in visitedNodes
                and connectedNode not in queuedNodes
            ):
                queuedNodes.append(connectedNode)
                nodeParent[connectedNode.value] = currentNode.value
                connectedNode.distHeuristic = (
                    haversineDistance(endNode, connectedNode)
                )

        queuedNodes.sort(key=attrgetter("distHeuristic"))

    if end not in nodeParent:
        return (
            [],
            expandedNodes,
            Process().memory_info().rss - startMemory,
            perf_counter() - startTime,
            "A* Haversine",
        )

    return (
        calculatePath(start, end, nodeParent),
        expandedNodes,
        Process().memory_info().rss - startMemory,
        perf_counter() - startTime,
        "A* Haversine",
    )
