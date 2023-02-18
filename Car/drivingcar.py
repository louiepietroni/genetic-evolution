from car import Car
from track import Track
from geneticalgorithm import next_generation
from neuralnetworkshow import draw_network
import pygame
import math

# Set up parameters for pygame
WIDTH = 1200
HEIGHT = 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Neuro Evolution of Driving Car')
clock = pygame.time.Clock()
frame = 0

car_image = pygame.image.load('car.png')
car = Car(WIDTH, HEIGHT, car_image)

# Create the track
track_outside_points_a = [(175, 50), (1000, 50), (1100, 100), (1150, 150), (1150, 500), (1025, 680), (950, 680), (775, 275), (600, 275), (400, 600), (125, 600), (75, 300)]
track_inside_points_a = [(300, 125), (950, 125), (1050, 180), (1050, 450), (1000, 525), (850, 175), (500, 175), (325, 475), (225, 475), (200, 300), (225, 200)]
score_points_a = [(700, 90), (900, 90), (1084, 150), (1100, 300), (1100, 450), (1020, 584), (936, 510), (854, 320), (770, 226), (740, 226), (720, 226), (700, 226), (680, 226), (550, 240), (470, 360), (350, 540), (190, 534), (154, 400), (164, 220), (250, 100), (450, 90)]
score_points_radius_a = [44, 44, 50, 50, 50, 60, 54, 54, 50, 50, 50, 50, 50, 64, 68, 68, 68, 62, 56, 56, 44]
score_points_a = [(700, 90), (900, 90), (1084, 150), (1100, 300), (1100, 450), (1020, 584), (936, 510), (854, 320), (750, 226), (720, 226), (680, 226), (550, 240), (470, 360), (350, 540), (190, 534), (154, 400), (164, 220), (250, 100), (450, 90)]
score_points_radius_a = [44, 44, 50, 50, 50, 60, 54, 54, 50, 50, 50, 64, 68, 68, 68, 62, 56, 56, 44]
track_a = Track(track_outside_points_a, track_inside_points_a, score_points_a, score_points_radius_a)


track_outside_points_b = [(175, 50), (700, 50), (825, 175), (875, 175), (1000, 50), (1100, 50), (1175, 100), (1175, 575), (1100, 675), (700, 675), (650, 625), (650, 500), (700, 450), (900, 425), (650, 400), (525, 250), (425, 250), (375, 300), (375, 400), (600, 500), (600, 625), (375, 675), (150, 650), (50, 550), (50, 200)]
track_inside_points_b = [(250, 125), (625, 125), (775, 275), (925, 275), (1050, 150), (1075, 200), (1075, 500), (1025, 575), (800, 575), (800, 550), (1050, 500), (1050, 350), (700, 300), (600, 175), (350, 175), (275, 250), (275, 475), (475, 550), (375, 575), (200, 550), (150, 500), (150, 250)]
score_points_b = [(675, 100), (750, 174), (850, 225), (925, 202), (1000, 128), (1120, 140), (1128, 210), (1128, 350), (1128, 500), (1050, 622), (850, 626), (750, 504), (875, 480), (900, 372), (800, 366), (636, 300), (500, 214), (330, 275), (425, 475), (460, 604), (200, 604), (100, 450), (120, 200), (300, 90), (500, 90)]
score_points_radius_b = [54, 56, 50, 54, 54, 68, 54, 54, 54, 54, 50, 70, 56, 54, 50, 54, 40, 54, 54, 54, 54, 54, 58, 40, 40]
track_b = Track(track_outside_points_b, track_inside_points_b, score_points_b, score_points_radius_b)

track = track_b
show_score_points = False

# Set up parameters for the game
speed_run = False
speed_run_counter = 0
population_size = 75
cars = [Car(WIDTH, HEIGHT, car_image) for _ in range(population_size)]
show_1 = False

saved_cars = []

show_track = True
show_car_rays = False
show_car_points = False
vision_options = [show_track, show_car_rays, show_car_points]


