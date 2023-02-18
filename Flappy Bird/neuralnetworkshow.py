import pygame
import numpy


def draw_network(window, birds, label_font, number_font, labels_in, labels_out):
    greatest_score = 0
    greatest_bird = birds[0]
    for bird in birds:
        if bird.score > greatest_score:
            greatest_score = bird.score
            greatest_bird = bird

    network_window_width = 600
    network_window_height = 400
    # network_window = pygame.Surface((network_window_width, network_window_height))
    # network_window.fill((255, 255, 255))
    network_window = pygame.Surface((network_window_width, network_window_height), pygame.SRCALPHA)

    window_width = greatest_bird.WINDOW_WIDTH
    window_height = greatest_bird.WINDOW_HEIGHT
    network_x = window_width - network_window_width
    network_y = window_height - network_window_height

    layer_sizes = greatest_bird.brain.layer_sizes
    x_locations = [(network_window_width * (layer_index + 1)) / (len(layer_sizes) + 1) for layer_index in range(len(layer_sizes))]
    for layer_index, (start_size, end_size) in enumerate(zip(layer_sizes[:-1], layer_sizes[1:])):
        weight_matrix = greatest_bird.brain.weights[layer_index]
        x1 = x_locations[layer_index]
        x2 = x_locations[layer_index + 1]
        for i in range(start_size):
            y1 = (network_window_height * (i + 1)) / (start_size + 1)
            for j in range(end_size):
                y2 = (network_window_height * (j + 1)) / (end_size + 1)
                value = round(weight_matrix[j][i])
                if value > 0:
                    pygame.draw.line(network_window, (50, 150, 50), (x1, y1), (x2, y2), abs(value))
                else:
                    pygame.draw.line(network_window, (150, 50, 50), (x1, y1), (x2, y2), abs(value))

    for layer_index, layer_size in enumerate(layer_sizes):
        x = x_locations[layer_index]
        bias_matrix = greatest_bird.brain.biases[layer_index - 1]
        for i in range(layer_size):
            y = (network_window_height * (i + 1)) / (layer_size + 1)
            pygame.draw.circle(network_window, (150, 150, 150), (x, y), 20)
            if layer_index == 0:
                text = number_font.render(labels_in[i], True, (0, 0, 0))
                network_window.blit(text, (x - 120, y - 8))
            else:
                if layer_index == len(greatest_bird.brain.biases):
                    text = number_font.render(labels_out[i], True, (0, 0, 0))
                    network_window.blit(text, (x + 40, y - 8))

                value = round(bias_matrix[i][0])
                if value > 0:
                    pygame.draw.circle(network_window, (50, 150, 50), (x, y), abs(value) * 5)
                else:
                    pygame.draw.circle(network_window, (150, 50, 50), (x, y), abs(value) * 5)



    for layer_index, (start_size, end_size) in enumerate(zip(layer_sizes[:-1], layer_sizes[1:])):
        x1 = x_locations[layer_index]
        x2 = x_locations[layer_index + 1]
        x = (x1 + x2) / 2

        weight_matrix = greatest_bird.brain.weights[layer_index]
        for i in range(start_size):
            y1 = (network_window_height * (i + 1)) / (start_size + 1)
            for j in range(end_size):
                y2 = (network_window_height * (j + 1)) / (end_size + 1)
                y = (y1 + y2) / 2

                value = round(weight_matrix[j][i], 2)
                text = number_font.render(str(value), True, (80, 80, 80))
                # network_window.blit(text, (x - 8, y - 8))

    for layer_index, layer_size in enumerate(layer_sizes[1:]):
        x = x_locations[layer_index + 1]
        bias_matrix = greatest_bird.brain.biases[layer_index]
        for i in range(layer_size):
            y = (network_window_height * (i + 1)) / (layer_size + 1)

            value = round(bias_matrix[i][0], 2)
            text = number_font.render(str(value), True, (80, 80, 80))
            # network_window.blit(text, (x - 8, y - 8))

    window.blit(network_window, (network_x, network_y))