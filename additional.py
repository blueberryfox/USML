import random


class Solver_8_queens:
    def __init__(self, pop_size=4, cross_prob=0.75, mut_prob=0.5, desk_size=8):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        self.desk_size = desk_size
        self.population = self.generate_desk()

    @staticmethod
    def print_desk(desk):
        result = ''
        for x in range(0, len(desk)):
            for y in range(0, len(desk)):
                if y != int(desk[x], 2):
                    result += '+'
                else:
                    result += 'Q'
            result += '\n'
        return result

    def generate_desk(self):
        population = []
        for k in range(0, self.pop_size):
            individual = []
            for i in range(0, self.desk_size):
                individual.append("{0:03b}".format(i))
            random.shuffle(individual)
            population.append(individual)
        return population

    def solve(self, min_fitness=1, max_epochs=10):
        best_fit = 0
        epoch_num = 0
        while best_fit < min_fitness and epoch_num < max_epochs:
            temp_fitness = []
            for chromosome in self.population:
                temp_fitness.append(self.hits(chromosome))
                if best_fit < self.hits(chromosome):
                    best_fit = self.hits(chromosome)
            parents = self.tournir_selection()
            next_generation = []
            for i in range(0, len(parents) - 2):
                temp_cross = random.random()
                if temp_cross <= self.cross_prob:
                    children = list(self.many_point_crossover(parents[i], parents[i + 1]))
                    for child in children:
                        for gen in child:
                            temp_mut = random.random()
                            if temp_mut < self.mut_prob:
                                gen = self.mutation(gen)
                    for child in children:
                        next_generation.append(child)
            epoch_num += 1
        visualization = self.print_desk(self.population[temp_fitness.index(best_fit)])
        return best_fit, epoch_num, visualization

    def hits(self, chromosome):
        wrong_queens = 0
        for i in range(0, self.desk_size):
            flag = False
            for j in range(0, self.desk_size):
                if j != i:
                    if abs(j - i) == abs(int(chromosome[j], 2) - int(chromosome[i], 2)) or chromosome[j] == chromosome[
                        i]:
                        flag = True
                        break
            if flag:
                wrong_queens += 1
        return 1 - (wrong_queens / self.desk_size)

    def tournir_selection(self):
        temp_population = []
        parent_population = []
        for i in range(0, self.pop_size, 2):
            tour = [self.population[i], self.population[i + 1]]
            temp_population.append(tour)
        for tour in temp_population:
            best_fit = 0
            best_chromosome = []
            for chromosome in tour:
                if best_fit < self.hits(chromosome):
                    best_fit = self.hits(chromosome)
                    best_chromosome = chromosome
            parent_population.append(best_chromosome)
        return parent_population

    def many_point_crossover(self, first_parent, second_parent):
        lotuses_quantity = random.randint(1, self.desk_size / 2)
        lotuses = set()
        for i in range(0, lotuses_quantity):
            lotuses.add(random.randint(0, self.desk_size / 2))
        lotuses = list(lotuses)
        first_child = first_parent[:lotuses[0]]
        second_child = second_parent[:lotuses[0]]
        if lotuses_quantity > 1:
            for i in range(0, len(lotuses) - 1):
                first_child += second_parent[lotuses[i]:lotuses[i + 1]]
                second_child += first_parent[lotuses[i]:lotuses[i + 1]]
                temp = first_parent
                first_parent = second_parent
                second_parent = temp
        first_child += second_parent[lotuses[len(lotuses) - 1]:]
        second_child += first_child[lotuses[len(lotuses) - 1]:]
        return first_child, second_child

    def mutation(self, gen):
        lotus = random.randint(0, len(gen) - 1)
        if gen[lotus] == '1':
            gen = gen.replace(gen[lotus], '0')
        else:
            gen = gen.replace(gen[lotus], '1')
        return gen
