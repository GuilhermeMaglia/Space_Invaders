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

# Criação da classe Nave
class nave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/nave.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

# Criação do grupo sprite
nave_grupo = pygame.sprite.Group()

# Criação do player
nave = nave(int(screen_width / 2), screen_height - 100)
nave_grupo.add(nave)

run = True
while run:

    clock.tick(fps)

    #desenha o background
    draw_bg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    

    # Atualiza o grupo sprites
    nave_grupo.draw(screen)


    pygame.display.update()





pygame.quit()