from bird import Bird
import random


def next_generation(population_size, saved_birds):
    calculate_generation_fitness(saved_birds)

    birds = []

    # This is for no cross over, just copy
    for _ in range(population_size):
        birds.append(create_child(saved_birds))

    # This if for crossover
    # for _ in range(population_size // 2):
    #     birds.extend(create_children(saved_birds))

    return birds


def calculate_generation_fitness(saved_birds):
    # This normalises all the fitness values to be between 0 and 1 and sum to 1
    total_score = sum(bird.score for bird in saved_birds)

    for bird in saved_birds:
        bird.fitness = bird.score / total_score


def create_child(saved_birds):
    # Create a new child with no cross over, just mutation
    parent = get_parent(saved_birds)
    child = Bird(parent.WINDOW_WIDTH, parent.WINDOW_HEIGHT)
    child.brain = parent.brain.copy()
    # print(parent.brain.weights[1], 'Parent')
    # print(child.brain.weights[1], 'Child')
    child.mutate(0.02)
    # print(child.brain.weights[1], 'Child after mutation')
    # print(parent.brain.weights[1], 'Parent after mutation')

    return child


def get_parent(saved_birds):
    # As all fitness values sum to 1, this chooses one randomly based on its fitness
    index = 0
    r = random.random()
    while r > 0:
        r -= saved_birds[index].fitness
        index += 1
    index -= 1
    return saved_birds[index]


def create_children(saved_birds):
    # This is to perform cross over between two parents
    first_parent = get_parent(saved_birds)
    second_parent = get_parent(saved_birds)
    first_child = Bird(first_parent.WINDOW_WIDTH, first_parent.WINDOW_HEIGHT)
    second_child = Bird(first_parent.WINDOW_WIDTH, first_parent.WINDOW_HEIGHT)
    first_parent_brain = first_parent.brain.copy()
    second_parent_brain = second_parent.brain.copy()

    # Give one child the first part of the one parents weight matrices and the other to the other child

    weights_split = random.randint(0, len(first_parent_brain.weights))
    bias_split = random.randint(0, len(first_parent_brain.biases))

    first_child.brain.weights[:weights_split] = first_parent_brain.weights[:weights_split]
    second_child.brain.weights[:weights_split] = second_parent_brain.weights[:weights_split]
    first_child.brain.weights[weights_split:] = second_parent_brain.weights[weights_split:]
    second_child.brain.weights[weights_split:] = first_parent_brain.weights[weights_split:]

    first_child.brain.biases[:bias_split] = first_parent_brain.biases[:bias_split]
    second_child.brain.biases[:bias_split] = second_parent_brain.biases[:bias_split]
    first_child.brain.biases[bias_split:] = second_parent_brain.biases[bias_split:]
    second_child.brain.biases[bias_split:] = first_parent_brain.biases[bias_split:]

    first_child.mutate(0.03)
    second_child.mutate(0.03)

    return [first_child, second_child]
