import pygame
from pygame import mixer
from pygame.locals import *
import random
import os

# Inicialização
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.font.init()

# FPS
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders - Pro Edition')

# Fontes
font30 = pygame.font.SysFont('constantia', 30)
font40 = pygame.font.SysFont('constantia', 40)

# Sons 
try:
    explosao_fx = pygame.mixer.Sound("img/explosion.wav")
    explosao2_fx = pygame.mixer.Sound("img/explosion2.wav")
    laser_fx = pygame.mixer.Sound("img/laser.wav")
    for snd in [explosao_fx, explosao2_fx, laser_fx]: snd.set_volume(0.25)
except:
    print("Arquivos de som não encontrados. Verifique a pasta img/")

# Cores
red = (255, 0, 0)
green = (0, 255, 5)
white = (255, 255, 255)

# Variáveis Globais de Jogo
rows = 5
cols = 5
alien_cooldown = 1500
alien_min_cooldown = 400
alien_cooldown_step = 75
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0 # 0 vivo, -1 morreu
score = 0
wave = 1
user_name = ""

# Carregar Background
bg = pygame.image.load("img/background.png")

def draw_bg():
    screen.blit(bg, (0, 0))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# --- NOVO: SISTEMA DE SCORE E NOME ---
def save_score(name, final_score):
    with open("highscores.txt", "a") as file:
        file.write(f"Nome: {name} | Pontos: {final_score} | Onda: {wave}\n")

def get_user_name():
    name = ""
    getting_name = True
    while getting_name:
        draw_bg()
        draw_text("DIGITE SEU NOME:", font40, white, 130, 300)
        draw_text(name, font40, green, 150, 400)
        draw_text("Aperte ENTER para iniciar", font30, white, 130, 500)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) > 0:
                    getting_name = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 15: # Limite de caracteres
                        name += event.unicode
        
        pygame.display.update()
        clock.tick(fps)
    return name

# Classes 
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
        cooldown = 500 
        game_over = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed
        
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser_fx.play()
            balas = Balas(self.rect.centerx, self.rect.top)
            balas_grupo.add(balas)
            self.last_shot = time_now

        self.mask = pygame.mask.from_surface(self.image)
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15 ))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15 ))
        elif self.health_remaining <= 0:
            explosao = Explosao(self.rect.centerx, self.rect.centery, 3)
            explosao_grupo.add(explosao)
            self.kill()
            game_over = -1
        return game_over

class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        global score # Acessa a pontuação global
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_grupo, True):
            self.kill()
            score += 10 # Adiciona pontos por alien
            explosao_fx.play()
            explosao = Explosao(self.rect.centerx, self.rect.centery, 2)
            explosao_grupo.add(explosao)

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        speed = 1 + (wave * 0.2)
        self.rect.x += self.move_direction * speed
        self.move_counter += self.move_direction * speed
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter = 0

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
            explosao2_fx.play()
            player.health_remaining -= 1 
            explosao = Explosao(self.rect.centerx, self.rect.centery, 1)
            explosao_grupo.add(explosao)

class Explosao(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"img/exp{num}.png")
            if size == 1: img = pygame.transform.scale(img, (20, 20))
            if size == 2: img = pygame.transform.scale(img, (40, 40))
            if size == 3: img = pygame.transform.scale(img, (160, 160))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosao_speed = 3
        self.counter += 1
        if self.counter >= explosao_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= explosao_speed:
            self.kill()

# Grupos
nave_grupo = pygame.sprite.Group()
balas_grupo = pygame.sprite.Group()
alien_grupo = pygame.sprite.Group()
alien_balas_grupo = pygame.sprite.Group()
explosao_grupo = pygame.sprite.Group()

def cria_aliens():
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_grupo.add(alien)

# Início do Jogo
user_name = get_user_name() # Pega o nome antes de começar
cria_aliens()
player = nave(int(screen_width / 2), screen_height - 100, 3)
nave_grupo.add(player)

score_saved = False
run = True
while run:
    clock.tick(fps)
    draw_bg()

    # --- HUD (Display de Pontos e Ondas) ---
    draw_text(f"Piloto: {user_name}", font30, white, 10, 10)
    draw_text(f"Score: {score}", font30, white, 10, 40)
    draw_text(f"Onda: {wave}", font30, white, screen_width - 120, 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if countdown == 0:
        time_now = pygame.time.get_ticks()
        # Tiro alienígena mais frequente conforme as ondas passam
        current_cooldown = max(alien_min_cooldown, alien_cooldown - ((wave - 1) * alien_cooldown_step))
        if time_now - last_alien_shot > current_cooldown and len(alien_balas_grupo) < 5 and len(alien_grupo) > 0:
            ataque_alien = random.choice(alien_grupo.sprites())
            alien_balas = Alien_Balas(ataque_alien.rect.centerx, ataque_alien.rect.bottom)
            alien_balas_grupo.add(alien_balas)
            last_alien_shot = time_now

        # SISTEMA DE ONDAS
        if len(alien_grupo) == 0:
            wave += 1
            cria_aliens()
            countdown = 3 # Pequena pausa entre ondas

        if game_over == 0:
            game_over = player.update()
            balas_grupo.update()
            alien_grupo.update()
            alien_balas_grupo.update()
        else:
            if game_over == -1:
                draw_text('GAME OVER', font40, white, int(screen_width/2 - 110), int(screen_height / 2))
                draw_text(f'Final Score: {score}', font30, green, int(screen_width/2 - 100), int(screen_height / 2 + 50))
                
                # Salva apenas uma vez quando morre
                if not score_saved:
                    save_score(user_name, score)
                    score_saved = True

    if countdown > 0:
        draw_text('PREPARE-SE!', font40, white, int(screen_width/2 - 110), int(screen_height / 2 + 50))
        draw_text(str(countdown), font40, white, int(screen_width/2 - 10), int(screen_height / 2 + 10))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer
   
    explosao_grupo.update()
    nave_grupo.draw(screen)
    balas_grupo.draw(screen)
    alien_grupo.draw(screen)
    alien_balas_grupo.draw(screen)
    explosao_grupo.draw(screen)

    pygame.display.update()

pygame.quit()