import random
import math
import copy
import sys
import re
import linecache
import time
import csv

class genetic():
    def __init__(self, vertices, name):
        self.data_set_name = name
        self.original_dataset = vertices
        self.vertices = {}
        self.tours = []
        self.best_tour = {
            'best' : [],
            'distance' : sys.float_info.max
        }

        # Cities Setup
        self.line_num = 0  # For the city selection
        self.shuffleCities()

        for point in vertices:
            self.vertices[point[0]] = {
                "point":(point[1], point[2]),
                "id":point[0],
                "city":self.getNextCity()
        }

        # File output
        self.init_temp = 10
        cooldown_schedule = "temp -= .5"

        # Open output file, init the header
        self.init_print_output(self.init_temp, cooldown_schedule)

        self.init_tours()
        self.genetic_algo()

    def init_tours(self):
        # Basic 1-5 tour
        first_tour = []
        for key in self.vertices:
            node = self.vertices[key]
            first_tour.append(copy.deepcopy(node))
        self.tours.append(copy.deepcopy(first_tour))
        
        ten_percent = int(len(self.vertices)/10)
        for i in range(1, ten_percent):
            population_keys = random.sample(range(1, len(self.vertices)+1), len(self.vertices))
            print('pop keys:', population_keys)
            temp_tour = []
            for j in population_keys:
                temp_tour.append(copy.deepcopy(self.vertices[j]))
            self.tours.append(copy.deepcopy(temp_tour))
            temp_tour = []
    
    def genetic_algo(self):
        # File opens
        results = open('/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/genetic/output/output.txt', 'a+')
        curve = open('/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/genetic/output/curve.csv', 'w+')
        writer = csv.writer(curve)
        writer.writerow(['Iteration', 'Distance'])
        
        temp = self.init_temp  # Stopping criteria
        iteration = 0
        while temp > 0:
            # Get best tour
            best_tour_results : list = self.find_best_tour()
            if self.best_tour['distance'] > best_tour_results[1]:
                self.best_tour['best'] = copy.deepcopy(best_tour_results[0])
                self.best_tour['distance'] = best_tour_results[1]

            # File output
            writer.writerow([iteration, best_tour_results[1]])
            results.write(
                        '\n***\n'
                        'Iteration: '+str(iteration)+
                        '\nTemp: '+str(temp)+
                        '\nCurrent Distance: '+str(best_tour_results[1]))
            
            # Breed a new population with the crossover algorithm
            new_tours = []
            new_tours.append(copy.deepcopy(best_tour_results[0]))
            while len(new_tours) <= int(len(self.vertices)/10):
                new_tour = self.crossover(best_tour_results[0])
                # 10% chance of mutation
                if random.random() <= 0.1:
                    results.write('\nMutation Accepted')
                    new_tour = copy.deepcopy(self.mutate(new_tour))
                new_tours.append(copy.deepcopy(new_tour))
            
            print('Best Distance this round:',best_tour_results[1])
            print('Temp:',temp)
            
            # Copy to instance
            self.tours = copy.deepcopy(new_tours)

            # Cooling schedule
            # temp = temp - (1/math.log(iteration+2))
            temp = temp - 0.5
            iteration += 1
        
        # Once temp == 0, find best solution
        best_tour_results : list = self.find_best_tour()
        if self.best_tour['distance'] > best_tour_results[1]:
            self.best_tour['best'] = copy.deepcopy(best_tour_results[0])
            self.best_tour['distance'] = best_tour_results[1]
        results.close()
        self.print_path_output(self.best_tour['best'], self.best_tour['distance'])
        
        print('\nDistance: ', self.best_tour['distance'])
        curve.close()

    # Calculates the best tour, returns a copy of the tour list and the best distance
    def find_best_tour(self):
        best_distance = sys.float_info.max
        best_tour = None
        for tour in self.tours:
            this_distance = self.calculate_path_distance(tour)
            if this_distance < best_distance:
                best_distance = this_distance
                best_tour = copy.deepcopy(tour)
        return [copy.deepcopy(best_tour), best_distance]
    
    # Mutation helper method. Returns n tours, n being 10% of the number of cities
    def mutate(self, tour):
        # Swap Mutation (swap two elements)
        num_cities = len(self.vertices)

        # Switch variables
        tour_copy = copy.deepcopy(tour)
        switch_1 = random.randint(0, num_cities)
        switch_2 = random.randint(0, num_cities)
        while (switch_1 == switch_2):
            switch_1 = random.randint(0, num_cities)
            switch_2 = random.randint(0, num_cities)
                
        # Switch Nodes
        node_copy = copy.deepcopy(tour_copy[switch_1-1])
        tour_copy[switch_1-1] = copy.deepcopy(tour_copy[switch_2-1])
        tour_copy[switch_2-1] = node_copy
       
        return tour_copy

    # Crossover helper method. Takes a random i to k range of the provided tour and returns
    # a new tour with this range and filler cities between 0 and n not between i and k
    def crossover(self, tour):
        begin = random.randint(0, len(tour))
        end = random.randint(0, len(tour))
        while begin == end or begin > end:
            begin = random.randint(0, len(tour))
            end = random.randint(0, len(tour))
        crossover_range = range(begin, end+1)
        crossover_index = 0
        new_tour = []
        visited = []
        for i in range(0,len(tour)):
            if (i in crossover_range):
                new_tour.append(copy.deepcopy(tour[crossover_range[crossover_index]]))
                crossover_index += 1
            else:
                while True:
                    random_index = random.randint(0,len(tour)-1)
                    if (random_index not in crossover_range):
                        temp_city = copy.deepcopy(tour[random_index])
                        if temp_city not in visited:
                            new_tour.append(copy.deepcopy(temp_city))
                            visited.append(copy.deepcopy(temp_city))
                            break
        return new_tour
        
    def calculate_path_distance(self, tour):
        distance = 0
        l = len(tour)
        for index, node in enumerate(tour):
            if (index + 1 != l):
                next_node = tour[index+1]
            else:
                next_node = tour[0]            
            distance += self.calculateDistance(node['point'], next_node['point'])
        return distance

    def calculateDistance(self, point1 : tuple, point2 : tuple):
        x = math.pow(point2[0] - point1[0], 2)
        y = math.pow(point2[1] - point1[1], 2)
        distance = math.sqrt(x + y)
        return distance

    # City generation
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
    
    # Shuffles the city dataset to give a new city list for each program run
    def shuffleCities(self):
        fid = open("/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/datasets/world-cities_csv.csv", "r")
        li = fid.readlines()
        fid.close()
        random.shuffle(li)
        fid = open("/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/datasets/world-cities_shuffle.csv", "w")
        fid.writelines(li)
        fid.close()

    # inits the file output, creates file if it does not exist
    def init_print_output(self, temp, cooldown_schedule):
        results = open('/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/genetic/output/output.txt', 'w+')
        results.write("## TSP OUTPUT FILE - GENETIC ALGORITHM ##\n")
        results.write('Dataset Name: '+self.data_set_name+'\n')
        results.write('Initial Temp: '+str(temp)+'\n')
        results.write('Cooldown Schedule: '+cooldown_schedule+'\n')
        results.write('Number of Initial Tours: '+ str(len(self.tours)))

    # Prints result path
    def print_path_output(self, tour, total_distance):
        results = open('/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/genetic/output/output.txt', 'a+')
        results.write('\n\n\n### RESULT ###\n')
        l = len(tour)
        for index, city in enumerate(tour):
            if (index + 1 != l):
                next_node = tour[index+1]
            else:
                next_node = tour[0]            
            distance = self.calculateDistance(city['point'], next_node['point'])
            results.write('\n')
            results.write(city['city']+ " --> "+next_node['city']+'         Distance of: '+ str(distance))
        results.write('\nFinished with final distance: '+str(total_distance))

# Parses file provided by assignment
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

data = parse_file('/Users/brice/Desktop/Classes/COMP361/Assignment4/tsp-algorithms/datasets/a280.tsp.txt')
genetic = genetic(data[0], data[1])