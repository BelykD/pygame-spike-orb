
"""
Spike Orb - Pygame

Author: Dylan Belyk
"""

import pygame
import os
import sys
import random

pygame.init() # Initializing pygame

WIDTH, HEIGHT = 600, 900 # Screen width and height
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
LOAD = pygame.image.load # To simplify image loading code
ORB_CHARACTER, ORB_GAME_OVER, SPIKE = map(LOAD, [
    os.path.join('Assets', 'orbcharactersquare.png'),
    os.path.join('Assets', 'orbcharactergameover.png'),
    os.path.join('Assets', 'spike.png')
])

pygame.display.set_caption("Spike Orb") # Window caption
pygame.display.set_icon(ORB_CHARACTER) # Window icon

colors = { # Colors dictionary
    'PURPLE': (125, 55, 212),
    'RED': (255, 0, 0),
    'WHITE': (255, 255, 255),
    'YELLOW': (255, 255, 0)
}

score = [] # To be appended to hold score value
ORB_DIMENSIONS = 80 # Size of orb character
ORB_X, ORB_Y = (WIDTH - ORB_DIMENSIONS) // 2, (HEIGHT - ORB_DIMENSIONS) // 2 # Centering image in the window
GAP, SPIKE_WIDTH = 250, 150 # Space between spikes and width of spike
spike_dim_y = random.randint(100, 550) # Randomly generating spikes height
SPIKE_SPAWN_Y = 0 # Aligning spike to the bottom of the screen
MOVE_SPEED, SPIKE_SPEED = 15, -5 # Setting the speed that the spikes move and set a variable for player movement speed
MAX_SPIKE_HEIGHT, MIN_SPIKE_HEIGHT = 550, 100 # Minimum and maximum spike sizes
limit_top, limit_bottom = 0, 820 # Collision to keep character within the game window
FPS = 60 # Variable for setting frame rate
GRAVITY = 5 # Set a variable for gravity strength

background_array = ['purplecity1.jpg', 'purplecity2.jpg', 'purplecity3.jpg', 'purplecity4.jpg', 'purplecity5.jpg', # Array of random background images
                    'purplecity6.jpg', 'purplecity7.jpg', 'purplecity8.jpg', 'purplecity9.jpg', 'purplecity10.jpg', 'purplecity11.jpg']

run = globals().setdefault('run', True) # Setting run's global to equal true

def random_background_load(): # Function to generate a random background
    global BACKGROUND
    BACKGROUND = LOAD(os.path.join('Assets', 'Backgrounds', random.choice(background_array)))

def draw_window(orb, height, movement): # Order of which drawing items matters - drawing first = behind
    WIN.fill(colors['PURPLE']) # Background color - #7D37D4 Purple
    WIN.blit(BACKGROUND, (0, 0)) # Loading random background
    WIN.blit(ORB_CHARACTER, (orb.x, orb.y)) # Character loading

    spike_dim_bot_y = HEIGHT - (height + GAP) # Sets height of bottom spike keeping the GAP between it and the top spike
    spike_spawn_bot_y = HEIGHT - spike_dim_bot_y # Sets location of bottom spike related to the random height of top spike

    spike_top = pygame.Rect(movement, SPIKE_SPAWN_Y, SPIKE_WIDTH, height) # Hit box on top spike
    spike_bottom = pygame.Rect(movement, spike_spawn_bot_y, SPIKE_WIDTH, spike_dim_bot_y) # Hit box on bottom spike
   
    hit_boxes = [orb, spike_top, spike_bottom]  # List elements for hitboxes
    for hit_box in hit_boxes:
        pygame.draw.rect(WIN, colors['RED'], hit_box, 1)  # Drawing hitboxes for DEBUGGING

    scale_spike_top = height / SPIKE_WIDTH # Scale factors
    scale_spike_bottom = spike_dim_bot_y / SPIKE_WIDTH
    scaled_spike_top = pygame.transform.scale(SPIKE, (150, int(SPIKE.get_height() * scale_spike_top))) # Scaling image to fit each spike
    scaled_spike_bottom = pygame.transform.scale(SPIKE, (150, int(SPIKE.get_height() * scale_spike_bottom)))
    flip_spike_top = pygame.transform.flip(scaled_spike_top, False, True) # Flipping the top image
    
    WIN.blit(flip_spike_top, spike_top) # Displaying each spike image on its rect
    WIN.blit(scaled_spike_bottom, spike_bottom)

    text_surface = pygame.font.SysFont("Impact", 32).render("SCORE: " + str(len(score)), True, colors['YELLOW'])
    WIN.blit(text_surface, (10, 10)) # Displaying score

    if orb.colliderect(spike_top) or orb.colliderect(spike_bottom): # Handles collisions
        print("COLLIDE")
        end()
    pygame.display.update() # Updates display to show background

