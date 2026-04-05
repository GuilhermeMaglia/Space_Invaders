import pygame
from pygame.locals import*

#fps
clock = pygame.time.Clock()
fps = 60



screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')


# Define cores
red = (255, 0, 0)
green = (0, 255, 5)


bg = pygame.image.load("img/background.png")

def draw_bg():
    screen.blit(bg, (0, 0))

# Criação da classe Nave
class nave(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/nave.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
    
    def update(self):
        speed = 8

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        # Desenha barra de vida
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15 ))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15 ))


# Criação do grupo sprite
nave_grupo = pygame.sprite.Group()

# Criação do player
nave = nave(int(screen_width / 2), screen_height - 100, 3)
nave_grupo.add(nave)

run = True
while run:

    clock.tick(fps)

    #desenha o background
    draw_bg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    nave.update()

    # Atualiza o grupo sprites
    nave_grupo.draw(screen)


    pygame.display.update()





pygame.quit()