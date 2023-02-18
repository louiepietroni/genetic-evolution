from ship import Ship
from geneticalgorithm import next_generation
from neuralnetworkshow import draw_network
import pygame
import math

# Set up parameters for pygame
WIDTH = 1200
HEIGHT = 700
# HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Neuro Evolution of Asteroids')
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font('OpenSans.ttf', 20)
font_for_network = pygame.font.Font('OpenSans.ttf', 10)
network_labels_in = ['Forward', 'Right 1', 'Right 2', 'Right 3', 'Back', 'Left 3', 'Left 2', 'Left 1']
network_labels_out = ['Left', 'Right', 'Forward', 'Fire']
show_network = False

ship_image = pygame.image.load('ship.png')

population_size = 100
ships = [Ship(WIDTH, HEIGHT, ship_image) for _ in range(population_size)]
saved_ships = []
generation = 1
speed_run = False
speed_run_counter = 0


def check_exit(index, speed_run, show_lines, show_network):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            index += 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            speed_run = not speed_run
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            show_lines = not show_lines
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            show_network = not show_network

    return index, speed_run, show_lines, show_network


def check_move(ship):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            ship.fire()
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP]:
        ship.forward()
    if keys_pressed[pygame.K_LEFT]:
        ship.turn_left()
    if keys_pressed[pygame.K_RIGHT]:
        ship.turn_right()


def update_game(ships):
    for ship in ships:
        ship.update_ship()
        ship.update_asteroids()
        ship.update_bullets()

        ship.check_edges_ship()
        ship.check_edges_asteroids()
        ship.check_edges_bullets()

        ship.think()


def check_collisions(ships, saved_ships):
    for ship in ships:
        if ship.check_collisions():
            saved_ships.append(ship)
            ships.remove(ship)
        else:
            ship.check_level()
    return ships, saved_ships


def check_generation(population_size, ships, saved_ships, generation):
    if len(ships) == 0:
        print('Gen:', generation)
        ships = next_generation(population_size, saved_ships)
        saved_ships = []
        generation += 1

    return ships, saved_ships, generation


def draw_game(window, ship, show_lines):
    window.fill((0, 0, 0))

    ship.show_ship(window, show_lines)
    ship.show_asteroids(window)
    ship.show_bullets(window)


def draw_info(window, ship, index, alive, generation):
    score_text = font.render(('Score: ' + str(ship.score)), True, (255, 255, 255))
    index_text = font.render(('Ship index: ' + str(index)), True, (255, 255, 255))
    alive_text = font.render(('Ships alive: ' + str(alive)), True, (255, 255, 255))
    generation_text = font.render(('Generation: ' + str(generation)), True, (255, 255, 255))
    window.blit(score_text, (10, 10))
    window.blit(index_text, (10, 50))
    window.blit(alive_text, (10, 90))
    window.blit(generation_text, (10, 130))

index = 0
show_lines = False
while True:
    index, speed_run, show_lines, show_network = check_exit(index, speed_run, show_lines, show_network)

    if speed_run:
        speed_run_counter += 1

    # check_move(ships[index])
    update_game(ships)

    ships, saved_ships = check_collisions(ships, saved_ships)
    ships, saved_ships, generation = check_generation(population_size, ships, saved_ships, generation)

    index = index % len(ships)

    if speed_run and speed_run_counter == 100 or not speed_run:
        speed_run_counter = 0

        draw_game(window, ships[index], show_lines)
        # draw_info(window, ships[index], index, len(ships), generation)

        if show_network:
            draw_network(window, ships, font, font_for_network, network_labels_in, network_labels_out)

        pygame.display.update()
        clock.tick(30)
