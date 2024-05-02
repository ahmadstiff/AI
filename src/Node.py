class Node:
    def __init__(self, value):
        self.value = value
        self.connectedNodes = []
        self.distHeuristic = 0
        self.lat = 0
        self.lon = 0
        
    def addConnection(self, connection):
        if connection not in self.connectedNodes:
            self.connectedNodes.append(connection)
            
    def doesConnectionExist(self, connection):
        return connection in self.connectedNodes
    
    def __lt__(self, other):
        return self.distHeuristic < other.distHeuristic 
    