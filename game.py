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

# Criação da Nave
class nave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/nave.png")
        self.react = self.image.get_react()
        self.react.center = [x, y]
        

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