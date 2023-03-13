import pygame
import random

# definir as constantes do jogo
WIDTH = 288
HEIGHT = 512
FPS = 60
GRAVITY = 0.25
JUMP_HEIGHT = -4
PIPE_GAP = 100

# inicializar o Pygame
pygame.init()

# criar a tela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# definir as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# carregar os sprites do jogo
bird_image = pygame.image.load("bird.png").convert_alpha()
pipe_image = pygame.image.load("pipe.png").convert_alpha()

# definir a classe Bird
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.vel = 0

    def update(self):
        self.vel += GRAVITY
        self.rect.y += self.vel

        if self.rect.top < 0:
            self.rect.top = 0
            self.vel = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel = 0

    def jump(self):
        self.vel = JUMP_HEIGHT

# definir a classe Pipe
class Pipe(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe_image
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = WIDTH

    def update(self):
        self.rect.left -= 3

# criar os grupos de sprites
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

# criar o pássaro
bird = Bird()
all_sprites.add(bird)

# definir o loop principal do jogo
running = True
while running:
    # manter o loop rodando na velocidade correta
    clock.tick(FPS)

    # lidar com os eventos do teclado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    # criar novos canos
    if len(pipes) < 5:
        pipe_top = Pipe(0)
        pipe_bottom = Pipe(pipe_top.rect.bottom + PIPE_GAP)
        pipes.add(pipe_top)
        pipes.add(pipe_bottom)
        all_sprites.add(pipe_top)
        all_sprites.add(pipe_bottom)

    # atualizar os sprites
    all_sprites.update()

    # verificar colisões com os canos
    hits = pygame.sprite.spritecollide(bird, pipes, False)
    if hits:
        running = False

    # desenhar os sprites na tela
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # atualizar a tela
    pygame.display.flip()

# finalizar o Pygame
pygame.quit()
