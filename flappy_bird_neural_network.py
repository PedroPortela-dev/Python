import pygame
import random
import numpy as np
import tensorflow as tf

# definir as constantes do jogo
WIDTH = 288
HEIGHT = 512
FPS = 60
GRAVITY = 0.25
JUMP_HEIGHT = -4
PIPE_GAP = 100
PIPE_WIDTH = 52

# definir as constantes da rede neural
INPUT_SIZE = 4
HIDDEN_SIZE = 4
OUTPUT_SIZE = 1
LEARNING_RATE = 0.1

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

# definir a função de ativação da rede neural
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# criar a classe da rede neural
class NeuralNetwork:
    def __init__(self):
        self.input_size = INPUT_SIZE
        self.hidden_size = HIDDEN_SIZE
        self.output_size = OUTPUT_SIZE

        self.W1 = np.random.randn(self.input_size, self.hidden_size)
        self.W2 = np.random.randn(self.hidden_size, self.output_size)

    def forward(self, x):
        self.z1 = np.dot(x, self.W1)
        self.a1 = sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.W2)
        self.a2 = sigmoid(self.z2)
        return self.a2

    def backward(self, x, y, output):
        self.error = y - output
        self.delta2 = self
