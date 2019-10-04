import math # for distance calculation
import re
import random
import linecache

class Graph():
    def __init__(self, vertices, name):
        self.data_set_name = name
        self.original_dataset = vertices
        self.vertices = {}
        self.visited = {}
        self.total_distance = 0

        # Cities Setup
        self.line_num = 0  # For the city selection
        self.shuffleCities()
        
        for point in vertices:
            self.vertices[point[0]] = {
                "point":(point[1], point[2]),
                "edges":[],
                "id":point[0],
                "city":self.getNextCity()
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
                self.distances[key] = distance
        
        # Find Shortest Key
        if (len(self.distances) == 0):
            # 0 Distances, therefore graph is complete
            return
        min_key = min(self.distances, key=lambda k: self.distances[k]) 
        node = self.vertices.get(min_key)
        current_point['edges'].append((min_key, self.distances[min_key]))
        self.visited[min_key] = node
        self.distances = {}
        self.prims(node)


    def calculateDistance(self, point1 : tuple, point2 : tuple):
        x = math.pow(point2[0] - point1[0], 2)
        y = math.pow(point2[1] - point1[1], 2)
        distance = math.sqrt(x + y)
        return distance

    def tsp_init(self):
            results = open('/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/mst-heuristic/output/output.txt', 'w+')
            results.write("## TSP OUTPUT FILE - APPROXIMATION ALGORITHM ##\n")
            print("\n\nTSP")
            prior_city = self.vertices[1]['city']
            results.write(self.data_set_name+"Start City: "+ prior_city+'\n')
            print("\nStart City: ", prior_city)
            results.close()
            self.tsp(self.vertices[1]['edges'][0], prior_city)

    def tsp(self, node, prior_city):
        results = open('/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/mst-heuristic/output/output.txt', 'a+')
        node_id = node[0]
        distance = node[1]
        self.total_distance += distance
        city = self.vertices[node_id]['city']
        results.write('\n')
        results.write(prior_city+ " --> "+city+'         Distance of:'+ str(distance))
        print('\n'+prior_city+ " --> "+city+'         Distance of:'+ str(distance))
        if (len(self.vertices[node_id]['edges']) > 0):
            results.close()
            self.tsp(self.vertices[node_id]['edges'][0], city)
        else:
            results.close()
            self.end_tsp(self.vertices[node_id])

    def end_tsp(self, prior_city_node):
        with open('/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/mst-heuristic/output/output.txt', 'a+') as results:
            home_node = self.vertices[1]
            distance = self.calculateDistance(home_node['point'], prior_city_node['point'])
            self.total_distance += distance
            results.write('\n'+prior_city_node['city']+ " --> "+home_node['city']+'         Distance of:'+ str(distance)+'\n')
            results.write('\nEnd of Tour! Total Distance of: '+str(self.total_distance))
            print(prior_city_node['city'], "-->",home_node['city'],'         Distance of:', distance,'\n')
            print('End of Tour! Total Distance of: ',self.total_distance,'\n')

    def printMST(self):
        for element in self.vertices:
            print(element['edges'])

    def getNextCity(self):
        # Choose some random number between 1 and 20000
        if (self.line_num == 0):
            self.line_num = random.randint(1, 20000)
        city_data = linecache.getline('/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/datasets/world-cities_shuffle.csv', self.line_num)
        city_list = city_data.strip().split(',')
        print(city_list[1])
        if (city_list[1] != 'United States'):
            self.line_num+=1
            return self.getNextCity()
        self.line_num+=1
        return city_list[0]
    
    def shuffleCities(self):
        fid = open("/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/datasets/world-cities_csv.csv", "r")
        li = fid.readlines()
        fid.close()
        random.shuffle(li)
        fid = open("/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/datasets/world-cities_shuffle.csv", "w")
        fid.writelines(li)
        fid.close()

def parse_file(path):
    with open(path) as file:
        points = []
        for line in file:
            if ("NAME" in line):
                name = line
            if (not re.search('[a-zA-Z]', line)):
                this_line = line.strip().split(' ')
                this_line = list(filter(None, this_line))
                this_line = [ int(x) for x in this_line ]
                print(this_line)
                points.append(this_line)
        return (points, name)


data = parse_file('/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/datasets/kroB200.tsp.txt')
graph = Graph(data[0], data[1])
graph.tsp_init()