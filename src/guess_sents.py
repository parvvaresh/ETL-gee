from info import population_size, gens
from genetic import genetic
import random

class guess_sents:
    def __init__(self, target):
        self.target = target
        self.generation = 1
        self.found = False
        self.population = list()
        self.genetic = genetic("test", self.target)
    
    
    def get_target(self):
        for _ in range(population_size):
            gnomes =self.genetic.create_gnomes()
            self.population.append(genetic(gnomes, self.target))
        
        while not self.found:
            self.population = sorted(self.population, key=lambda x : x.fitness_score)  
        
            if self.population[0].fitness_score <= 0:
                self.found = True
                break
            
            
            new_generation = list()
            
            size_best_people = int((10 * population_size) / 100)
            new_generation.extend(self.population[: size_best_people])
            
            for _ in range(int((90 * population_size) / 100)):
                parent1 = random.choice(self.population[:50])
                parent2  = random.choice(self.population[:50])
                child = parent1.generation(parent2)
                new_generation.append(child)
            
            self.population = new_generation
            
            self.generation += 1
            
            self.show() 
        
        self.show() 
    
    
    def show(self):
        print(f"loop is  : {self.generation}")
        print(f"generation: {self.population[0]}\tpassword: {self.population[0].chromosome}\tFitness: {self.population[0].fitness_score}") 
                    