pygame.font.init()
font = pygame.font.Font('OpenSans.ttf', 20)
font_for_network = pygame.font.Font('OpenSans.ttf', 10)
network_labels_in = ['Forward', 'Left Forward', 'Right Forward', 'Left Diagonal', 'Right Diagonal', 'Left', 'Right']
network_labels_out = ['Forward', 'Left', 'Right']
show_network = False
greatest_score = 0
generation = 1


def check_exit(speed_run, show_score_points, show_1, vision_options, show_network):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            speed_run = not speed_run
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            show_score_points = not show_score_points
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            show_1 = not show_1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
            vision_options[0] = not vision_options[0]
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            vision_options[1] = not vision_options[1]
        if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            vision_options[2] = not vision_options[2]
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            show_network = not show_network
    return speed_run, show_score_points, show_1, vision_options, show_network


def check_move(car):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP]:
        car.forward()
    if keys_pressed[pygame.K_LEFT]:
        car.turn_left()
    if keys_pressed[pygame.K_RIGHT]:
        car.turn_right()


def update_game(cars, track, saved_cars):
    for car in cars:
        car.update()
        car.think(track)

    for i in range(len(cars) - 1, -1, -1):
        if track.check_collision(cars[i]) or cars[i].frames_since_point > 60:
            # print('Car crashed')
            saved_cars.append(cars[i])
            del cars[i]

    return cars, saved_cars


def draw_game(window, cars, track, show_1, greatest_score, vision_options):
    window.fill((156, 167, 171))

    greatest_current_score = 0
    greatest_current_car = cars[0]
    for car in cars:
        if car.score > greatest_current_score:
            greatest_current_score = car.score
            greatest_current_car = car

    if greatest_current_score > greatest_score:
        greatest_score = greatest_current_score

    if vision_options[0]:
        track.show(window)
    if show_1:
        greatest_current_car.show(window, vision_options)
    else:
        for car in cars:
            car.show(window, vision_options)

    return greatest_score, greatest_current_score


def check_generation(cars, saved_cars, population_size, generation):
    if len(cars) == 0:
        cars = next_generation(population_size, saved_cars)
        saved_cars = []
        generation += 1
    return cars, saved_cars, generation


def give_score(cars, track):
    for car in cars:
        target_index = car.score % len(track.score_points)
        target_score_point = track.score_points[target_index]
        target_score_point_radius = track.score_points_radius[target_index]

        x_difference = target_score_point[0] - car.x
        y_difference = target_score_point[1] - car.y
        distance = math.sqrt(x_difference ** 2 + y_difference ** 2)
        if distance < target_score_point_radius:
            car.score += 1
            car.frames_since_point = 0
        car.frames_since_point += 1
    return cars


def draw_info(window, font, cars, greatest_score, current_score, generation):
    generation_text = font.render(('Generation: ' + str(generation)), True, (255, 255, 255))
    greatest_score_text = font.render(('Greatest Score: ' + str(greatest_score)), True, (255, 255, 255))
    score_text = font.render(('Score: ' + str(current_score)), True, (255, 255, 255))
    remaining_text = font.render(('Remaining: ' + str(len(cars))), True, (255, 255, 255))

    window.blit(generation_text, (10, 10))
    window.blit(greatest_score_text, (10, 50))
    window.blit(score_text, (10, 90))
    window.blit(remaining_text, (10, 130))


while True:
    speed_run, show_score_points, show_1, vision_options, show_network = check_exit(speed_run, show_score_points, show_1, vision_options, show_network)
    if speed_run:
        speed_run_counter += 1

    # check_move(car)
    cars, saved_cars = update_game(cars, track, saved_cars)
    cars, saved_cars, generation = check_generation(cars, saved_cars, population_size, generation)

    cars = give_score(cars, track)

    if speed_run and speed_run_counter == 100 or not speed_run:
        speed_run_counter = 0
        greatest_score, current_score = draw_game(window, cars, track, show_1, greatest_score, vision_options)

        draw_info(window, font, cars, greatest_score, current_score, generation)

        if show_network:
            draw_network(window, cars, font, font_for_network, network_labels_in, network_labels_out)

        # print(len(cars))

        if show_score_points:
            for index in range(len(track.score_points)):
                pygame.draw.circle(window, (36, 156, 54), track.score_points[index], track.score_points_radius[index])


        pygame.display.update()
        clock.tick(30)
