import pygame
from pygame.locals import*

#fps
clock = pygame.time.Clock()
fps = 60



screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')



bg = pygame.image.load("img/background.png")

def draw_bg():
    screen.blit(bg, (0, 0))

run = True
while run:

    clock.tick(fps)

    #desenha o background
    draw_bg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()





pygame.quit()