from math import sqrt, cos, radians, sin, atan2

def calculateDistanceBetweenNodes(node1, node2):
    return abs(
        int(
            sqrt(
                ((node1.lat - node2.lat) * (node1.lat - node2.lat))
                + ((node1.lon - node2.lon) * (node1.lon - node2.lon))
            ).real
        )
    )

def haversineDistance(node1, node2):
    lat1 = radians(node1.lat) / 1000000
    lon1 = radians(node1.lon) / 1000000
    lat2 = radians(node2.lat) / 1000000
    lon2 = radians(node2.lon) / 1000000

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6371
    distance = R * c

    return distance

