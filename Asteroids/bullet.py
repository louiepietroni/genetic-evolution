import pygame
import numpy
import math


class Bullet:
    def __init__(self, width, height, x, y, rotation, closest_asteroid):
        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height

        self.x = x
        self.y = y
        self.position = numpy.array([self.x, self.y])

        self.radius = 2

        self.rotation = rotation
        self.speed = 30
        self.velocity = Bullet.get_vector_at_angle(self.rotation) * self.speed
        self.closest_asteroid = closest_asteroid

    def update(self):
        self.position = self.position + self.velocity
        self.x = self.position[0]
        self.y = self.position[1]

    def show(self, window):
        pygame.draw.circle(window, (255, 255, 255), (self.x, self.y), 2)

    def check_edges(self):
        if 0 < self.x < self.WINDOW_WIDTH:
            if 0 < self.y < self.WINDOW_HEIGHT:
                return False
        return True

    @staticmethod
    def get_vector_at_angle(rotation):
        x = math.cos(math.radians(rotation))
        y = math.sin(math.radians(rotation))
        return numpy.array([x, y])
