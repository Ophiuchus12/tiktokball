import pygame
from balle import Balle
from carre import Carre
import numpy as np
import os
from note_sounds import load_note_sounds
import random

# --- Initialisation ---
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(32)

note_sounds = load_note_sounds()

pygame.mixer.music.load("music/bg10.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

ambient_sound = pygame.mixer.Sound("music/audio8.wav")
ambient_sound.set_volume(1.0)
ambient_sound.play()

screen = pygame.display.set_mode((1080, 1920), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF)

# --- Image cachée ---
hidden_image = pygame.image.load("images/rainbow.jpg").convert()
hidden_image = pygame.transform.scale(hidden_image, (600, 600))
image_rect = hidden_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

# --- Balle ---
ball = Balle(
    color=(0, 0, 0),
    colorIn=(0, 0, 0),
    note_sounds=note_sounds,
    image_path=None,
    hidden_image=hidden_image,
    image_rect=image_rect
)
balles = [ball]

# --- Carré ---
carre = Carre(300)

# --- Boucle principale ---
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # MAJ carré et dessin
    carre.update_angles()
    carre.draw(screen)

    # Gestion des balles
    for b in balles:
        b.update()
        carre.check_collision(b)
        b.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
