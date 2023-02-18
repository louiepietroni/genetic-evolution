import pygame
import random


class Pipe:
    def __init__(self, width, height):
        self.x = width
        self.verticalGap = 200
        self.width = 80
        self.velocity = 10
        self.top = random.randrange(0, height - self.verticalGap)
        self.bottom = self.top + self.verticalGap

        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height

    def show(self, window):
        pygame.draw.rect(window, (80, 126, 70), (self.x, 0, self.width, self.top))
        pygame.draw.rect(window, (80, 126, 70), (self.x, self.bottom, self.width, self.WINDOW_HEIGHT - self.bottom))

    def update(self):
        self.x -= self.velocity

    def off_screen(self):
        if self.x + self.width < 0:
            return True
        else:
            return False

    def check_hit(self, bird):
        # Check if a bird has hit the pipee
        if self.x < bird.x < self.x + self.width:
            if not self.top + bird.radius < bird.y < self.bottom - bird.radius:
                return True
        return False