def start(): # Start screen function
    WIN.fill(colors['PURPLE']) # Background color - #7D37D4 Purple
    start_text = pygame.font.SysFont("Impact", 32).render("PRESS SPACE TO START", True, colors['WHITE'])
    center_text = start_text.get_rect(center = (WIDTH // 2, HEIGHT // 2))
    WIN.blit(start_text, center_text) # Displaying score

    pygame.display.update() # Updates display to show background

def end(): # End game function
    WIN.fill(colors['PURPLE']) # Background color - #7D37D4 Purple
    start_text = pygame.font.SysFont("Impact", 32).render("GAME OVER", True, colors['WHITE']) # Game over text
    continue_text = pygame.font.SysFont("Impact", 32).render("PRESS ENTER TO CONTINUE", True, colors['WHITE']) # Game over text
    final_score = pygame.font.SysFont("Impact", 32).render("SCORE: " + str(len(score)), True, colors['YELLOW']) # Final score

    CENTER_TEXT = start_text.get_rect(center = ((WIDTH // 2) - 85, (HEIGHT // 2) - 100))
    CENTER_CONTINUE = start_text.get_rect(center = ((WIDTH // 2) - 85, (HEIGHT // 2) + 200))
    CENTER_SCORE = start_text.get_rect(center = ((WIDTH // 2) - 85, (HEIGHT // 2) - 150))

    WIN.blit(ORB_GAME_OVER, CENTER_TEXT)
    WIN.blit(start_text, CENTER_TEXT) # Displaying game over text
    WIN.blit(continue_text, CENTER_CONTINUE)
    WIN.blit(final_score, CENTER_SCORE) # Displaying final score

    global run
    run = False

def quit(): # Exit all function
    pygame.quit()   
    sys.exit()

def main():
    random_background_load() # Random background function to get a new background each time
    start_screen = True
    
    SPIKE_SPAWN_X = 650
    new_height = random.randint(MIN_SPIKE_HEIGHT, MAX_SPIKE_HEIGHT)
    orb = pygame.Rect(ORB_X, ORB_Y, ORB_DIMENSIONS, ORB_DIMENSIONS) # Orb character
    clock = pygame.time.Clock() # Clock object for FPS

    global run
    while(run): # Starting game loop
        while(start_screen):
            start()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start_screen = False             

        clock.tick(FPS) # Controlling speed of while loop with FPS

        SPIKE_SPAWN_X += SPIKE_SPEED # Moving spikes horizontally

        for event in pygame.event.get(): # Check for events happening in pygame
            if event.type == pygame.QUIT: # Check for user exiting page and breaking out of while loop
                quit()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]: # Checks for the spacebar
            orb.y -= MOVE_SPEED # Speed that the orb moves with key controls
            if orb.y <= limit_top: # Sets top limit and removes bouncing off the roof when holding space
                orb.y = 0

        if orb.y < limit_bottom: # Adding collision to bottom of screen
            orb.y += GRAVITY # Constantly moving orb down with gravity

        # Reseting spikes position when it goes off screen
        if SPIKE_SPAWN_X <= -SPIKE.get_width():
            SPIKE_SPAWN_X = 650 # Reset spikes location
            new_height = random.randint(MIN_SPIKE_HEIGHT, MAX_SPIKE_HEIGHT) # Generating new random for next spike
            score.append(0)
            print(len(score)) # Debugging for score
        
        draw_window(orb, new_height, SPIKE_SPAWN_X) # Calling draw_window function and passing orb's rect thorugh

    while not run: # Loops when game ends
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_screen = True # Resetting start_screen loop
                    run = True # Resetting run loop
                    score.clear(                ) # Clearing score for next round

                    if __name__ == "__main__":
                        main()           
            elif event.type == pygame.QUIT: # Check for user exiting page
                quit()
    quit()

if __name__ == "__main__":
    main()