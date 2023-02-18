import numpy
import pygame
import random
import math


class Asteroid:
    def __init__(self, width, height, parent=None):
        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height

        self.closest = False
        self.close_to_ship = False

        # For new asteroids at start of level
        if not parent:
            self.x, self.y = self.spawn_on_edge()
            self.position = numpy.array([self.x, self.y])

            self.radius = 60

            self.rotation = random.randrange(360)
            self.speed = random.uniform(3, 4)
            self.velocity = Asteroid.get_vector_at_angle(self.rotation) * self.speed
        else:
            self.x, self.y = parent.x, parent.y
            self.position = numpy.array([self.x, self.y])

            self.radius = parent.radius / 2

            self.rotation = parent.rotation + random.uniform(-40, 40)
            if parent.radius == 60:
                self.speed = random.uniform(3.5, 4.5)
            else:
                self.speed = random.uniform(4, 5)
            self.velocity = Asteroid.get_vector_at_angle(self.rotation) * self.speed

    def update(self):
        self.position = self.position + self.velocity
        self.x = self.position[0]
        self.y = self.position[1]

    def show(self, window):
        # if self.closest:
        #     pygame.draw.circle(window, (200, 50, 50), (self.x, self.y), self.radius, 1)
        # else:
        #     pygame.draw.circle(window, (255, 255, 255), (self.x, self.y), self.radius, 1)
        pygame.draw.circle(window, (255, 255, 255), (self.x, self.y), self.radius, 1)

    def spawn_on_edge(self):
        edge = self.WINDOW_WIDTH * 2 + self.WINDOW_HEIGHT * 2
        location = random.randrange(edge)
        if location < self.WINDOW_WIDTH:
            x = location
            y = 0
        elif location < 2 * self.WINDOW_WIDTH:
            x = location - self.WINDOW_WIDTH
            y = self.WINDOW_HEIGHT
        elif location < 2 * self.WINDOW_WIDTH + self.WINDOW_HEIGHT:
            x = 0
            y = location - 2 * self.WINDOW_WIDTH
        else:
            x = self.WINDOW_WIDTH
            y = location - 2 * self.WINDOW_WIDTH - self.WINDOW_HEIGHT
        return x, y

    def get_score(self):
        if self.radius == 60:
            return 20
        elif self.radius == 30:
            return 50
        else:
            return 100

    def split(self):
        asteroid_a = Asteroid(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self)
        asteroid_b = Asteroid(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self)
        return [asteroid_a, asteroid_b]

    @staticmethod
    def get_vector_at_angle(rotation):
        x = math.cos(math.radians(rotation))
        y = math.sin(math.radians(rotation))
        return numpy.array([x, y])
