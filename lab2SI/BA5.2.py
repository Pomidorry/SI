import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
dim=3
def bee_waggle_dance(solution, ngh, minVal, maxVal):
    # Perform a waggle dance with the solution, neighborhood radius, and min/max values.
    random_offset = (2 * ngh * np.random.rand(solution.size)) - ngh
    new_solution = solution + random_offset
    new_solution = np.clip(new_solution, minVal, maxVal)  # Ensure new_solution is within bounds
    return new_solution

def generate_random_solution(maxParameters, minVal, maxVal):
    return np.random.uniform(low=minVal, high=maxVal, size=maxParameters)

def f(x):
    func=(x[2] + 2) * x[1] * (x[0] ** 2)
    g1 = 1 - (((x[1] ** 3) * x[2]) / (7.178 * (x[0] ** 4))) <=0
    g2 = ((4 * (x[1] ** 2) - x[0] * x[1]) / (12.566 * (x[1] * (x[0] ** 3)) - x[0] ** 4)) + (1 / (5.108 * (x[0] ** 2))) - 1 <= 0
    g3 = 1 - ((140.45 * x[0]) / ((x[1] ** 2) * x[2])) <= 0
    g4 = ((x[0] + x[1]) / 1.5) - 1<=0
    g5 = x[0] >= 0.005
    g6 = x[0] <= 2.0
    g7 = x[1] >= 0.25
    g8 = x[1] <= 1.3
    g9 = x[2] >= 2.0
    g10=x[2] <= 15.0
    if g1 and g2 and g3 and g4 and g5 and g6 and g7 and g8 and g9 and g10: 
        return func  # Penalty for violating constraints
    else:
        return 10000
    
population_show = np.zeros((30, dim + 1))
minVal = np.array([0.005, 0.25, 2.0])
maxVal = np.array([2.0, 1.3, 15])


for i in range(30):
        solution = generate_random_solution(dim, minVal, maxVal)
        population_show[i, 0:dim] = solution
        population_show[i, 2]=np.round(population_show[i, 2])
        population_show[i, dim] = f(solution)
        
fitnessValues_show=list(map(f, population_show))
print(fitnessValues_show)        
def GBA(population_show):
    # Set the problem parameters
    maxIteration = 200
    maxParameters = 3
    minVal = np.array([0.005, 0.25, 2.0])
    maxVal = np.array([2.0, 1.3, 15])
    # Set the grouped bees algorithm (GBA) parameters
    R_ngh = 1
    n = 30
    nGroups = 20

    # GBA's automatic parameter settings
    k = 3 * n / ((nGroups + 1) ** 3 - 1)
    groups = np.zeros(nGroups)
    recruited_bees = np.zeros(nGroups)
    a = (((maxVal - minVal) / 2) - R_ngh) / (nGroups ** 2 - 1)
    b = R_ngh - a

    for i in range(1, nGroups ):
        groups[i - 1] = np.floor(k * i ** 2)
        if groups[i - 1] == 0:
            groups[i - 1] = 1
        recruited_bees[i - 1] = (nGroups + 1 - i) ** 2
        ngh = a * i ** 2 + b

    group_random = n - np.sum(groups)
    group_random = max(group_random, 0)

    # Initialize the population matrix

    #sorted_population = population_show[population_show[:, maxParameters].argsort()]

    # Iterations of the grouped bees algorithm
    beeIndex = 0
    for g in range(nGroups):
        for j in range(int(groups[g])):
            beeIndex += 1

            for _ in range(int(recruited_bees[g])):
                solution = bee_waggle_dance(population_show[beeIndex, 0:maxParameters], ngh, minVal, maxVal)
                fit = f(solution)

                if fit < population_show[beeIndex, maxParameters]:
                    population_show[beeIndex, 0:maxParameters] = solution
                    population_show[beeIndex, 2]=np.round(population_show[beeIndex, 2])
                    population_show[beeIndex, maxParameters] = fit
    for j in range(int(group_random)):
        if beeIndex >= n:
            break
        solution = generate_random_solution(maxParameters, minVal, maxVal)
        fit = f(solution)
        population_show[beeIndex, 0:maxParameters] = solution
        population_show[beeIndex, 2]=np.round(population_show[beeIndex, 2])
        population_show[beeIndex, maxParameters] = fit
        beeIndex += 1

    population_show = population_show[population_show[:, maxParameters].argsort()]

    return population_show

MinFitnessValues = []
generationCounter=0

def animate(i):
    global generationCounter, dim, particles_show, fitnessValues_show

    max_iter=30 

    if generationCounter >= max_iter:
        return
    
    plt.clf()
    # if dim == 1:
    #     ax = fig.add_subplot(111)
    #     X = np.arange(0, 3, 0.01)
    #     Y = evaluate_fitness([X])
    #     ax.plot(X, Y, color='blue', label='Function Curve')
    #     for individ, val in zip(population_show[:, 0], population_show[:, 1]):
    #         ax.scatter(individ, val, marker='*', edgecolors='red')
    #     ax.set_xlabel('X')
    #     ax.set_ylabel('Y')
    #     ax.set_title('GA')
    #     plt.legend()
    # elif dim == 2:
    #     ax = fig.add_subplot(111, projection='3d')
    #     X = np.arange(-10, 10, 0.01)
    #     Y = np.arange(-10, 10, 0.01)
    #     X, Y = np.meshgrid(X, Y)
    #     Z = evaluate_fitness([X, Y])
    #     ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.2)
    #     for individ0,individ1, val in zip(population_show[:,0],population_show[:,1], population_show[:,2]):
    #         ax.scatter(individ0,individ1, val, marker='*', edgecolors='red')
    #     ax.set_xlabel('X')
    #     ax.set_ylabel('Y')
    #     ax.set_zlabel('Fitness')
    #     ax.set_title('GA')
    if dim >= 3:
        plt.plot(MinFitnessValues[int(max_iter * 0.1):], color='red')
        plt.ylabel('Min пристосованість')
        plt.ylabel('Покоління')
        plt.title('Залежність min')

    # population_show[:] = GBA(population_show)
    # print(population_show[:, 0], population_show[:, 1])
    population_show[:] = GBA(population_show)
    #print(population_show)
    fitnessValues_show=list(map(f, population_show))
    print(fitnessValues_show)  
    minFitness = min(fitnessValues_show)
    MinFitnessValues.append(minFitness)
    #print(fitnessValues_show)
    print(f"Generation {generationCounter}: Min Fitness = {minFitness}")

    best_index = fitnessValues_show.index(min(fitnessValues_show))
    print("Best individual = ", *population_show[best_index, 0:3], "\n")
    # MinFitnessValues.append(minFitness)

    generationCounter += 1


fig = plt.figure()

ani = animation.FuncAnimation(fig, animate, interval=900)

plt.show()

# population_show[:] = GBA(population_show)
# print(population_show[:, 0], population_show[:, 1])
# minFitness = min(population_show[:, 1])
# print(population_show)   
# print(population_show[:, 0])     




