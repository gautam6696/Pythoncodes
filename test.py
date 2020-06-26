import numpy as np
import sys



class Board(object):
    def __init__(self):
        self.chromo = None
        self.fitness = None
        self.survival = None

    def set_chromo(self, value):
        self.chromo = value

    def set_fitness(self, value):
        self.fitness = value

    def set_survival(self, value):
        self.survival = value


    class Queens(object):
        def create_chromo(self):
            x = np.arange(0, 8)
            np.random.shuffle(x)
            return x

        def find_fitness(self,chromo):
            max_clashes = 28
            clashes = len(chromo) - len(set(chromo))  # Horizontal clashes
            for i in range(len(chromo)):
                for j in range(len(chromo)):
                    if i != j:
                        index_val = abs(j - i)
                        actual_val = abs(chromo[j] - chromo[i])
                        if actual_val == index_val:
                            clashes += 1
            return max_clashes - clashes

        def create_population(self,size):
            population = []
            for i in range(size):
                population.append(Board())
            for i in range(size):
                population[i].set_chromo(self.create_chromo())
                population[i].set_fitness(self.find_fitness(population[i].chromo))
            return population

        def get_Parent(self):
            parent1 = parent2 = None
            total_clashes = np.sum([x.fitness for x in population])
            for chromo in population:
                chromo.survival = chromo.fitness / (total_clashes * 1.0)

            while True:
                parent1_min_surv = np.random.rand()
                parent1_better_surv = [x for x in population if x.survival <= parent1_min_surv]
                try:
                    parent1 = parent1_better_surv[0]
                    break
                except:
                    pass

            while True:
                parent2_min_surv = np.random.rand()
                parent2_better_surv = [x for x in population if x.survival <= parent2_min_surv]
                try:
                    t = np.random.randint(len(parent2_better_surv))
                    parent2 = parent2_better_surv[t]
                    if parent1 != parent2:
                        break
                    else:
                        continue
                except:
                    continue

            if parent1 is not None and parent2 is not None:
                return parent1, parent2
            else:
                sys.exit(-1)

        def crossover(self,parent1, parent2):
            child = Board()
            child.chromo = []
            n = len(parent1.chromo)
            a = np.random.randint(n)
            child.chromo.extend(parent1.chromo[0:a])
            child.chromo.extend(parent2.chromo[a:])
            child.set_fitness(self.find_fitness(child.chromo))
            return child

        def mutation(self,child):
            if child.fitness < 0.000001:
                n = len(child.chromo)
                a = np.random.randint(n)
                child.chromo[a] = np.random.randint(n)
            return child

        def GeneticAlgo(self):
            newpopulation = []
            for i in range(len(population)):
                parent1, parent2 = self.get_Parent()
                child = self.crossover(parent1, parent2)
                child = self.mutation(child)
                newpopulation.append(child)
            return newpopulation

        def stop_condition(self):
            fitness_values = [x.fitness for x in population]
            if 28 in fitness_values:
                return True
            if iteration == 100:
                return True
            return False


if __name__ == "__main__":
    iteration = 0
    Queenobj = Board.Queens()
    population = Queenobj.create_population(1000)
    print("population created")
    while not Queenobj.stop_condition():
        print(iteration)
        population = Queenobj.GeneticAlgo()
        iteration += 1

    for i in population:
        if i.fitness == 28:
            print("Found solution")
            print(i.chromo)
            print((i.fitness / 28) * 100)
            break