import pygame
from neuralnetwork import NeuralNetwork


class Bird:
    def __init__(self, width, height):
        self.y = height / 2
        self.x = 200
        self.radius = 20
        self.velocity = 0
        self.lift = 30

        self.brain = NeuralNetwork([4, 2, 1])
        self.crashed = False
        self.score = 0
        self.fitness = 0

        self.GRAVITY = 1.7
        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height

    def show(self, window):
        pygame.draw.circle(window, (214, 169, 41), (self.x, self.y), self.radius)

    def think(self, pipes):
        # Check which pipe is the current closest pipe
        current_pipe = pipes[0]
        for pipe in pipes:
            if pipe.x + pipe.width - self.x >= 0:
                current_pipe = pipe
                break

        # Set up the inputs to the network of what the bird can see
        inputs = []

        normalised_y_velocity = self.velocity / 20
        normalised_x_distance = (current_pipe.x + current_pipe.width - self.x) / self.WINDOW_WIDTH
        normalised_top_distance = (self.y - current_pipe.top) / self.WINDOW_HEIGHT
        normalised_bottom_distance = (current_pipe.bottom - self.y) / self.WINDOW_HEIGHT

        inputs.append(normalised_y_velocity)
        inputs.append(normalised_x_distance)
        inputs.append(normalised_top_distance)
        inputs.append(normalised_bottom_distance)

        # Pass the inputs through the network and decide whether to jump
        output = self.brain.feed_forward(inputs)[0]
        if output > 0.5:
            self.up()


    def update(self):
        # Increase score for surviving which is used for fitness function
        self.score += 1

        # Adjust velocity and position
        self.velocity += self.GRAVITY
        self.velocity *= 0.9
        self.y += self.velocity

    def up(self):
        # If jump, increase velocity up
        self.velocity -= self.lift

    def mutate(self, probability):
        # When a new child is created, used to mutate the neural network for variation
        self.brain.mutate(probability)


