import pygame
import numpy


class Track:
    def __init__(self, outside_points, inside_points, score_points, score_points_radius):
        self.outside_points = outside_points
        self.inside_points = inside_points

        self.score_points = score_points
        self.score_points_radius = score_points_radius

        self.outside_line_vectors = []
        self.inside_line_vectors = []
        self.calculate_outside_line_vectors()
        self.calculate_inside_line_vectors()

    def calculate_outside_line_vectors(self):
        vertices = len(self.outside_points)
        j = vertices - 1
        for i in range(vertices):
            x_displacement = self.outside_points[i][0] - self.outside_points[j][0]
            y_displacement = self.outside_points[i][1] - self.outside_points[j][1]
            displacement = numpy.array([x_displacement, y_displacement])
            self.outside_line_vectors.append(displacement)
            j = i
        self.outside_line_vectors.append(self.outside_line_vectors[0])
        self.outside_line_vectors = self.outside_line_vectors[1:]

    def calculate_inside_line_vectors(self):
        vertices = len(self.inside_points)
        j = vertices - 1
        for i in range(vertices):
            x_displacement = self.inside_points[i][0] - self.inside_points[j][0]
            y_displacement = self.inside_points[i][1] - self.inside_points[j][1]
            displacement = numpy.array([x_displacement, y_displacement])
            self.inside_line_vectors.append(displacement)
            j = i
        self.inside_line_vectors.append(self.inside_line_vectors[0])
        self.inside_line_vectors = self.inside_line_vectors[1:]

    def show(self, window):
        pygame.draw.lines(window, (0, 0, 0), True, self.outside_points, 2)
        pygame.draw.lines(window, (0, 0, 0), True, self.inside_points, 2)

    def check_collision(self, car):
        if self.in_outside_track(car):
            if not self.in_inside_track(car):
                return False
        return True

    def in_outside_track(self, car):
        collision = False
        vertices = len(self.outside_points)
        j = vertices - 1
        for i in range(vertices):
            if (self.outside_points[i][1] > car.y) != (self.outside_points[j][1] > car.y):
                if car.x < (self.outside_points[j][0] - self.outside_points[i][0]) * (car.y - self.outside_points[i][1]) / (self.outside_points[j][1] - self.outside_points[i][1]) + self.outside_points[i][0]:
                    collision = not collision
            j = i
        return collision

    def in_inside_track(self, car):
        collision = False
        vertices = len(self.inside_points)
        j = vertices - 1
        for i in range(vertices):
            if (self.inside_points[i][1] > car.y) != (self.inside_points[j][1] > car.y):
                if car.x < (self.inside_points[j][0] - self.inside_points[i][0]) * (car.y - self.inside_points[i][1]) / (self.inside_points[j][1] - self.inside_points[i][1]) + self.inside_points[i][0]:
                    collision = not collision
            j = i
        return collision


