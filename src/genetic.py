from info import population_size, gens
import random

class genetic(object):
    def __init__(self, chromosome = None, target = None):
        self.target = target
        self.chromosome = chromosome
        self.fitness_score = self.get_fitness()
        
        
    
    def create_gnomes(self):
        gnomes_size = len(self.target)
        return "".join(self._create_gnomes() for _ in range(gnomes_size))

    
    def _create_gnomes(self):
        return  random.choice(self.target)

   
    def generation(self, parent):
        new_generation = list()
        for p1, p2 in zip(self.chromosome, parent.chromosome):

            probabality = random.random()
            
            if probabality < 0.45:
                new_generation.append(p1)
            
            elif probabality < 0.90:
                new_generation.append(p2)

            else:
                new_generation.append(self._create_gnomes())
        
        new_generation = "".join(new_generation)
        return genetic(new_generation, self.target)
    
    def get_fitness(self):
        fitness_score = 0
        
        for element1, element2 in zip(self.chromosome, self.target):
            if element1 != element2:
                fitness_score += 1
        
        return fitness_score
    