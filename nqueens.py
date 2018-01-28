import random


class Solver_8_queens:
    def __init__(self, pop_size=300, cross_prob=1, mut_prob=0.8, desk_size=8):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        self.desk_size = desk_size

    def generate_population(self):
        population = []
        for k in range(0, self.pop_size):
            desk = []
            for i in range(0, self.desk_size):
                desk.append("{0:03b}".format(i))
            random.shuffle(desk)
            population.append("".join(desk))
        return population

    def hits(self, desk):
        wrong_queens_num = 0
        for i in range(0, self.desk_size):
            is_wrong_queen = False
            for j in range(0, self.desk_size):
                if j == i:
                    continue
                neighbour_queen = int(desk[j * 3:j * 3 + 3], 2)
                my_queen = int(desk[i * 3:i * 3 + 3], 2)
                if abs(j - i) == abs(neighbour_queen - my_queen) or neighbour_queen == my_queen:
                    is_wrong_queen = True
                    break
            if is_wrong_queen:
                wrong_queens_num += 1
        return 1 - (wrong_queens_num / self.desk_size)

    def selection(self, population, population_fitnesses):
        roulette_wheel = [0]
        for i in range(0, self.pop_size):
            roulette_wheel.append(roulette_wheel[len(roulette_wheel) - 1] + population_fitnesses[i])

        parent_population = []
        for i in range(0, self.pop_size):
            roll_probability = random.uniform(0, roulette_wheel[len(roulette_wheel) - 1])
            for j in range(0, len(roulette_wheel) - 1):
                if roulette_wheel[j] <= roll_probability < roulette_wheel[j + 1]:
                    parent_population.append(population[j])
        return parent_population

    def crossover(self, first_parent, second_parent):
        lotus = random.randint(0, len(first_parent) - 1)
        first_child = first_parent[:lotus] + second_parent[lotus:]
        second_child = second_parent[:lotus] + first_parent[lotus:]
        return first_child, second_child

    def mutation(self, chromosome):
        lotus = random.randint(0, len(chromosome) - 1)
        temp = list(chromosome)
        if temp[lotus] == '1':
            temp[lotus] = '0'
        else:
            temp[lotus] = '1'
        return "".join(temp)

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

    def solve(self, min_fitness=1, max_epochs=8000):
        if min_fitness is None: min_fitness = 0
        if max_epochs is None: max_epochs = 1
        best_fit = 0
        epoch_num = 0
        visualization = None
        population = self.generate_population()
        while True:
            epoch_num += 1
            population_fitnesses = []
            for individual in population:
                population_fitnesses.append(self.hits(individual))
            best_fit = max(population_fitnesses)
            if best_fit >= min_fitness or epoch_num == max_epochs:
                index = population_fitnesses.index(best_fit)
                visualization = self.print_desk(population[index])
                break
            parents = self.selection(population, population_fitnesses)
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
            next_generation = self.mutate_children(self.crossover(first_parent, second_parent))
        else:
            next_genaration = (first_parent, second_parent)
        return next_generation

    def mutate_children(self, children):
        mutants = []
        for child in children:
            if random.random() < self.mut_prob:
                mutants.append(self.mutation(child))
            else:
                mutants.append(child)
        return mutants
