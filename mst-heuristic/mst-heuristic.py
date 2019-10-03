import math # for distance calculation
import re

class Graph():
    def __init__(self, vertices):
        self.original_dataset = vertices
        self.vertices = {}
        self.visited = {}
        for point in vertices:
            self.vertices[point[0]] = {
                "point":(point[1], point[2]),
                "edges":[],
                "id":point[0]
            }
        self.visited[1] = self.vertices[1]
        self.prims(self.vertices[1])

    def prims(self, current_point):
        # Calculate all distances
        self.distances = {}
        for key in self.vertices:
            val = self.vertices[key]
            if (key not in self.visited):
                distance = self.calculateDistance(current_point['point'], val['point'])
                # print(distance)
                self.distances[key] = distance
        
        # Find Shortest Key
        if (len(self.distances) == 0):
            # 0 Distances, therefore graph is complete
            return
        min_key = min(self.distances, key=lambda k: self.distances[k]) 
        node = self.vertices.get(min_key)
        current_point['edges'].append(min_key)
        self.visited[min_key] = node
        self.prims(node)


    def calculateDistance(self, point1 : tuple, point2 : tuple):
        x = math.pow(point2[0] - point1[0], 2)
        y = math.pow(point2[1] - point1[1], 2)
        distance = math.sqrt(x + y)
        return distance

    def tsp(self):
        

    def printMST(self):
        for element in self.vertices:
            print(element['edges'])

def parse_file(path):
    with open(path) as file:
        points = []
        for line in file:
            if (not re.search('[a-zA-Z]', line)):
                this_line = line.strip().split(' ')
                this_line = list(filter(None, this_line))
                this_line = [ int(x) for x in this_line ]
                print(this_line)
                points.append(this_line)
        return points

# points = [  [1, 1, 1], 
#             [2, 4, 1], 
#             [3, 1, 4], 
#             [4, 3, 4], 
#             [5, 5, 3]] 
# points = [  [1, 1, 1], 
#             [2, 1, 3], 
#             [3, 2, 2], 
#             [4, 3, 2], 
#             [5, 3, 4],
#             [6, 5, 3],
#             [7, 5, 1],
#             [8, 4, 1],
#             [9, 6, 7]] 

points = parse_file('/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/datasets/a280.tsp.txt')

graph = Graph(points)
# graph.printMST()
