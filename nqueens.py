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
        wrong_queens = 0
        for i in range(0, self.desk_size):
            flag = False
            for j in range(0, self.desk_size):
                if j == i:
                    continue
                neighbour_queen = int(desk[j * 3:j * 3 + 3], 2)
                my_queen = int(desk[i * 3:i * 3 + 3], 2)
                if abs(j - i) == abs(neighbour_queen - my_queen) or neighbour_queen == my_queen:
                    flag = True
                    break
            if flag:
                wrong_queens += 1
        return 1 - (wrong_queens / self.desk_size)

    def selection(self, population, individual_fitnesses):
        roulette_wheel = [0]
        for i in range(0, self.pop_size):
            roulette_wheel.append(roulette_wheel[len(roulette_wheel) - 1] + individual_fitnesses[i])
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

    def solve(self, min_fitness=1, max_epochs=1000):
        if max_epochs is None: max_epochs = float('inf')
        if min_fitness is None: min_fitness = float('inf')
        best_fit = 0
        epoch_num = 0
        visualization = ""
        population = self.generate_population()
        while True:
            epoch_num += 1
            temp_fitness = []
            new_generation = []
            for individual in population:
                temp_fitness.append(self.hits(individual))
            best_fit = max(temp_fitness)
            if best_fit >= min_fitness or epoch_num == max_epochs:
                index = temp_fitness.index(best_fit)
                visualization = self.print_desk(population[index])
                break
            parents = self.selection(population, temp_fitness)
            for _ in range(0, self.pop_size // 2):
                first_parent = population[random.randint(0, self.pop_size - 1)]
                second_parent = population[random.randint(0, self.pop_size - 1)]
                t = random.random()
                if t < self.cross_prob:
                    children = self.crossover(first_parent, second_parent)
                    for i in children:
                        if random.random() < self.mut_prob:
                            new_generation.append(self.mutation(i))
                        else:
                            new_generation.append(i)
                else:
                    new_generation.append(first_parent)
                    new_generation.append(second_parent)
            population = new_generation
        return best_fit, epoch_num, visualization
