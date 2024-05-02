def calculatePath(start, finish, parentSet):
    currentNode = finish
    path = []

    while currentNode != start:
        path.append(currentNode)
        currentNode = parentSet[currentNode]
    path.append(start)

    return path[::-1]


def pathInLatLon(graph: list, path: list):
    pathLatLon = ""
    for node in path:
        if type(node) is not int:
            pathLatLon += "(" + str(node.lat) + " " + str(node.lon) + ")"
        else:
            pathLatLon += (
                "("
                + str(graph[node].lat / 1000000)
                + " "
                + str(graph[node].lon / 1000000)
                + ")"
            )
    return pathLatLon
