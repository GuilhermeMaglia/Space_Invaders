import pygame
from pygame.locals import*
import random


#fps
clock = pygame.time.Clock()
fps = 60



screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')


# Define variaveis de jogo
rows = 5
cols = 5
alien_cooldown = 1000  #milisegundos
last_alien_shot = pygame.time.get_ticks()


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
        self.last_shot = pygame.time.get_ticks()
    
    def update(self):
        speed = 8

        #Variavel cooldown
        cooldown = 500 #milisegundos

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed
    
        # cooldown
        time_now = pygame.time.get_ticks()

        #atirar
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            balas = Balas(self.rect.centerx, self.rect.top)
            balas_grupo.add(balas)
            self.last_shot = time_now

        # Update mascara
        self.mask = pygame.mask.from_surface(self.image)

        # Desenha barra de vida
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15 ))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15 ))
        elif self.health_remaining <= 0:
            explosao = Explosao(self.rect.centerx, self.rect.centery, 3)
            explosao_grupo.add(explosao)
            self.kill()

# Classe Balas
class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_grupo, True):
            self.kill()
            explosao = Explosao(self.rect.centerx, self.rect.centery, 2)
            explosao_grupo.add(explosao)

# Criação da classe aliens
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

# Classe Balas dos Aliens
class Alien_Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, nave_grupo, False, pygame.sprite.collide_mask):
            self.kill()
            # Reduzir vida da nave 
            nave.health_remaining -= 1
            explosao = Explosao(self.rect.centerx, self.rect.centery, 1)
            explosao_grupo.add(explosao)


# Criação da classe explosão
class Explosao(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"img/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            # Adição de lista de imagens
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0


    def update(self):
        explosao_speed = 3
        # Update animação de explosão
        self.counter += 1

        if self.counter >= explosao_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosao_speed:
            self.kill()


# Criação do grupo sprites
nave_grupo = pygame.sprite.Group()
balas_grupo = pygame.sprite.Group()
alien_grupo = pygame.sprite.Group()
alien_balas_grupo = pygame.sprite.Group()
explosao_grupo = pygame.sprite.Group()

def cria_aliens():
    # Gerador de aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_grupo.add(alien)

cria_aliens()


# Criação do player
nave = nave(int(screen_width / 2), screen_height - 100, 3)
nave_grupo.add(nave)

run = True
while run:

    clock.tick(fps)

    #desenha o background
    draw_bg()


    # Cria balas dos aliens
    time_now = pygame.time.get_ticks()
    # Tiro
    if time_now - last_alien_shot > alien_cooldown and len(alien_balas_grupo) < 5 and len(alien_grupo) > 0:
        ataque_alien = random.choice(alien_grupo.sprites())
        alien_balas = Alien_Balas(ataque_alien.rect.centerx, ataque_alien.rect.bottom)
        alien_balas_grupo.add(alien_balas)
        last_alien_shot = time_now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    nave.update()

    balas_grupo.update()
    alien_grupo.update()
    alien_balas_grupo.update()
    explosao_grupo.update()

    # Atualiza o grupo sprites
    nave_grupo.draw(screen)
    balas_grupo.draw(screen)
    alien_grupo.draw(screen)
    alien_balas_grupo.draw(screen)
    explosao_grupo.draw(screen)


    pygame.display.update()





pygame.quit()