import pygame
from bird import Bird
from pipe import Pipe
from neuralnetworkshow import draw_network
from geneticalgorithm import next_generation

# Set up parameters for pygame
WIDTH = 1000
HEIGHT = 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Neuro Evolution of Flappy Bird')
clock = pygame.time.Clock()
frame = 0

# Set up parameters for the game
speed_run = False
speed_run_counter = 0
population_size = 100
birds = [Bird(WIDTH, HEIGHT) for _ in range(population_size)]
pipes = [Pipe(WIDTH, HEIGHT)]

saved_birds = []

pygame.font.init()
font = pygame.font.Font('OpenSans.ttf', 20)
font_for_network = pygame.font.Font('OpenSans.ttf', 10)
network_labels_in = ['Y velocity', 'X distance', 'Y distance up', 'Y distance down']
network_labels_out = ['Jump']
greatest_score = 0
generation = 1
show_network = False

# pipes.append(Pipe(WIDTH, HEIGHT))


def check_exit(speed_run, show_network):
    # Checks each frame if the game should quit or if space has been pressed to run faster
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            speed_run = not speed_run
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            show_network = not show_network
    return speed_run, show_network


def check_jump(bird):
    # Used for testing when bird controlled by space
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.up()

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


def update_game(frame, birds, pipes, width, height, greatest_score):
    # Create a new pipe. If the value is changed, must change in the calculation of score when written to screen
    frame += 1
    if frame == 50 or frame == 0:
        frame = 0
        pipes.append(Pipe(width, height))

    for bird in birds:
        bird.think(pipes)
        bird.update()

    for pipe in pipes:
        pipe.update()

    # Remove any pipes which are now offscreen
    for index, pipe in enumerate(pipes):
        if not pipe.off_screen():
            pipes = pipes[index:]
            break

    if birds[0].score > greatest_score:
        greatest_score = birds[0].score

    return frame, birds, pipes, greatest_score


def draw_game(window, birds, pipes):
    window.fill((122, 174, 212))

    for pipe in pipes:
        pipe.show(window)
    for bird in birds:
        bird.show(window)


def check_collisions(saved_birds, birds, pipes):
    # Check if any birds have collided with any pipes
    for pipe in pipes:
        for i in range(len(birds) - 1, -1, -1):
            if pipe.check_hit(birds[i]):
                saved_birds.append(birds[i])
                del birds[i]

    # Check if any birds are not in the window
    for i in range(len(birds) - 1, -1, -1):
        if not 0 < birds[i].y < birds[i].WINDOW_HEIGHT:
            saved_birds.append(birds[i])
            del birds[i]

    return saved_birds, birds


def check_generation(saved_birds, birds, population_size, pipes, frame, generation):
    # Create a new generation if needed and reset pipes and frame to create a new pipe next frame
    if len(birds) == 0:
        birds = next_generation(population_size, saved_birds)
        saved_birds = []
        pipes = []
        frame = -1
        generation += 1
    return saved_birds, birds, pipes, frame, generation

def draw_info(window, font, birds, greatest_score, generation):
    generation_text = font.render(('Generation: ' + str(generation)), True, (255, 255, 255))
    greatest_score_text = font.render(('Greatest Score: ' + str(int((greatest_score - 40) / 50))), True, (255, 255, 255))
    score_text = font.render(('Score: ' + str(int((birds[0].score - 40) / 50))), True, (255, 255, 255))
    remaining_text = font.render(('Remaining: ' + str(len(birds))), True, (255, 255, 255))

    window.blit(generation_text, (10, 10))
    window.blit(greatest_score_text, (10, 50))
    window.blit(score_text, (10, 90))
    window.blit(remaining_text, (10, 130))

a = True
while True:
    # check_jump(bird)
    # Check if any keys have been pressed to exit or to change the speed
    speed_run, show_network = check_exit(speed_run, show_network)
    if speed_run:
        speed_run_counter += 1

    frame, birds, pipes, greatest_score = update_game(frame, birds, pipes, WIDTH, HEIGHT, greatest_score)
    saved_birds, birds = check_collisions(saved_birds, birds, pipes)
    saved_birds, birds, pipes, frame, generation = check_generation(saved_birds, birds, population_size, pipes, frame, generation)

    # Every 100 updates if speed run or always if otherwise, show screen
    if speed_run and speed_run_counter == 100 or not speed_run:
        speed_run_counter = 0
        draw_game(window, birds, pipes)
        draw_info(window, font, birds, greatest_score, generation)

        if show_network:
            draw_network(window, birds, font, font_for_network, network_labels_in, network_labels_out)

        pygame.display.update()
        clock.tick(30)
        # if a:
        #     pygame.time.delay(2000)
        #     a = False
