import random


class Individual(object):
    def __init__(self, chromoLen):
        self.chromosome = []
        self.fitness = 0
        self.chromosomeLength = chromoLen
        self.generateChromosome()

    def generateChromosome(self):
        for i in range(self.chromosomeLength):
            self.chromosome.append(i + 1)
        random.shuffle(self.chromosome)

    def getChromosome(self):
        return self.chromosome

    def getFitness(self):
        return self.fitness
