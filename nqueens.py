import random


class Individual:
    def __init__(self, chromosome=None, desk_size=8):
        self.desk_size = desk_size
        self.chromosome = chromosome if chromosome is not None else self.__generate_chromosome()
        self.fitness = self.__hits()

    def __generate_chromosome(self):
        desk = []
        for i in range(0, self.desk_size):
            desk.append("{0:03b}".format(i))
        random.shuffle(desk)
        return "".join(desk)

    def __hits(self):
        wrong_queens_num = 0
        for i in range(0, self.desk_size):
            is_wrong_queen = False
            for j in range(0, self.desk_size):
                if j == i:
                    continue
                neighbour_queen = int(self.chromosome[j * 3:j * 3 + 3], 2)
                my_queen = int(self.chromosome[i * 3:i * 3 + 3], 2)
                if abs(j - i) == abs(neighbour_queen - my_queen) or neighbour_queen == my_queen:
                    is_wrong_queen = True
                    break
            if is_wrong_queen:
                wrong_queens_num += 1
        return 1 - (wrong_queens_num / self.desk_size)

    def update_fitness(self):
        self.fitness = self.__hits()

    def visualize_solution(self):
        result = ''
        for x in range(0, self.desk_size):
            for y in range(0, self.desk_size):
                if y != int(self.chromosome[x * 3:x * 3 + 3], 2):
                    result += '+'
                else:
                    result += 'Q'
            result += '\n'
        return result


class Solver_8_queens:
    def __init__(self, pop_size=300, cross_prob=1, mut_prob=0.4):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob

    def generate_population(self):
        population = []
        for _ in range(0, self.pop_size):
            individual = Individual()
            population.append(individual)
        return population

    def selection(self, population):
        roulette_wheel = [0]
        for individual in population:
            roulette_wheel.append(roulette_wheel[len(roulette_wheel) - 1] + individual.fitness)
        parent_population = []
        for i in range(0, self.pop_size):
            roll_probability = random.uniform(0, roulette_wheel[len(roulette_wheel) - 1])
            for j in range(0, len(roulette_wheel) - 1):
                if roulette_wheel[j] <= roll_probability < roulette_wheel[j + 1]:
                    parent_population.append(population[j])
        return parent_population

    def crossover(self, first_parent, second_parent):
        lotus = random.randint(0, len(first_parent.chromosome) - 1)
        first_child_chromosome = first_parent.chromosome[:lotus] + second_parent.chromosome[lotus:]
        second_child_chromosome = second_parent.chromosome[:lotus] + first_parent.chromosome[lotus:]
        first_child = Individual(first_child_chromosome)
        second_child = Individual(second_child_chromosome)
        return first_child, second_child

    def mutation(self, child):
        lotus = random.randint(0, len(child.chromosome) - 1)
        temp = list(child.chromosome)
        if temp[lotus] == '1':
            temp[lotus] = '0'
        else:
            temp[lotus] = '1'
        return "".join(temp)

    def many_point_crossover(self, first_parent, second_parent):
        lotuses_quantity = random.randint(1, first_parent.desk_size // 2)
        lotuses = set()
        for i in range(0, lotuses_quantity):
            lotuses.add(random.randint(0, first_parent.desk_size // 2))
        lotuses = list(lotuses)
        first_parent_chrom = first_parent.chromosome
        second_parent_chrom = second_parent.chromosome
        first_child_chrom = first_parent_chrom[:lotuses[0]]
        second_child_chrom = second_parent_chrom[:lotuses[0]]
        if lotuses_quantity > 1:
            for i in range(0, len(lotuses) - 1):
                first_child_chrom += second_parent_chrom[lotuses[i]:lotuses[i + 1]]
                second_child_chrom += first_parent_chrom[lotuses[i]:lotuses[i + 1]]
                temp = first_parent_chrom
                first_parent_chrom = second_parent_chrom
                second_parent_chrom = temp
        first_child_chrom += second_parent_chrom[lotuses[len(lotuses) - 1]:]
        second_child_chrom += first_parent_chrom[lotuses[len(lotuses) - 1]:]
        first_child = Individual(first_child_chrom)
        second_child = Individual(second_child_chrom)
        return first_child, second_child

    def tournament_selection(self, population, tour=2):
        parent_population = []
        for _ in range(0, self.pop_size):
            participants = []
            for i in range(0, tour):
                participants.append(population[random.randint(0, self.pop_size - 1)])
            if participants[0].fitness > participants[1].fitness:
                parent_population.append(participants[0])
            else:
                parent_population.append(participants[1])
        return parent_population

    def reproduce(self, population):
        first_parent = population[random.randint(0, self.pop_size - 1)]
        second_parent = population[random.randint(0, self.pop_size - 1)]
        if random.random() < self.cross_prob:
            next_generation = self.crossover(first_parent, second_parent)
            self.mutate_children(next_generation)
        else:
            next_genaration = (first_parent, second_parent)
        return next_generation

    def mutate_children(self, children):
        for child in children:
            if random.random() < self.mut_prob:
                child.chromosome = self.mutation(child)
                child.update_fitness()

    def solve(self, min_fitness=1, max_epochs=7000):
        if min_fitness is None: min_fitness = 0
        if max_epochs is None: max_epochs = 1
        best_fit = 0
        epoch_num = 0
        visualization = None
        population = self.generate_population()
        while True:
            epoch_num += 1
            best_fit = max(individual.fitness for individual in population)
            if best_fit >= min_fitness or epoch_num == max_epochs:
                individual = [individual for individual in population if individual.fitness == best_fit]
                visualization = individual[0].visualize_solution()
                break
            parents = self.selection(population)
            new_population = []
            for _ in range(0, self.pop_size // 2):
                temp = self.reproduce(population)
                for i in temp:
                    new_population.append(i)
            population = new_population
        return best_fit, epoch_num, visualization
