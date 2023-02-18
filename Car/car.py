from neuralnetwork import NeuralNetwork
import pygame
import numpy
import math


class Car:
    def __init__(self, width, height, image):
        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height

        self.x = 500
        self.y = 100

        self.position = numpy.array([self.x, self.y])

        self.image = image
        self.image_rect = self.image.get_rect(center=(self.x, self.y))

        self.steering_angle = 8
        self.velocity = numpy.zeros(2)
        self.acceleration = numpy.zeros(2)

        self.rotation = 0
        self.speed = 8
        self.power = 1.2

        self.brain = NeuralNetwork([7, 8, 3])
        self.score = 0
        self.fitness = 0
        self.frames_since_point = 0

        self.rays = []
        self.ray_points = []

    def update(self):
        self.acceleration -= self.velocity * 0.05
        self.velocity *= 0.92
        self.velocity += self.acceleration
        self.position = self.position + self.velocity
        self.x = self.position[0]
        self.y = self.position[1]

        self.image_rect = self.image.get_rect(center=(self.x, self.y))

        self.acceleration = numpy.zeros(2)

    def show(self, window, vision_options):
        if vision_options[1]:
            for ray in self.rays:
                pygame.draw.line(window, (255, 255, 255), (self.x, self.y), (self.x + ray[0], self.y + ray[1]))
        if vision_options[2]:
            for point in self.ray_points:
                pygame.draw.circle(window, (255, 255, 255), point, 5)

        rotated_image = pygame.transform.rotate(self.image, -self.rotation)
        rotated_image_rect = rotated_image.get_rect(center=self.image_rect.center)
        window.blit(rotated_image, rotated_image_rect)

    def turn_left(self):
        self.rotation -= self.steering_angle

    def turn_right(self):
        self.rotation += self.steering_angle

    @staticmethod
    def get_vector_at_angle(rotation):
        x = math.cos(math.radians(rotation))
        y = math.sin(math.radians(rotation))
        return numpy.array([x, y])

    def forward(self):
        # self.velocity = numpy.array([x, y])
        # self.velocity = self.velocity * self.speed
        self.acceleration = Car.get_vector_at_angle(self.rotation) * self.power

    def think(self, track):
        inputs = self.see(track)
        inputs_normalised = [distance / self.WINDOW_WIDTH for distance in inputs]
        outputs = self.brain.feed_forward(inputs_normalised)
        if outputs[0] > 0.5:
            self.forward()
        if outputs[1] > 0.5:
            self.turn_left()
        if outputs[2] > 0.5:
            self.turn_right()

    def mutate(self, probability):
        self.brain.mutate(probability)


    @staticmethod
    def cross(vector1, vector2):
        return vector1[0] * vector2[1] - vector1[1] * vector2[0]

    @staticmethod
    def distance(vector):
        return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

    def see(self, track):
        straight = Car.get_vector_at_angle(self.rotation) * 1200
        left = Car.get_vector_at_angle(self.rotation + 10) * 1200
        right = Car.get_vector_at_angle(self.rotation - 10) * 1200
        left_side = Car.get_vector_at_angle(self.rotation + 35) * 1200
        right_side = Car.get_vector_at_angle(self.rotation - 35) * 1200
        left_edge = Car.get_vector_at_angle(self.rotation + 60) * 1200
        right_edge = Car.get_vector_at_angle(self.rotation - 60) * 1200

        rays = [straight, left, right, left_side, right_side, left_edge, right_edge]

        distances = []
        points = []
        for ray in rays:
            minimum_length = 2000
            point = (0, 0)
            for i in range(len(track.outside_line_vectors)):
                r_cross_s = Car.cross(ray, track.outside_line_vectors[i])
                if r_cross_s != 0:
                    t = Car.cross((track.outside_points[i] - self.position), track.outside_line_vectors[i]) / r_cross_s
                    if 0 <= t <= 1:
                        u = Car.cross((track.outside_points[i] - self.position), ray) / r_cross_s
                        if 0 <= u <= 1:
                            intersection_point = self.position + ray * t
                            intersection_point = (intersection_point[0], intersection_point[1])
                            distance = Car.distance(ray * t)
                            if distance < minimum_length:
                                minimum_length = distance
                                point = intersection_point

            for i in range(len(track.inside_line_vectors)):
                r_cross_s = Car.cross(ray, track.inside_line_vectors[i])
                if r_cross_s != 0:
                    t = Car.cross((track.inside_points[i] - self.position), track.inside_line_vectors[i]) / r_cross_s
                    if 0 <= t <= 1:
                        u = Car.cross((track.inside_points[i] - self.position), ray) / r_cross_s
                        if 0 <= u <= 1:
                            intersection_point = self.position + ray * t
                            intersection_point = (intersection_point[0], intersection_point[1])
                            distance = Car.distance(ray * t)
                            if distance < minimum_length:
                                minimum_length = distance
                                point = intersection_point

            distances.append(round(minimum_length))
            points.append(point)

        for index in range(len(rays)):
            rays[index] = rays[index] / 1200 * distances[index]
        self.rays = rays
        self.ray_points = points

        # for point in points:
        #     pygame.draw.circle(window, (255, 255, 255), point, 5)
        #
        # pygame.draw.line(window, (255, 255, 255), (self.x, self.y), (self.x + rays[0][0], self.y + rays[0][1]))
        # pygame.draw.line(window, (255, 255, 255), (self.x, self.y), (self.x + rays[1][0], self.y + rays[1][1]))
        # pygame.draw.line(window, (255, 255, 255), (self.x, self.y), (self.x + rays[2][0], self.y + rays[2][1]))
        # pygame.draw.line(window, (255, 255, 255), (self.x, self.y), (self.x + rays[3][0], self.y + rays[3][1]))
        # pygame.draw.line(window, (255, 255, 255), (self.x, self.y), (self.x + rays[4][0], self.y + rays[4][1]))

        return distances

