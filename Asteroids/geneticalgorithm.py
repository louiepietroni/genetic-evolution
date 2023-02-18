from ship import Ship
import random


def next_generation(population_size, saved_ships):
    calculate_generation_fitness(saved_ships)

    greatest_score = max([ship.score for ship in saved_ships])
    greatest_fitness = max([ship.fitness for ship in saved_ships])

    # print('New generation, Greatest score:', greatest_score, 'Greatest fitness:', greatest_fitness)
    print('Score:', greatest_score)

    ships = []

    # This is for no cross over, just copy
    for _ in range(population_size):
        ships.append(create_child(saved_ships))

    # This if for crossover
    # for _ in range(population_size // 2):
    #     ships.extend(create_children(saved_ships))

    return ships


def calculate_generation_fitness(saved_ships):
    # This normalises all the fitness values to be between 0 and 1 and sum to 1
    total_score = sum(ship.score for ship in saved_ships)

    for ship in saved_ships:
        ship.fitness = ship.score / total_score


def create_child(saved_ships):
    # Create a new child with no cross over, just mutation
    parent = get_parent(saved_ships)
    child = Ship(parent.WINDOW_WIDTH, parent.WINDOW_HEIGHT, parent.image)
    child.brain = parent.brain.copy()
    child.mutate(0.15)

    return child


def get_parent(saved_ships):
    # As all fitness values sum to 1, this chooses one randomly based on its fitness
    index = 0
    r = random.random()
    while r > 0:
        r -= saved_ships[index].fitness
        index += 1
    index -= 1
    return saved_ships[index]


def create_children(saved_ships):
    # This is to perform cross over between two parents
    first_parent = get_parent(saved_ships)
    second_parent = get_parent(saved_ships)
    first_child = Ship(first_parent.WINDOW_WIDTH, first_parent.WINDOW_HEIGHT, first_parent.image)
    second_child = Ship(first_parent.WINDOW_WIDTH, first_parent.WINDOW_HEIGHT, first_parent.image)
    first_parent_brain = first_parent.brain.copy()
    second_parent_brain = second_parent.brain.copy()

    # Give one child the first part of the one parents weight matrices and the other to the other child

    weights_split = random.randint(0, len(first_parent_brain.weights))
    bias_split = random.randint(0, len(first_parent_brain.biases))

    # To make both split at the same point
    both_split = random.randrange(1, len(first_parent_brain.weights))
    # both_split = random.randint(0, len(first_parent_brain.weights))
    weights_split = both_split
    bias_split = both_split

    first_child.brain.weights[:weights_split] = first_parent_brain.weights[:weights_split]
    second_child.brain.weights[:weights_split] = second_parent_brain.weights[:weights_split]
    first_child.brain.weights[weights_split:] = second_parent_brain.weights[weights_split:]
    second_child.brain.weights[weights_split:] = first_parent_brain.weights[weights_split:]

    first_child.brain.biases[:bias_split] = first_parent_brain.biases[:bias_split]
    second_child.brain.biases[:bias_split] = second_parent_brain.biases[:bias_split]
    first_child.brain.biases[bias_split:] = second_parent_brain.biases[bias_split:]
    second_child.brain.biases[bias_split:] = first_parent_brain.biases[bias_split:]

    first_child.mutate(0.15)
    second_child.mutate(0.15)

    return [first_child, second_child]
