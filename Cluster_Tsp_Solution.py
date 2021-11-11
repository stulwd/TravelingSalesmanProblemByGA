# 1. Discuss if the start and the end city are given. So instead of finishing at where he started, his last location
#    should be the given end city
# 2. Students are also encouraged to discuss on the effect of a nonsymmetrical TSP problem

# extensions:
# 1.Asymmetric traveling salesman problem, for any two cities A and B, the
#   distance from A to B is different from that from B to A
# 2.Sequential ordering problem
#   Sequence constraint is required in real world problem. The salesman is asked to visit certain
#   cities in a req uired sequence. A particular city has to be visited before some other cities
# 3.Time window is considered in the problem.
#   The salesman is required to visit certain cities within certain time window.
#   A data set with 100 cities is given (‘TSPTW_dataset.txt’).
# 4.) For large-scale data, the cities can be divided into several regions (decided by students),
#   the salesman must finish visiting all the cities within the region before traveling to any other
#   city in other regions. Using clustering technique can decompose the large-scale data into
#   several small-scale data sets by its relativity. The dataset with 50 points is provided
#   (‘Cluster_dataset.txt’).
import random
from functools import reduce
import individual
import math
import matplotlib.pyplot as plt
import clustering_GaussianMixtureModel as cluster_GS


class Solution(object):
    def __init__(self):
        self.__pop_size = 30
        self.__mutation_rate = 0.03
        self.__crossover_rate = 0.6
        self.__chromosome_length = 50
        self.__max_generation = 1000
        self.individuals = []
        self.eliteTrend = []
        self.group = []

        print("start readCityData")
        self.cityData = self.readCityData()
        self.group = self.label()
        self.showCityData()
        print("CityData reading finished!")
        print("\n")
        print("start initialize individuals")
        self.initialize()
        for ind in self.individuals:
            for i in ind.chromosome:
                print(self.group[i-1])
        self.fitness()
        self.showPop()
        print("Individuals initialization finished!")

    def readCityData(self):
        f = open("Cluster_dataset.txt", "r")
        cityData = {}
        for i in range(self.__chromosome_length):
            each_city = f.readline()
            each_city = list(map(float, each_city.split()))
            cor = each_city[0:]
            cityData[i+1] = cor
        f.close()
        return cityData

    def label(self):
        return cluster_GS.label(list(self.cityData.values()))

    def initialize(self):
        for i in range(self.__pop_size):
            ind = individual.Individual(self.__chromosome_length)
            self.groupSolution(ind)
            self.individuals.append(ind)

    def groupSolution(self, ind):
        res = []
        for i in ind.chromosome:
            if self.group[i-1] == 0:
                res.append(i)
        for i in ind.chromosome:
            if self.group[i-1] == 1:
                res.append(i)
        for i in ind.chromosome:
            if self.group[i-1] == 2:
                res.append(i)
        ind.chromosome = res

    def showPop(self):
        for i in range(len(self.individuals)):
            print(self.individuals[i].getChromosome())
            print(self.individuals[i].getFitness())

    def showCityData(self):
        print(self.cityData)

    # suppose that the postman spent 1 unit time to travel 1 unit distance, and ignore the service time
    # between he/she get to city and leave city, and if he/she arrive 1 unit time early, he/she will pay
    # one more unit cost.
    def fitness(self):
        for ind in self.individuals:
            distance = 0
            preCity = 0
            for i in range(1, 1 + (len(ind.chromosome) - 1)):
                distance += math.dist(self.cityData[ind.chromosome[preCity]], self.cityData[ind.chromosome[i]])
                preCity = i
            ind.fitness = 1.0 / distance


    def run(self):
        self.fitness()
        for i in range(self.__max_generation):

            # get elite and put it again
            e = self.getElite()
            elite = individual.Individual(self.__chromosome_length)
            elite.fitness = e.fitness
            elite.chromosome = e.chromosome.copy()
            self.eliteTrend.append(elite)
            self.individuals.append(elite)
            print(self.showPop())

            # remove weakest
            # self.removeWeakest()
            # print(self.showPop())

            # mating(Selection)
            self.individuals = self.mating()
            print(self.showPop())

            # crossover
            self.crossover()

            # mutation
            self.mutation()

            # calculate fitness
            self.fitness()

    def getElite(self):
        elite = self.individuals[0]
        for ind in self.individuals:
            if elite.fitness < ind.fitness:
                elite = ind
        return elite

    def removeWeakest(self):
        weakest = self.individuals[0]
        for ind in self.individuals:
            if weakest.fitness > ind.fitness:
                weakest = ind
        self.individuals.remove(weakest)

    def mating(self):
        matingPool = []
        for i in range(self.__pop_size):
            sel1 = random.randint(0, len(self.individuals) - 1)
            sel2 = random.randint(0, len(self.individuals) - 1)
            if self.individuals[sel1].fitness >= self.individuals[sel2].fitness:
                matingPool.append(self.individuals[sel1])
            else:
                matingPool.append(self.individuals[sel2])
        return matingPool

    def crossover(self):
        for i in range(0, self.__pop_size, 2):
            sisChrom = self.individuals[i].chromosome
            broChrom = self.individuals[i+1].chromosome
            if random.random() < self.__crossover_rate:
                for j in range(2):
                    cutPoint1 = random.randint(0, self.__chromosome_length - 1)
                    cutPoint2 = random.randint(0, self.__chromosome_length - 1)
                    if cutPoint1 > cutPoint2:
                        temp = cutPoint1
                        cutPoint1 = cutPoint2
                        cutPoint2 = temp
                    child = individual.Individual(self.__chromosome_length)
                    if j == 0:
                        child.chromosome = broChrom.copy()
                        temp = sisChrom[cutPoint1: cutPoint2 + 1]
                    else:
                        child.chromosome = sisChrom.copy()
                        temp = broChrom[cutPoint1: cutPoint2 + 1]

                    for t in temp:
                        child.chromosome.remove(t)
                    child.chromosome = child.chromosome + temp
                    self.groupSolution(child)
                    self.individuals[i + j] = child

    def mutation(self):
        sel1 = random.randint(0, len(self.individuals) - 1)
        if random.random() < self.__mutation_rate:
            mutPoint1 = random.randint(0, self.__chromosome_length - 1)
            mutPoint2 = random.randint(0, self.__chromosome_length - 1)
            tmp = self.individuals[sel1].chromosome[mutPoint1]
            self.individuals[sel1].chromosome[mutPoint1] = self.individuals[sel1].chromosome[mutPoint2]
            self.individuals[sel1].chromosome[mutPoint2] = tmp
            self.groupSolution(self.individuals[sel1])





s = Solution()
s.run()
# print(s.fitnessTrend)
fitnessTrend = list(map(lambda e: e.fitness, s.eliteTrend))
result = reduce((lambda e1, e2: e1 if e1.fitness > e2.fitness else e2), s.eliteTrend)
print("the optimal path is ")
print(result.chromosome)
print("the fitness value is ")
print(result.fitness)
fig, axs = plt.subplots(1, 2, figsize=(5, 5))
axs[0].plot(fitnessTrend)
bestChrom = result.chromosome
pathx = []
pathy = []
for i in bestChrom:
    pathx.append(s.cityData[i][0])
    pathy.append(s.cityData[i][1])
axs[1].plot(pathx, pathy)
plt.show()