import random
import linecache
import re
import math
import copy

class tsp():
    def __init__(self, vertices, name):
        self.data_set_name = name
        self.original_dataset = vertices
        self.vertices = {}
        self.current_path = {}

        # Cities Setup
        self.line_num = 0  # For the city selection
        self.shuffleCities()
        
        for point in vertices:
            self.vertices[point[0]] = {
                "point":(point[1], point[2]),
                "edges":[],
                "prior":[],
                "id":point[0],
                "city":self.getNextCity()
            }
        self.init_path()

    def init_path(self):
        for key in self.vertices:
            current_node = self.vertices[key]
            if key + 1 in self.vertices:
                next_node = self.vertices[key + 1]
            else:
                next_node = self.vertices[1]
            current_node['edges'].append(next_node['id'])
            next_node['prior'].append(key)

    def calculate_path_distance(self):
        distance = 0
        for key in self.vertices:
            current_node = self.vertices[key]
            next_node = self.vertices[current_node['edges'][0]]
            distance += self.calculateDistance(current_node['point'], next_node['point'])
        return distance

    def calculateDistance(self, point1 : tuple, point2 : tuple):
        x = math.pow(point2[0] - point1[0], 2)
        y = math.pow(point2[1] - point1[1], 2)
        distance = math.sqrt(x + y)
        return distance
    
    def simulated_annealing(self):
        temp = 5
        itertion = 0
        num_cities = len(self.vertices)
        current_distance = self.calculate_path_distance()
        self.edge_print()
        # 1/log(step)
        while temp >= 0:
            print('\nTemp',temp)
            print('Cur Distance', current_distance)
            path_copy = copy.deepcopy(self.vertices)
            switch_1 = random.randint(1, num_cities)
            switch_2 = random.randint(1, num_cities)
            while switch_2 == switch_1:
                switch_2 = random.randint(1, num_cities)
            print(switch_1, switch_2)
            self.vertices[self.vertices[switch_1]['prior'][0]]['edges'] = [switch_2]
            self.vertices[self.vertices[switch_2]['prior'][0]]['edges'] = [switch_1]
            s1_edges_copy = copy.deepcopy(self.vertices[switch_1]['edges'])
            s2_edges_copy = copy.deepcopy(self.vertices[switch_2]['edges'])
            s1_prior_copy = copy.deepcopy(self.vertices[switch_1]['prior'])
            s2_prior_copy = copy.deepcopy(self.vertices[switch_2]['prior'])
            self.vertices[switch_2]['edges'] = s1_edges_copy
            self.vertices[switch_1]['edges'] = s2_edges_copy
            self.vertices[switch_2]['prior'] = s2_prior_copy
            self.vertices[switch_1]['prior'] = s1_prior_copy
            self.edge_print()
            new_distance = self.calculate_path_distance()
            if (new_distance > current_distance):
                # probability we reject it
                replace_path = self.replace_path(temp, current_distance, new_distance)
                if not replace_path:
                    self.vertices = copy.deepcopy(path_copy)
                else:
                    current_distance = new_distance
            temp = temp - (1/math.log(itertion+2))/2
            itertion += 1
        
        print("done")
        print(self.vertices)
        print(current_distance)

    def replace_path(self, tempature, l1, l2):
        probability = math.exp((l1-l2)/tempature)
        print("Prob", probability, "\t replace_path", random.random() < probability)
        return random.random() < probability

    def edge_print(self):
        for key in self.vertices:
            val = self.vertices[key]
            print(val['id'],val['prior'],val['edges'])

    def getNextCity(self):
        # Choose some random number between 1 and 20000
        if (self.line_num == 0):
            self.line_num = random.randint(1, 20000)
        city_data = linecache.getline('/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/datasets/world-cities_shuffle.csv', self.line_num)
        city_list = city_data.strip().split(',')
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



data = parse_file('/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/datasets/test.txt')
tsp = tsp(data[0], data[1])
print(tsp.calculate_path_distance())
print(tsp.vertices)
tsp.simulated_annealing()
