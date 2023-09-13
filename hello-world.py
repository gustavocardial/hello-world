import string
import random

def create_individual(length, genes):
    """ Create a single individual with random genes. """
    individual = ''
    for _ in range(length):
        individual += random.choice(genes)
    return individual

def create_population(size, length, genes):
    """ Create a population of individuals. """
    population = []
    for _ in range(size):
        population.append(create_individual(length, genes))
    return population

def fitness(individual, target):
    """ Calculate fitness score of an individual based on the target. """
    fitness_score = 0
    for char1, char2 in zip(individual, target):
        if char1 == char2:
            fitness_score += 1
    return fitness_score

def select_parents(population, target, retain):
    """ Select the top individuals from the population to breed. """
    population.sort(key=lambda x: fitness(x, target), reverse=True)
    retain_length = int(len(population) * retain)
    return population[:retain_length]

def mutate(individual, genes, probability):
    """ Randomly mutate an individual's genes. """
    if probability > random.random():
        pos_to_mutate = random.randint(0, len(individual) - 1)
        individual = individual[:pos_to_mutate] + random.choice(genes) + individual[pos_to_mutate+1:]
    return individual

def add_diversity(population, target, genes, add_random_individuals):
    """ Add random individuals to the population to maintain diversity. """
    for _ in range(int(len(population) * add_random_individuals)):
        population.append(create_individual(len(target), genes))
    return population

def crossover(parents, population_size):
    """ Breed parents to produce children, performing a crossover. """
    attempts = len(parents)
    while len(parents) < population_size:
        parent1 = random.choice(parents)
        parent2 = parent1
        
        while parent1 == parent2 and attempts > 0:
            parent2 = random.choice(parents)
            attempts -= 1

        if parent1 != parent2 or attempts <= 0:
            half = len(parent1) // 2
            child = parent1[:half] + parent2[half:]
            parents.append(child)
        
    return parents

def main():
    """ Main program that combines all the functions to run the genetic algorithm. """

    # Set the gene pool and target.
    genes = string.ascii_letters + " "
    target = "Hello World"

    # Create the initial population.
    population = create_population(size=200, length=len(target), genes=genes)

    generations = 0

    # Main loop for the genetic algorithm.
    while True:
        print("Generation: {}, Best string: {}".format(generations, population[0]))

        # Condition to terminate the algorithm.
        if fitness(population[0], target) == len(target):
            break

        # Execute genetic operations.
        parents = select_parents(population, target, retain=0.2)
        mutated = []
        for parent in parents:
            mutated.append(mutate(parent, genes, probability=0.01))
        parents = mutated
        parents = add_diversity(parents, target, genes, add_random_individuals=0.01)
        population = crossover(parents, population_size=len(population))
        
        generations += 1

if __name__ == "__main__":
    main()
