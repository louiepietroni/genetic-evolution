from bullet import Bullet
from asteroid import Asteroid
from neuralnetwork import NeuralNetwork
import pygame
import numpy
import math


class Ship:
    def __init__(self, width, height, image):
        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height

        self.x = width / 2
        self.y = height / 2

        self.position = numpy.array([self.x, self.y])

        self.image = image
        self.image_rect = self.image.get_rect(center=(self.x, self.y))

        self.steering_angle = 8
        self.velocity = numpy.zeros(2)
        self.acceleration = numpy.zeros(2)

        self.rotation = 0
        self.power = 1.4

        self.bullets = []
        self.score = 0

        self.level = 1
        self.asteroids = []
        self.create_asteroids()

        self.brain = NeuralNetwork([8, 12, 6, 4])

        self.bullet_timer = 0
        self.point_timer = 0

        self.lines = []

    def create_asteroids(self):
        self.asteroids = [Asteroid(self.WINDOW_WIDTH, self.WINDOW_HEIGHT) for _ in range(self.level * 2 + 2)]
        # self.asteroids = [Asteroid(self.WINDOW_WIDTH, self.WINDOW_HEIGHT) for _ in range(1)]

    def update_ship(self):
        self.velocity += self.acceleration
        self.velocity *= 0.93
        self.position = self.position + self.velocity
        self.x = self.position[0]
        self.y = self.position[1]

        self.image_rect = self.image.get_rect(center=(self.x, self.y))
        self.acceleration = numpy.zeros(2)

        closest_asteroid = self.asteroids[0]
        closest_asteroid_distance = self.WINDOW_WIDTH * 2
        for asteroid in self.asteroids:
            if Ship.get_distance(self, asteroid) < closest_asteroid_distance:
                closest_asteroid_distance = Ship.get_distance(self, asteroid)
                closest_asteroid = asteroid
            asteroid.closest = False
        closest_asteroid.closest = True

        # for asteroid in self.asteroids:
        #     if Ship.get_distance(self, asteroid) - asteroid.radius < 70:
        #         asteroid.close_to_ship = True

    def update_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.update()

    def update_bullets(self):
        if self.bullet_timer != 0:
            self.bullet_timer -= 1

        for bullet in self.bullets:
            bullet.update()

    def show_ship(self, window, show_lines):
        rotated_image = pygame.transform.rotate(self.image, -self.rotation)
        rotated_image_rect = rotated_image.get_rect(center=self.image_rect.center)
        window.blit(rotated_image, rotated_image_rect)

        if show_lines:
            for line in self.lines:
                pygame.draw.line(window, (255, 255, 255), (self.x, self.y), (line[0], line[1]))
                pygame.draw.circle(window, (255, 255, 255), (line[0], line[1]), 3)

    def show_asteroids(self, window):
        for asteroid in self.asteroids:
            asteroid.show(window)

    def show_bullets(self, window):
        for bullet in self.bullets:
            bullet.show(window)

    def turn_left(self):
        self.rotation -= self.steering_angle
        self.rotation %= 360

    def turn_right(self):
        self.rotation += self.steering_angle
        self.rotation %= 360

    def forward(self):
        self.acceleration = Ship.get_vector_at_angle(self.rotation) * self.power

    def fire(self):
        if self.bullet_timer == 0:
            closest_asteroid = self.get_closest_asteroid()
            bullet = Bullet(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.x, self.y, self.rotation, closest_asteroid)
            if len(self.bullets) > 3:
                self.bullets = self.bullets[1:]
            self.bullets.append(bullet)
            self.bullet_timer = 7

    def think(self):
        # inputs = self.see()
        inputs = self.see_lines()
        outputs = self.brain.feed_forward(inputs)
        # print('Inputs:', inputs)
        # print('Outputs:', outputs)

        if outputs[0] > 0.5:
            self.turn_left()
        if outputs[1] > 0.5:
            self.turn_right()
        if outputs[2] > 0.5:
            self.forward()
        if outputs[3] > 0.5:
            self.fire()


    def see(self):
        closest_asteroid = self.get_closest_asteroid()

        x_distance = closest_asteroid.x - self.x
        y_distance = closest_asteroid.y - self.y
        distance = math.sqrt(x_distance**2 + y_distance**2)
        bullets = len(self.bullets)
        x_velocity = self.velocity[0]
        y_velocity = self.velocity[1]
        ship_angle_from_horizontal = math.atan2(y_distance, x_distance)
        relative_ship_angle = math.radians(self.rotation) - ship_angle_from_horizontal
        relative_asteroid_angle = math.radians(closest_asteroid.rotation) - ship_angle_from_horizontal

        if relative_ship_angle > math.pi:
            relative_ship_angle -= 2 * math.pi
        if relative_asteroid_angle > math.pi:
            relative_asteroid_angle -= 2 * math.pi
        asteroid_velocity = closest_asteroid.speed


        # print(self.rotation, math.degrees(ship_angle_from_horizontal), math.degrees(relative_ship_angle), math.degrees(relative_asteroid_angle))


        x_distance /= self.WINDOW_WIDTH
        y_distance /= self.WINDOW_WIDTH
        distance /= self.WINDOW_WIDTH
        relative_ship_angle /= math.pi
        relative_asteroid_angle /= math.pi
        bullets /= 4
        x_velocity /= 20
        y_velocity /= 20
        asteroid_velocity /= 10

        # inputs = [x_distance, y_distance, angle, bullets, x_velocity, y_velocity]
        inputs = [distance, relative_ship_angle, relative_asteroid_angle, asteroid_velocity]
        # print(inputs)
        return inputs

    @staticmethod
    def get_vector_at_angle(rotation):
        x = math.cos(math.radians(rotation))
        y = math.sin(math.radians(rotation))
        return numpy.array([x, y])

    def see_lines(self):
        line_segment_values = []

        for offset in range(0, 360, 45):
            line_segment = Ship.get_vector_at_angle(self.rotation + offset) * math.sqrt(self.WINDOW_WIDTH ** 2 + self.WINDOW_HEIGHT ** 2)
            start_x = self.x
            start_y = self.y
            end_x = self.x + line_segment[0]
            end_y = self.y + line_segment[1]
            a = end_y - start_y
            b = start_x - end_x
            c = end_x * start_y - start_x * end_y
            values = (a, b, c)
            line_segment_values.append(values)

        distances = []
        points = []

        for values in line_segment_values:
            a = values[0]
            b = values[1]
            c = values[2]

            shortest_distance = math.sqrt(self.WINDOW_WIDTH ** 2 + self.WINDOW_HEIGHT ** 2)
            shortest_point = (self.x - b, self.y + a)

            end_point = (self.x - b, self.y + a)
            full_distance = shortest_distance

            for asteroid in self.asteroids:
                distance_one = math.sqrt(self.WINDOW_WIDTH ** 2 + self.WINDOW_HEIGHT ** 2)
                distance_two = math.sqrt(self.WINDOW_WIDTH ** 2 + self.WINDOW_HEIGHT ** 2)
                if not -100 < b < 100:
                    x_squared_coefficient = a ** 2 + b ** 2
                    x_coefficient = 2 * a * c + 2 * a * b * asteroid.y - 2 * b ** 2 * asteroid.x
                    constant_coefficient = c ** 2 + 2 * b * c * asteroid.y - b ** 2 * (asteroid.radius ** 2 - asteroid.x ** 2 - asteroid.y ** 2)

                    discriminant = x_coefficient ** 2 - 4 * x_squared_coefficient * constant_coefficient
                    if discriminant >= 0:
                        x_one = (-x_coefficient + math.sqrt(discriminant)) / (2 * x_squared_coefficient)
                        x_two = (-x_coefficient - math.sqrt(discriminant)) / (2 * x_squared_coefficient)
                        y_one = -(a * x_one + c) / b
                        y_two = -(a * x_two + c) / b

                        distance_one = math.sqrt((x_one - self.x) ** 2 + (y_one - self.y) ** 2)
                        distance_two = math.sqrt((x_two - self.x) ** 2 + (y_two - self.y) ** 2)

                        if (self.x < x_one) != (x_one < end_point[0]):
                            distance_one = full_distance
                        if (self.x < x_two) != (x_one < end_point[0]):
                            distance_two = full_distance

                else:
                    y_squared_coefficient = a ** 2 + b ** 2
                    y_coefficient = 2 * b * c + 2 * a * b * asteroid.x - 2 * a ** 2 * asteroid.y
                    constant_coefficient = c ** 2 + 2 * a * c * asteroid.x - a ** 2 * (asteroid.radius ** 2 - asteroid.x ** 2 - asteroid.y ** 2)

                    discriminant = y_coefficient ** 2 - 4 * y_squared_coefficient * constant_coefficient
                    if discriminant >= 0:
                        y_one = (-y_coefficient + math.sqrt(discriminant)) / (2 * y_squared_coefficient)
                        y_two = (-y_coefficient - math.sqrt(discriminant)) / (2 * y_squared_coefficient)
                        x_one = -(b * y_one + c) / a
                        x_two = -(b * y_two + c) / a

                        distance_one = math.sqrt((x_one - self.x) ** 2 + (y_one - self.y) ** 2)
                        distance_two = math.sqrt((x_two - self.x) ** 2 + (y_two - self.y) ** 2)

                        if (self.y < y_one) != (y_one < end_point[1]):
                            distance_one = full_distance
                        if (self.y < y_two) != (y_one < end_point[1]):
                            distance_two = full_distance

                if distance_one < distance_two:
                    # print('distance one was lower')
                    if distance_one < shortest_distance:
                        shortest_distance = distance_one
                        shortest_point = (x_one, y_one)
                else:
                    # print('Intersection found')
                    if distance_two < shortest_distance:

                        # print('distance two is new')
                        shortest_distance = distance_two
                        shortest_point = (x_two, y_two)

            # if int(shortest_distance) != 1389:
            #     print('New')

            distances.append(shortest_distance)
            points.append(shortest_point)

        maximum = math.sqrt(self.WINDOW_WIDTH ** 2 + self.WINDOW_HEIGHT ** 2)
        distances = [distance / maximum for distance in distances]

        # self.lines = [(int(point[0]), int(point[1])) for point in points]
        self.lines = points
        # self.lines = ray_points

        return distances

    @staticmethod
    def check_object_edges(item):
        if item.x > item.WINDOW_WIDTH:
            item.position[0] -= item.WINDOW_WIDTH
        elif item.x < 0:
            item.position[0] += item.WINDOW_WIDTH

        if item.y > item.WINDOW_HEIGHT:
            item.position[1] -= item.WINDOW_HEIGHT
        elif item.y < 0:
            item.position[1] += item.WINDOW_HEIGHT

        item.x = item.position[0]
        item.y = item.position[1]

    def check_edges_ship(self):
        Ship.check_object_edges(self)

    def check_edges_asteroids(self):
        for asteroid in self.asteroids:
            Ship.check_object_edges(asteroid)

    def check_edges_bullets(self):
        # for bullet in self.bullets:
        #     Ship.check_object_edges(bullet)
        for i in range(len(self.bullets) - 1, -1, -1):
            if self.bullets[i].check_edges():
                del self.bullets[i]

    @staticmethod
    def get_distance(item_a, item_b):
        x_difference = item_a.x - item_b.x
        y_difference = item_a.y - item_b.y
        distance = math.sqrt(x_difference ** 2 + y_difference ** 2)
        return distance

    def check_collisions(self):
        self.point_timer += 1
        if self.point_timer == 600:
            return True
        closest_asteroid = self.get_closest_asteroid()
        x_distance = closest_asteroid.x - self.x
        y_distance = closest_asteroid.y - self.y
        angle = math.atan2(y_distance, x_distance)
        angle_relative = math.radians(self.rotation) - angle
        if angle_relative > math.pi:
            angle_relative -= math.pi * 2
        angle_relative = math.degrees(angle_relative)
        angle = math.degrees(angle)
        # if -10 < angle_relative < 10:
        #     self.score += 1
        # print(self.rotation, angle, angle_relative)

        for i in range(len(self.asteroids) - 1, -1, -1):
            asteroid = self.asteroids[i]

            if Ship.get_distance(self, asteroid) - asteroid.radius < 100:
                asteroid.close_to_ship = True
                # if self.score >= 5:
                #     self.score -= 5
            else:
                if asteroid.close_to_ship:
                    self.score += 40
                    # pass
                asteroid.close_to_ship = False

            if Ship.get_distance(self, asteroid) < asteroid.radius + 16:
                score = asteroid.get_score()
                # if asteroid.closest:
                #     self.score += score
                #     self.point_timer = 0
                if score != 100:
                    new_asteroids = asteroid.split()
                    self.asteroids.extend(new_asteroids)
                del self.asteroids[i]
                return True

            for j in range(len(self.bullets) - 1, -1, -1):
                if Ship.get_distance(self.bullets[j], asteroid) < asteroid.radius + self.bullets[j].radius:
                    score = asteroid.get_score()
                    self.score += score
                    self.point_timer = 0
                    if score != 100:
                        new_asteroids = asteroid.split()
                        self.asteroids.extend(new_asteroids)
                    del self.asteroids[i]
                    del self.bullets[j]
                    break
        return False

    def check_level(self):
        if len(self.asteroids) == 0:
            self.level += 1
            self.create_asteroids()
            # print('Next level')

    def get_closest_asteroid(self):
        closest_asteroid = [asteroid for asteroid in self.asteroids if asteroid.closest][0]
        return closest_asteroid

    def mutate(self, probability):
        self.brain.mutate(probability)

    @staticmethod
    def get_vector_at_angle(rotation):
        x = math.cos(math.radians(rotation))
        y = math.sin(math.radians(rotation))
        return numpy.array([x, y])
