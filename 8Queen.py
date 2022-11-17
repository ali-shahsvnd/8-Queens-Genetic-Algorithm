import random
import matplotlib.pyplot as plt
import numpy as np

# population size
POP_SIZE = 100
# number of generations
NUM_GEN = 10000
# mutation rate
MUT_RATE = 0.8


# fitness function
def fitness(chromosome):
    # number of conflicts
    conflicts = 0
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            # check row and diagonal conflicts
            if chromosome[i] == chromosome[j] or abs(chromosome[i] - chromosome[j]) == j - i:
                conflicts += 1
    return 28 - conflicts

# selection function
def selection(population):
    # select five random chromosomes
    random_list = random.sample(population, 5)
    # sort five chromosomes by fitness
    random_list = sorted(random_list, key=lambda chromosome: fitness(chromosome))
    # return best two chromosomes
    return random_list[-1], random_list[-2]

# crossover function
def crossover(parent1, parent2):
   
    crossover_point = random.randint(0, 7)
    child1 = parent1[:crossover_point]
    child1 = child1 + [i for i in parent2[crossover_point:] if i not in child1]
    child1 = child1 + [i for i in parent1[crossover_point:] if i not in child1]
    child2 = parent2[:crossover_point]
    child2 = child2 + [i for i in parent1[crossover_point:] if i not in child2]
    child2 = child2 + [i for i in parent2[crossover_point:] if i not in child2]

    return child1, child2


# mutation function
def mutation(chromosome):
        # select two random positions
        pos1 = random.randint(0, len(chromosome) - 1)
        pos2 = random.randint(0, len(chromosome) - 1)
        # swap values
        chromosome[pos1], chromosome[pos2] = chromosome[pos2], chromosome[pos1]
        return chromosome

# plot chessboard and queens
def plot_board(results):

    plt.figure(figsize=(6, 6))
    plt.xlim(0, 8)
    plt.ylim(0, 8)
    plt.xticks(np.arange(0, 8, 1))
    plt.yticks(np.arange(0, 8, 1))
    plt.grid()
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                plt.fill_between([i, i + 1], [j, j], [j + 1, j + 1], color='black')

    results.reverse()
    for i in range(len(results)):
            # print Q in chessboard with red color
        plt.text( 7.5 - i , results[i] + 0.5 , 'Q', color='red', fontsize=30, horizontalalignment='center', verticalalignment='center')
    plt.show()


# evaluate fitness
def evaluate(chromosome):
        if fitness(chromosome) == 28:
            return True
        else:
            return False

# survival selection
def survival_selection(population, child1 , child2):
    fitness_per_chromosome = []
    for chromosome in population:
        fitness_per_chromosome += [[fitness(chromosome), chromosome]]
    fitness_per_chromosome.sort()
    # fitness_per_chromosome.reverse()
    # delete worst 2 chromosome
    del fitness_per_chromosome[0]
    del fitness_per_chromosome[0]
    new_population = [i[1] for i in fitness_per_chromosome]
    # add two new children
    new_population.append(child1)
    new_population.append(child2)
    
    return new_population


# generate initial population
def generate_population():
    population = []
    for i in range(POP_SIZE):
        chromosome = list(range(8))
        random.shuffle(chromosome)
        population.append(chromosome)
    return population

def genetic_algorithm(termination = 'first_fit'):
    # initialize population
    population = generate_population()

    # initialize fitness list
    solution_list = []
    solution_gen_list=[]
    # start evolution
    for i in range(NUM_GEN):

        # calculate fitness of each chromosome and check if solution is in initial population
        for chromosome in population:
            if evaluate(chromosome):
                solution_list.append(chromosome)
                solution_gen_list.append(i)
                if termination == 'first_fit':
                    print("Solution found at generation : " + str(i) + " and chromosome is " + str(chromosome))
                    plot_board(chromosome)
                    return solution_gen_list

        # selecttion
        parent1, parent2 = selection(population)

        # crossover
        child1, child2 = crossover(parent1, parent2)

        # mutation
        if random.random() < MUT_RATE:
            child1 = mutation(child1)
            child2 = mutation(child2)
        
        # next generation
        population = survival_selection(population, child1, child2)
    
    if len(solution_list) == 0:
        # print("No solution found")
        solution_gen_list.append(NUM_GEN)

    # delete duplicate solutions
    solution_list = list(set(tuple(solution) for solution in solution_list))
    # make list to numpy array
    solution_list = np.array(solution_list)
    print("Number of solutions found : {}".format(len(solution_list)))
    print("Solutions are : ")
    print(solution_list)
    # print("solution list is : " + str(solution_list))
    print('-'*50)

    return solution_gen_list
    


# if termination = 'first_fit' after finding first solution stop and plot the solution
# if termination = 'all_fit' after finding all solutions in NUM_GEN iteration stop and return all found solutions
genetic_algorithm(termination='first_fit')



# run genetic algorithm 100 times and plot the average number of generations
# def run_genetic_algorithm():
#     # initialize list of generations
#     generations = []
#     for i in range(100):
#         generations += genetic_algorithm(termination='all_fit')
#     # calculate average number of generations
#     average = sum(generations)/len(generations)
#     print("Average number of generations is : " + str(average))
#     # plot histogram
#     plt.hist(generations, bins=100)
#     plt.title("Average number of generations is : " + str(average))
#     plt.show()

# run_genetic_algorithm()
