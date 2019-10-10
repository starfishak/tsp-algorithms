import random
import linecache
import re
import math
import copy
import csv

class tsp():
    def __init__(self, vertices, name):
        self.data_set_name = name
        self.original_dataset = vertices
        self.vertices = {}
        self.tour = []
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
            self.tour.append(current_node)

    def calculate_path_distance(self):
        distance = 0
        l = len(self.tour)
        for index, node in enumerate(self.tour):
            if (index + 1 != l):
                next_node = self.tour[index+1]
            else:
                next_node = self.tour[0]            
            distance += self.calculateDistance(node['point'], next_node['point'])
        return distance

    def calculateDistance(self, point1 : tuple, point2 : tuple):
        x = math.pow(point2[0] - point1[0], 2)
        y = math.pow(point2[1] - point1[1], 2)
        distance = math.sqrt(x + y)
        return distance
    
    def simulated_annealing(self):
        # Simulation Definitions
        temp = 50
        iteration = 0
        num_cities = len(self.vertices)
        current_distance = self.calculate_path_distance()
        cooldown_schedule = "temp -= 1/log(iteration+2)"

        # Open output file, init the header
        self.init_print_output(temp, cooldown_schedule)
        results = open('./output/output.txt', 'a+')
        curve = open('./output/curve.csv', 'w+')
        writer = csv.writer(curve)
        writer.writerow(['Iteration', 'Distance'])

        # While the temp is > 0
        while temp >= 0:
            # print current iteration information
            results.write('\n***\n'
                        'Iteration: '+str(iteration)+
                        '\nTemp: '+str(temp)+
                        '\nCurrent Distance: '+str(current_distance))

            # Write to curve csv
            writer.writerow([iteration, current_distance])

            # Make copy of current path incase we reject the new path
            path_copy = copy.deepcopy(self.tour)


            # Generate our random switch indexes, ensure they are not equal
            switch_1 = random.randint(1, num_cities)
            switch_2 = random.randint(1, num_cities)
            while (switch_2 == switch_1):
                switch_1 = random.randint(1, num_cities)
                switch_2 = random.randint(1, num_cities)
            results.write('\nSwitch indexs ' + str(switch_1) + ' and ' + str(switch_2))
            
            # Switch Nodes
            node_copy = copy.deepcopy(self.tour[switch_1-1])
            self.tour[switch_1-1] = copy.deepcopy(self.tour[switch_2-1])
            self.tour[switch_2-1] = node_copy
            new_distance = self.calculate_path_distance()

            # Check distance sizes
            if (new_distance > current_distance):
                # Probability we reject it
                replace_path = self.replace_path(temp, current_distance, new_distance)
                results.write('\nNew path is longer'+
                              '\nProbability We Accept:'+str(replace_path[0]))
                if not replace_path[1]:
                    results.write('\nPath Rejected')
                    self.tour = copy.deepcopy(path_copy)
                else:
                    current_distance = new_distance
                    results.write('\nPath Accepted\nNew Distance:'+str(new_distance))
            
            temp = temp - (1/math.log(iteration+2))/2
            results.write('\nCooldown: ' + str((1/math.log(iteration+2))/2))
            iteration += 1
        results.write('\n\n\nComplete\nBest found distance:'+str(current_distance))
        print("done")
        print(current_distance)
        results.close()
        

    # Returns True if switch 1 comes first, false is switch 2 comes first
    def sequence_order(self, switch_1, switch_2):
        for key in self.vertices:
            val = self.vertices[key]
            if val['id'] == switch_1:
                return True
            elif val['id'] == switch_2:
                return False

    def replace_path(self, tempature, l1, l2):
        probability = math.exp((l1-l2)/tempature)
        print("Prob", probability, "\t replace_path", random.random() < probability)
        return [probability,random.random() < probability]

    def edge_print(self):
        for val in self.tour:
            print(val['id'], val['city'])

    def getNextCity(self):
        # Choose some random number between 1 and 20000
        if (self.line_num == 0):
            self.line_num = random.randint(1, 20000)
        city_data = linecache.getline('../datasets/world-cities_shuffle.csv', self.line_num)
        city_list = city_data.strip().split(',')
        if (city_list[1] != 'United States'):
            self.line_num+=1
            return self.getNextCity()
        self.line_num+=1
        return city_list[0]
    
    def shuffleCities(self):
        fid = open("../datasets/world-cities_csv.csv", "r")
        li = fid.readlines()
        fid.close()
        random.shuffle(li)
        fid = open("../world-cities_shuffle.csv", "w")
        fid.writelines(li)
        fid.close()

    def init_print_output(self,temp, cooldown_schedule):
        results = open('./output/output.txt', 'w+')
        results.write("## TSP OUTPUT FILE - LOCAL SEARCH ##\n")
        results.write('Initial Temp: '+str(temp)+'\n')
        results.write('Cooldown Schedule: '+cooldown_schedule+'\n')
        start_city = self.tour[0]['city']
        results.write(self.data_set_name+"Start City: "+ start_city+'\n')

    def print_path_output(self):
        results = open('./output/output.txt', 'a+')
        results.write('\n\n\n### RESULT ###\n')
        l = len(self.tour)
        for index, city in enumerate(self.tour):
            if (index + 1 != l):
                next_node = self.tour[index+1]
            else:
                next_node = self.tour[0]            
            distance = self.calculateDistance(city['point'], next_node['point'])
            results.write('\n')
            results.write(city['city']+ " --> "+next_node['city']+'         Distance of: '+ str(distance))

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

data = parse_file('../datasets/berlin52.tsp.txt')
tsp = tsp(data[0], data[1])
print(tsp.calculate_path_distance())
print(tsp.vertices)
tsp.simulated_annealing()
tsp.print_path_output()