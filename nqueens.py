import random


class Individ:
    def __init__(self, desk_size=8, chromosome=None):
        self.desk_size = 8
        if chromosome is not None:
            self.chromosome = chromosome
        else:
            self.chromosome = self.__generate_chromosome()
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


class Solver_8_queens:
    def __init__(self, pop_size=10, cross_prob=1, mut_prob=0.8, desk_size=8):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        self.desk_size = desk_size

    def generate_population(self):
        population = []
        for _ in range(0, self.pop_size):
            individ = Individ()
            population.append(individ)
        return population

    def selection(self, population):
        roulette_wheel = [0]
        for individ in population:
            roulette_wheel.append(roulette_wheel[len(roulette_wheel) - 1] + individ.fitness)

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
        first_child = Individ(first_child_chromosome)
        second_child = Individ(second_child_chromosome)
        return first_child, second_child

    def mutation(self, child):
        lotus = random.randint(0, len(child.chromosome) - 1)
        temp = list(child.chromosome)
        if temp[lotus] == '1':
            temp[lotus] = '0'
        else:
            temp[lotus] = '1'
        child.chromosome = "".join(temp)
        child.update_fitness()

    def print_desk(self, desk):
        result = ''
        for x in range(0, self.desk_size):
            for y in range(0, self.desk_size):
                if y != int(desk[x * 3:x * 3 + 3], 2):
                    result += '+'
                else:
                    result += 'Q'
            result += '\n'
        return result

    def solve(self, min_fitness=1, max_epochs=3000):
        if min_fitness is None: min_fitness = 0
        if max_epochs is None: max_epochs = 1
        best_fit = 0
        epoch_num = 0
        visualization = None
        population = self.generate_population()
        while True:
            epoch_num += 1
            best_fit = max(individ.fitness for individ in population)
            if best_fit >= min_fitness or epoch_num == max_epochs:
                individ = [individ for individ in population if individ.fitness == best_fit]
                visualization = self.print_desk(individ[0].chromosome)
                break
            parents = self.selection(population)
            new_population = []
            for _ in range(0, self.pop_size // 2):
                temp = self.reproduce(population)
                for i in temp:
                    new_population.append(i)
            population = new_population
        return best_fit, epoch_num, visualization

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
                self.mutation(child)
