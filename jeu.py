import pygame
from balle import Balle
from cercle import Cercle
import math
import numpy as np
import random
import os
import subprocess
import shutil
from note_sounds import load_note_sounds
import time
import colorsys
from concurrent.futures import ThreadPoolExecutor


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(32)

note_sounds = load_note_sounds()

pygame.mixer.music.load("music/bg10.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# 🔊 Chargement d’une piste audio secondaire
ambient_sound = pygame.mixer.Sound("music/audio8.wav")  # ou .ogg
ambient_sound.set_volume(1.0)  # plus fort que la musique
ambient_sound.play()



screen = pygame.display.set_mode((1080, 1920), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF)
hidden_image = pygame.image.load("images/rainbow.jpg").convert()
hidden_image = pygame.transform.scale(hidden_image, (600, 600))  # ou autre taille
image_rect = hidden_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

pygame.display.set_caption("Multi Cercle Escape")
pygame.font.init()
font = pygame.font.SysFont(None, 60)
clock = pygame.time.Clock()

os.makedirs("frames", exist_ok=True)

ball1 = Balle(( 0, 0, 0 ), (0, 0, 0), note_sounds, image_path=None, hidden_image=hidden_image, image_rect=image_rect)

#ball2 = Balle((  255, 0, 143  ), (0, 0, 0), note_sounds, image_path=None)


balles = [ball1]

# Avant la boucle principale
logo1 = logo2 = None
logo_size = (140, 100 )

if os.path.exists("images/yes.png") and os.path.exists("images/no.png"):
    logo1 = pygame.image.load("images/yes.png").convert_alpha()
    logo2 = pygame.image.load("images/no.png").convert_alpha()

    logo1 = pygame.transform.scale(logo1, logo_size)
    logo2 = pygame.transform.scale(logo2, logo_size)



#---------------------color-------------------

# Plusieurs cercles concentriques
cercles = []
min_radius = 80
spacing = 15  # Espace entre les cercles
colorTheme = "simpleCercle"  # "unicolor" ou "multicolor"

def generate_circle_colors(n):
    colors = []
    for i in range(n):
        hue = i / n
        r, g, b = colorsys.hsv_to_rgb(hue, 0.6, 1.0)
        colors.append((int(r * 255), int(g * 255), int(b * 255), 120))  # avec transparence
    return colors


if colorTheme == "unicolor":
    for i in range(100):
        radius = min_radius + i * spacing
        if 2 * radius < min(screen.get_width(), screen.get_height()):
            start_deg = (i * 5) % 360  # Décalage progressif
            end_deg = (start_deg + 20) % 360
            cercles.append(Cercle(radius, start_deg, end_deg, color=(  160, 158, 158 )))

if colorTheme == "multicolor":
    colors = generate_circle_colors(60)
    for i in range(60):
        radius = min_radius + i * spacing
        if 2 * radius < min(screen.get_width(), screen.get_height()):
            start_deg = (i * 8) % 360
            end_deg = (start_deg + 20) % 360
            color = colors[i]
            cercles.append(Cercle(radius, start_deg, end_deg, color=color[:3]))


if colorTheme == "simpleCercle":
    radius = 400
    if 2 * radius < min(screen.get_width(), screen.get_height()):
        start_deg = 335
        end_deg = 360
        cercles.append(Cercle(radius, start_deg, end_deg, color=( 255, 0, 139  )))

if colorTheme == "simpleCercleferme":
    radius = 500
    cercle1 = Cercle(radius, 0, 360, color=(0, 0, 255))
    cercle1.close = True
    cercles.append(cercle1)


if colorTheme == "infini":
    TOTAL_CERCLES = 500
    DISPLAYED_CERCLES = 50
    all_cercles = []
    current_start_index = 0  # Index du premier cercle affiché
    colors = generate_circle_colors(500)
    # Préparation des cercles (juste les données, pas affichés tous en même temps)
    for i in range(TOTAL_CERCLES):
        start_deg = 320 + i
        end_deg = start_deg + 40
        rayon = 200 + i * 20
        color = colors[i]
        cercle = Cercle(rayon, start_deg, end_deg, color=color[:3], index=i)
        all_cercles.append(cercle)


    # Initialiser la première tranche affichée
    cercles = all_cercles[:DISPLAYED_CERCLES]



TOTAL_FRAMES = 60 * 85
frame_count = 0
running = True
mode = "simple"  # "double", "multi", "simple", "infini", "cercleferme"
countdown_start = time.time()
countdown_duration = 70 
theme = "simpleCercle"  # "classique" ou "simpleCercle"
nbBalles = 1  # une balle au départ

while running:
    screen.fill((0, 0, 0))



    spacing = 200  # espace horizontal entre les scores (ajuste cette valeur)
    y_position = 300  # position verticale
    if mode != "infini" and mode != "cercleferme":
        text = "Listen and tell me what you think ! \n"
        lines = text.split('\n')
        for i, line in enumerate(lines):
            rendered = font.render(line, True, ( 70, 0, 255  ))
            rect = rendered.get_rect(center=(screen.get_width() // 2, y_position - 100 + i * font.get_height()))
            screen.blit(rendered, rect)

        textBelow = "What do you think ? \n Share it with your friends"
        linesBelow = textBelow.split('\n')
        for i, line in enumerate(linesBelow):
            rendered = font.render(line, True, ( 70, 0, 255  ))
            rect = rendered.get_rect(center=(screen.get_width() // 2, y_position + 1400 + i * font.get_height()))
            screen.blit(rendered, rect)

    

    if mode == "double":
        total_width = len(balles) * spacing
        start_x = (screen.get_width() - total_width) // 2

        for idx, balle in enumerate(balles):
            score_text = font.render(f"Score: {balle.score}", True, balle.color)
            text_rect = score_text.get_rect()
            text_rect.topleft = (start_x + idx * spacing, y_position)
            screen.blit(score_text, text_rect)

        # Positionnement des images
        if logo1 and logo2:
            logo_y = y_position
            logo1_x = start_x - logo_size[0] - 10
            logo2_x = start_x + (len(balles) - 1) * spacing + text_rect.width + 10

            screen.blit(logo1, (logo1_x, logo_y))
            screen.blit(logo2, (logo2_x, logo_y))

    if mode == "multi":
        # Calcul du temps restant (compte à rebours)
        elapsed = time.time() - countdown_start
        remaining = max(0, countdown_duration - int(elapsed))  # jamais négatif
        minutes = remaining // 60
        seconds = remaining % 60
        timer_text_str = f"Timer: {minutes:02d}:{seconds:02d}"

        timer_text = font.render(timer_text_str, True, (  237, 187, 153 ))
        timer_rect = timer_text.get_rect(center=(screen.get_width() // 2, y_position))
        screen.blit(timer_text, timer_rect)

    if mode == "simple":
        balle = balles[0]
        score_text = font.render(f"Score: {nbBalles}", True, (  255, 151, 0 ))
        text_rect = score_text.get_rect(center=(screen.get_width() // 2, y_position))
        screen.blit(score_text, text_rect)

        elapsed = time.time() - countdown_start
        remaining = max(0, countdown_duration - int(elapsed))  # jamais négatif
        minutes = remaining // 60
        seconds = remaining % 60
        timer_text_str = f"Timer: {minutes:02d}:{seconds:02d}"

        timer_text = font.render(timer_text_str, True, (  174, 180, 159 ))
        timer_rect = timer_text.get_rect(center=(screen.get_width() // 2, y_position+50))
        screen.blit(timer_text, timer_rect)

    if mode == "infini":
        shadow = font.render(f"{current_start_index}", True, (255,255,255))
        shadow_rect = shadow.get_rect(center=(screen.get_width() // 2 + 2, screen.get_height() // 2 + 2))
        screen.blit(shadow, shadow_rect)
        passed_text = font.render(f"{current_start_index}", True, (255, 151, 0))
        passed_rect = passed_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(passed_text, passed_rect)
    
    if mode =="simpleCercleferme":
        elapsed = time.time() - countdown_start
        remaining = max(0, countdown_duration - int(elapsed))  # jamais négatif
        minutes = remaining // 60
        seconds = remaining % 60
        timer_text_str = f"Timer: {minutes:02d}:{seconds:02d}"
        timer_text = font.render(timer_text_str, True, (  174, 180, 159 ))
        timer_rect = timer_text.get_rect(center=(screen.get_width() // 2, y_position+50))
        screen.blit(timer_text, timer_rect)
    
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if frame_count >= TOTAL_FRAMES:
        running = False

    # Met à jour chaque cercle
    for c in cercles:
        c.update_angles()

    # Supprime les cercles qui sont "morts"
    cercles = [c for c in cercles if c.update_mort()]

    # Met à jour la ball1e
    for b in balles:
        b.update()
 
    # Liste temporaire pour les duplications
    new_balles = []

    # Vérifie collision avec chaque cercle actif
    if theme == "classique":
        for c in cercles:
            for b in balles:
                passed = c.check_collision(b)
                if passed and mode == "multi":
                    clone = b.clone()
                    new_balles.append(clone)
        
        balles.extend(new_balles)

    if theme == "simpleCercleferme":
        for c in cercles:
            for b in balles:
                passed = c.close_cercle_collision(b)


    if theme == "simpleCercle":
        balles_to_remove = []
        new_balles = []
        for c in cercles:
            for b in balles:
                passed = c.check_collision_simple(b)
                if passed and mode == "simple" and b.active:
                    
                    
                    clone1 = b.clone()
                    
                    
                    clone2 = b.clone()
                    
                    
                    new_balles.append(clone1)
                    new_balles.append(clone2)

                    nbBalles += 1  # <- incrémente le score ici
                    b.active = False  # désactive la balle originale

                if (
                    b.position[0] < 0 or b.position[0] > screen.get_width() or
                    b.position[1] < 0 or b.position[1] > screen.get_height()
                ):
                    balles_to_remove.append(b) 

        for b in balles_to_remove:
            if b in balles:
                balles.remove(b)

        balles.extend(new_balles)

    if theme == "infini":
        cercles_to_remove = []

        def test_collision(c):
            for b in balles:
                if c.check_collision(b) and mode == "infini":
                    return c
            return None

        with ThreadPoolExecutor() as executor:
            results = executor.map(test_collision, cercles)
            cercles_to_remove = [c for c in results if c]


        if cercles_to_remove:
            current_start_index += len(cercles_to_remove)
            cercles = all_cercles[current_start_index:current_start_index + DISPLAYED_CERCLES]

            if len(cercles) >= 2:
                premier_cercle = cercles[0]
                dernier_cercle = cercles[-1]

                distance_rayon = dernier_cercle.rayon - premier_cercle.rayon

                # Calcul de la distance attendue entre premier et dernier cercle
                expected_distance = (DISPLAYED_CERCLES - 1) * spacing

                if distance_rayon > expected_distance:
                    # Ajuster le rayon du dernier cercle pour qu'il respecte l'espacement
                    dernier_cercle.rayon = premier_cercle.rayon + expected_distance


        # --- RÉDUCTION DYNAMIQUE DES CERCLES ---
        if cercles:
            smallest_radius = min(c.rayon for c in cercles)
            if smallest_radius > min_radius:
                for i, c in enumerate(cercles):
                    c.rayon -= 4

                for i in range(1, len(cercles)):
                    prev = cercles[i - 1]
                    current = cercles[i]
                    actual_spacing = current.rayon - prev.rayon
                    if actual_spacing > spacing:
                        current.rayon -= 1

            cercles.sort(key=lambda c: c.rayon)



        

    # Dessine tout
    for c in cercles:
        c.draw(screen)

    for b in balles:
        b.draw(screen)



    pygame.display.update()
    clock.tick(60)
    frame_count += 1

pygame.quit()

