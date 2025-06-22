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

# pygame.mixer.music.load("music/background2.mp3")
# pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play(-1)

# 🔊 Chargement d’une piste audio secondaire
# ambient_sound = pygame.mixer.Sound("music/audio8.wav")  # ou .ogg
# ambient_sound.set_volume(1.0)  # plus fort que la musique
# ambient_sound.play()



screen = pygame.display.set_mode((1080, 1920), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF)
hidden_image = pygame.image.load("images/logo.png").convert()
hidden_image = pygame.transform.scale(hidden_image, (600, 600))  # ou autre taille
image_rect = hidden_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

pygame.display.set_caption("Multi Cercle Escape")
pygame.font.init()
font = pygame.font.Font("font/symbola/Symbola.ttf", 60)
#font.set_bold(True)

clock = pygame.time.Clock()

os.makedirs("frames", exist_ok=True)

angle = random.uniform(0, 2 * math.pi)
vitesse = 20

vx = math.cos(angle) * vitesse
vy = math.sin(angle) * vitesse


#balle pour cercle ferme avec traits 
# ball1 = Balle(60,(  231, 76, 60  ), ( 231, 76, 60 ), note_sounds, image_path=None, hidden_image=None, image_rect=None, velocity= np.array([vx, vy]))
# ball2 = Balle(60,(  46, 134, 193  ), (  46, 134, 193  ), note_sounds, image_path=None, hidden_image=None, image_rect=None, velocity= np.array([vx+2, vy+2]))
# ball3 = Balle(60,(  244, 208, 63 ), ( 244, 208, 63 ), note_sounds, image_path=None, hidden_image=None, image_rect=None, velocity= np.array([vx+2, vy+2]))
# ball4 = Balle(60,( 22, 160, 133 ), ( 22, 160, 133 ), note_sounds, image_path=None, hidden_image=None, image_rect=None, velocity= np.array([vx+2, vy+2]))



ball1 = Balle(90,(205, 1, 23), (0, 0, 0), note_sounds, image_path='images/rct.png', position =np.array([540.0, 600.0]), velocity= np.array([vx, vy]),cage=2)
ball2 = Balle(90,(89, 24, 52 ), (0, 0, 0), note_sounds, image_path='images/bordeaux.png', position=np.array([580.0, 600.0]),velocity= np.array([-vx, vy]),cage=1)
#ball3 = Balle(60,( 163, 167, 162 ), (0, 0, 0), note_sounds, image_path='images/mercedes.png', position=np.array([520.0, 600.0]),velocity= np.array([-vx, vy]),cage=3)
#ball4 = Balle(60,( 255, 154, 0), (0, 0, 0), note_sounds, image_path='images/maclaren.png', position=np.array([480.0, 600.0]),velocity= np.array([-vx, vy]),cage=4)

ball0 = Balle(20,( 0,0,0 ), (0, 0, 0), note_sounds, image_path='images/rugby.png', position=np.array([560.0, 600.0]),velocity= np.array([vx, vy]),cage=0)
ball0.gravity_enabled = False  



balles = [ ]

# Avant la boucle principale
logo1 = logo2 = None
logo_size = (120, 100 )

if os.path.exists("images/barca.png") and os.path.exists("images/rm.png"):
    logo1 = pygame.image.load("images/rct.png").convert_alpha()
    logo2 = pygame.image.load("images/bordeaux.png").convert_alpha()
    logo3 = pygame.image.load("images/mercedes.png").convert_alpha()
    logo4 = pygame.image.load("images/maclaren.png").convert_alpha()


    logo1 = pygame.transform.scale(logo1, logo_size)
    logo2 = pygame.transform.scale(logo2, logo_size)
    logo3 = pygame.transform.scale(logo3, logo_size)
    logo4 = pygame.transform.scale(logo4, logo_size)




#---------------------color-------------------

# Plusieurs cercles concentriques
cercles = []
min_radius = 80
spacing = 15  # Espace entre les cercles
colorTheme = "triple"  # "unicolor" ou "multicolor"

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
            end_deg = (start_deg + 30) % 360
            cercles.append(Cercle(radius, start_deg, end_deg, color=( 160, 64, 0 )))

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
    radius = 500
    if 2 * radius < min(screen.get_width(), screen.get_height()):
        start_deg = 320
        end_deg = 360
        cercles.append(Cercle(radius, start_deg, end_deg, color=(248, 0, 154)))

if colorTheme == "simpleCercleferme":
    radius = 500
    cercle1 = Cercle(radius, 0, 360, color=( 217, 15, 241 ))
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

if colorTheme == "cageCercle":
    rayon = 525
    cages = {
        1: (-20, 20),      # cage rouge
        2: (160, 200),     # cage rouge
        3: (20, 160),      # partie pleine blanche
        4: (200, 340)      # partie pleine blanche
    }

    cercle_cages = Cercle(rayon, 0, 360, color=(255, 255, 255), index=0, cages=cages)
    cercles.append(cercle_cages)

if colorTheme == "cageCercle4":
    rayon = 525
    cages = {
        1: (0, 40),         # Cage rouge
        2: (90, 130),       # Cage rouge
        3: (180, 220),      # Cage rouge
        4: (270, 310),      # Cage rouge

        5: (40, 90),        # Zone blanche pleine
        6: (130, 180),      # Zone blanche pleine
        7: (220, 270),      # Zone blanche pleine
        8: (310, 360)       # Zone blanche pleine
    }

    cercle_cages = Cercle(rayon, 0, 360, color=(255, 255, 255), index=0, cages=cages)
    cercles.append(cercle_cages)



# if colorTheme == "multiCercleFerme":
#     for i in range(100):
#         radius = min_radius + i * spacing
#         if 2 * radius < min(screen.get_width(), screen.get_height()):
#             cercle = Cercle(radius, 0, 360, color=(  248, 0, 154  ))
#             cercle.close = True
#             cercles.append(cercle)

if colorTheme == "triple":
    rayon = 250
    cx, cy = 540, 960
    angle_offset = math.radians(120)
    
    for i in range(3):
        angle = i * angle_offset
        x = cx + 1.15 * rayon * math.cos(angle)
        y = cy + 1.15 * rayon * math.sin(angle)
        
        # Calcul de l'angle vers le centre
        angle_vers_centre = math.atan2(cy - y, cx - x)
        
        # Span d'ouverture pour créer une connexion entre les cercles
        arc_span = math.radians(30)  # Augmenté pour permettre la connexion
        
        # Inverser l'ouverture pour les deux cercles de gauche (indices 1 et 2)
        if i == 1:
            angle_vers_centre += (math.pi)/1.5  # Inverse la direction

        if i ==2 :
            angle_vers_centre -= (math.pi)/1.5
        
        # Les angles d'ouverture sont centrés sur la direction vers le centre
        start_deg = math.degrees(angle_vers_centre - arc_span / 2)
        end_deg = math.degrees(angle_vers_centre + arc_span / 2)
        
        cercle = Cercle(rayon, start_deg, end_deg, color=( 25, 207, 172 ), x=x, y=y)
        cercle.rotation_direction = 1 if i % 2 == 0 else -1
        cercles.append(cercle)
        
        balle = Balle(
            10,
            (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            ),  
            (255, 255, 255),
            note_sounds,
            image_path=None, 
            hidden_image=None, 
            image_rect=None,
            position=(x, y),
            velocity=np.array([-10.0, -5.0]),  # balle statique au départ
            rond=cercle
        )
        balles.append(balle)





TOTAL_FRAMES = 60 * 85
frame_count = 0
running = True
mode = "simple"  # "double", "multi", "simple", "infini", "simpleCercleferme"
visu = "clean"  
countdown_start = time.time()
countdown_duration = 60 
theme = "tripleCercle"  # "classique" ou "simpleCercle"
nbBalles = 1  # une balle au départ
rotate = "none"  #rotateCercles

background_image = pygame.image.load("images/etoile.jpeg").convert()
background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

# capture_image = pygame.image.load("images/losetime.png").convert_alpha()
capture_image = None  
#capture_image = False
# Optionnel : redimensionne si besoin, par exemple largeur max 500 px
max_width = 500
if capture_image:
    if capture_image.get_width() > max_width:
        
        capture_image = pygame.transform.smoothscale(capture_image, (800,100))


def check_balls_collision(b1, b2):
    direction = b2.position - b1.position
    distance = np.linalg.norm(direction)
    sum_radius = b1.radius + b2.radius

    return distance < sum_radius

def resolve_ball_collision(ball1, ball2):
    direction = ball2.position - ball1.position
    distance = np.linalg.norm(direction)

    if distance == 0:
        return  # éviter division par zéro

    # Normalisation
    normal = direction / distance

    # Vitesse relative
    relative_velocity = ball2.velocity - ball1.velocity

    # Projeter la vitesse relative sur la normale
    velocity_along_normal = np.dot(relative_velocity, normal)

    if velocity_along_normal >= 0:
        return  # Les balles s’éloignent déjà

    # Masse (si tu veux généraliser plus tard, ici masses égales)
    restitution = 1.0  # collision parfaitement élastique

    # Impulsion scalaire
    impulse_scalar = -(1 + restitution) * velocity_along_normal / 2
    impulse = impulse_scalar * normal

    # Appliquer l'impulsion (conservation quantité de mouvement)
    ball1.velocity -= impulse
    ball2.velocity += impulse

    # Correction position : éviter que les balles restent collées
    overlap = (ball1.radius + ball2.radius) - distance
    if overlap > 0:
        correction = normal * (overlap / 2)
        ball1.position -= correction
        ball2.position += correction

    # Optionnel : déclencher effet rebond visuel/sonore
    ball1.on_bounce()
    ball2.on_bounce()


def reset_all_balls(balls, vitesse=15, radius=100):
    """
    Réinitialise les positions et vitesses des balles autour du centre de l'écran.
    
    - balls : liste des balles
    - vitesse : vitesse initiale de chaque balle
    - radius : distance autour du centre pour éviter la superposition
    """
    center = np.array([540.0, 960.0])
    n = len(balls)

    for i, ball in enumerate(balls):
        # Répartir les balles uniformément en cercle autour du centre
        angle_pos = (2 * math.pi / n) * i
        pos_offset = np.array([math.cos(angle_pos), math.sin(angle_pos)]) * radius
        ball.position = center + pos_offset

        # Générer une direction aléatoire pour la vitesse
        angle_vel = random.uniform(0, 2 * math.pi)
        vx = math.cos(angle_vel) * vitesse
        vy = math.sin(angle_vel) * vitesse
        ball.velocity = np.array([vx, vy])

        ball.gravity_enabled = False  # ou True selon besoin




def rotate_cercles_orbital(cercles, center_x, center_y, rotation_speed, rotation_direction):
    """Les centres des cercles tournent autour du centre écran, ouvertures restent vers le centre"""
    angle = rotation_speed * rotation_direction
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    
    for i, cercle in enumerate(cercles):
        # 1. Faire tourner la POSITION du centre du cercle autour du centre écran
        dx = cercle.x - center_x
        dy = cercle.y - center_y
        
        new_dx = dx * cos_a - dy * sin_a
        new_dy = dx * sin_a + dy * cos_a
        
        cercle.x = center_x + new_dx
        cercle.y = center_y + new_dy
        
        # 2. Recalculer l'angle vers le centre pour cette nouvelle position
        angle_vers_centre = math.atan2(center_y - cercle.y, center_x - cercle.x)
        
        # 3. Appliquer les ajustements spécifiques selon ton code original
        if i == 1:
            angle_vers_centre += (math.pi)/1.5  # Ajustement pour cercle 1
        if i == 2:
            angle_vers_centre -= (math.pi)/1.5  # Ajustement pour cercle 2
        
        # 4. Recalculer les angles d'ouverture avec ton arc_span original
        arc_span = math.radians(40)  # Utilise ta valeur originale
        start_deg = math.degrees(angle_vers_centre - arc_span / 2)
        end_deg = math.degrees(angle_vers_centre + arc_span / 2)
        
        # 5. Mettre à jour les angles du cercle (en radians)
        cercle.start_angle = math.radians(start_deg)
        cercle.end_angle = math.radians(end_deg)

        
        
        
        



while running:
    screen.blit(background_image, (0, 0))




    spacing = 300  # espace horizontal entre les scores (ajuste cette valeur)
    y_position = 300  # position verticale
    if mode != "infini" and mode != "simpleCercleferme" and mode !="quadruple":

        if capture_image:# Positionner la capture horizontale centrée en X, et juste au-dessus du cercle
            circle_image_x = screen.get_width() // 2 - (capture_image.get_width()/2)
            circle_image_y =  y_position + 10  # à ajuster selon ton cercle


            screen.blit(capture_image, (circle_image_x, circle_image_y))

        text = "+ 1 ball for each circle change​​\n​ "
        lines = text.split('\n')
        

        max_width = 0
        total_height = 0
        rendered_lines = []

        for i, line in enumerate(lines):
            rendered = font.render(line, True, (0, 0, 0))
            rendered_lines.append(rendered)
            rect = rendered.get_rect()
            max_width = max(max_width, rect.width)
            total_height += rect.height

        # Coordonnées du fond
        padding = 10
        bg_rect = pygame.Rect(
            (screen.get_width() - max_width) // 2 - padding // 2,
            y_position - 200 - padding // 2,
            max_width + padding,
            total_height + padding
        )

        # Dessine le fond blanc
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=15)

        # Affiche les lignes par-dessus
        for i, rendered in enumerate(rendered_lines):
            rect = rendered.get_rect(center=(screen.get_width() // 2, y_position - 150 + i * font.get_height()))
            screen.blit(rendered, rect)

        textBelow = "Like and subscribe ​​\n I follow back 💪​"
        linesBelow = textBelow.split('\n')
        for i, line in enumerate(linesBelow):
            rendered = font.render(line, True, ( 255, 255, 255 ))
            rect = rendered.get_rect(center=(screen.get_width() // 2, y_position + 1400 + i * font.get_height()))
            screen.blit(rendered, rect)

    

    if mode == "double":
        total_width = (len(balles)-1) * spacing
        start_x = ((screen.get_width() - total_width) // 2) -250

        score_y_position = y_position + 1250  

        for idx, balle in enumerate(balles):
            if balle.cage != 0:
                score_text = font.render(f"Score: {balle.score}", True, balle.color)
                text_rect = score_text.get_rect()
                text_rect.topleft = (start_x + idx * spacing, score_y_position)
                screen.blit(score_text, text_rect)

        # Positionnement des images
        if logo1 and logo2:
            logo_y = score_y_position  # même ligne que les scores

            # Trouve les indexes de ball1 et ball2
            ball1_index = balles.index(ball1)
            ball2_index = balles.index(ball2)

            logo1_x = start_x + ball1_index * spacing - logo_size[0] - 10
            logo2_x = start_x + ball2_index * spacing + 250  # décalage à droite du score

            screen.blit(logo1, (logo1_x, logo_y))
            screen.blit(logo2, (logo2_x, logo_y))

        elapsed = time.time() - countdown_start
        remaining = max(0, countdown_duration - int(elapsed))  # jamais négatif
        minutes = remaining // 60
        seconds = remaining % 60
        timer_text_str = f"Timer: {minutes:02d}:{seconds:02d}"
        timer_text = font.render(timer_text_str, True, (  255, 255, 255 ))
        timer_rect = timer_text.get_rect(center=(screen.get_width() // 2, y_position+30))
        screen.blit(timer_text, timer_rect)

    if mode == "quadruple":
        cols = 2
        rows = 2
        spacing_x = 300  # Espace horizontal entre colonnes
        spacing_y = 100  # Espace vertical entre lignes
        start_x = (screen.get_width() - (cols - 1) * spacing_x) // 2
        score_y_position = y_position + 1250

        # Logos associés à balles[1] à balles[4]
        logos = [logo1, logo2, logo3, logo4]

        offset_x = -80

        for display_idx, balle_idx in enumerate(range(1, 5)):  # de balle[1] à balle[4]
            balle = balles[balle_idx]
            logo = logos[display_idx]

            if balle.cage != 0:
                col = display_idx % cols
                row = display_idx // cols
                x = start_x + col * spacing_x + offset_x
                y = score_y_position + row * spacing_y

                # Créer le texte du score
                score_text = font.render(f"Score: {balle.score}", True, balle.color)
                text_rect = score_text.get_rect()

                if col == 0:
                    # Logo à gauche
                    logo_x = x - logo_size[0] - 10
                    text_rect.topleft = (x, y)
                    screen.blit(score_text, text_rect)
                    if logo:
                        screen.blit(logo, (logo_x, y))
                else:
                    # Logo à droite
                    text_rect.topleft = (x, y)
                    screen.blit(score_text, text_rect)
                    logo_x = x + text_rect.width + 10
                    if logo:
                        screen.blit(logo, (logo_x, y))



        text = "Formula 1 Grand Prix of Canada​​​ \n\n Tell me your prediction in the comments"
        lines = text.split('\n')
        

        for i, line in enumerate(lines):
            rendered = font.render(line, True, ( 34, 201, 168 ))
            rect = rendered.get_rect(center=(screen.get_width() // 2, y_position - 200 + i * font.get_height()))
            screen.blit(rendered, rect)

        elapsed = time.time() - countdown_start
        remaining = max(0, countdown_duration - int(elapsed))  # jamais négatif
        minutes = remaining // 60
        seconds = remaining % 60
        timer_text_str = f"Timer: {minutes:02d}:{seconds:02d}"
        timer_text = font.render(timer_text_str, True, (  255, 255, 255 ))
        timer_rect = timer_text.get_rect(center=(screen.get_width() // 2, y_position+30))
        screen.blit(timer_text, timer_rect)

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
        if visu != "clean":
            balle = balles[0]
            score_text = font.render(f"Score: {nbBalles}", True, ( 214, 234, 248  ))
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
    if theme != "tripleCercle":
        for c in cercles:
            c.update_angles()
    elif theme == "tripleCercle" and rotate == "rotateCercles" :
        center_x, center_y = screen.get_width() // 2, screen.get_height() // 2
        rotate_cercles_orbital(cercles, center_x, center_y, 0.01, -1)

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
                if passed :
                    for c in cercles:
                        c.rotation_direction *= -1 
                        c.rotation_speed = random.uniform(0.005, 0.01)  # Réinitialise la vitesse de rotation
                if passed and mode == "multi":
                    clone = b.clone()
                    new_balles.append(clone)
        
        balles.extend(new_balles)

    if theme == "simpleCercleferme":
        for c in cercles:
            for b in balles:
                passed = c.close_cercle_collision(b)

    if theme == "rebondInfini":
        for c in cercles:
            for b in balles:
                b.gravity_enabled = False
                c.close_cercle_nogravity(b)



    if theme == "simpleCercle":
        balles_to_remove = []
        new_balles = []
        for c in cercles:
            for b in balles:
                passed = c.check_collision_simple(b, center = np.array([c.x, c.y]))
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

    if theme == "cageCercle":
        any_goal = False  

        for c in cercles:
            for b in balles:
                b.gravity_enabled = False
                goal, teamScored = c.check_collision_cage(b)
                if goal:
                    any_goal = True
                    for b in balles:
                        if teamScored == b.cage:
                            b.score += 1
                    

        if any_goal:
            reset_all_balls(balles)


    if theme == "tripleCercle":
        balles_to_remove = []
        new_balles = []

        for b in balles:
            if not b.active:
                continue

            # Assignation de cage initiale si nécessaire
            if b.cage is None:
                # Trouve le cercle le plus proche
                closest_circle = None
                min_distance = float('inf')
                for c_init in cercles:
                    distance = np.linalg.norm(b.position - np.array([c_init.x, c_init.y]))
                    if distance < min_distance:
                        min_distance = distance
                        closest_circle = c_init
                b.cage = closest_circle

            # Vérification des passages vers d'autres cercles
            passage_detected = False
            for c in cercles:
                if c != b.cage:
                    # Vérifie si la balle entre dans un nouveau cercle
                    if c.check_passage_only(b):
                        
                        # Délai minimum entre changements de cage pour éviter l'oscillation
                        if frame_count - b.last_cage_change_frame > 2:  # Augmenté de 5 à 10
                            old_cage = b.cage
                            b.cage = c
                            b.last_cage_change_frame = frame_count
                            
                            # Ajustement de position plus doux
                            center_old = np.array([old_cage.x, old_cage.y])
                            center_new = np.array([c.x, c.y])
                            
                            # Calcule la direction d'entrée dans le nouveau cercle
                            entry_vector = b.position - center_new
                            entry_distance = np.linalg.norm(entry_vector)
                            
                            if entry_distance > 0:
                                # Place la balle légèrement à l'intérieur du nouveau cercle
                                normalized_entry = entry_vector / entry_distance
                                safe_distance = c.rayon - b.radius * 1.5  # Distance sécurisée
                                b.position = center_new + normalized_entry * safe_distance
                            
                            
                            passage_detected = True

                            clonedBalle = b.clone(position = np.array([old_cage.x, old_cage.y]))
                            clonedBalle.cage = old_cage
                            clonedBalle.last_cage_change_frame = frame_count
                            clonedBalle.color = (
                                random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255)
                            )

                            clonedBalle2 = b.clone(position = np.array([old_cage.x, old_cage.y]))
                            clonedBalle2.cage = old_cage
                            clonedBalle2.last_cage_change_frame = frame_count
                            clonedBalle2.color = (
                                random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255)
                            )
                            new_balles.append(clonedBalle)
                            new_balles.append(clonedBalle2)

                               
                            break

            # Collision avec la cage actuelle
            if not passage_detected and b.cage is not None:
                passed, passedBall =  b.cage.check_collision_triple(b)
                if passed and passedBall != None :
                    if (
                    passedBall.position[0] < 0 or passedBall.position[0] > screen.get_width() or
                    passedBall.position[1] < 0 or passedBall.position[1] > screen.get_height()
                    ):
                        balles_to_remove.append(passedBall)



            # Suppression des balles sorties de l'écran
            


        # Nettoie les balles supprimées
        for b in balles_to_remove:
            if b in balles:
                balles.remove(b)

        # Ajoute les nouvelles balles si nécessaire
        balles.extend(new_balles)



 


    if theme == "multiCercleFerme":
        for c in cercles:
            for b in balles:
                b.gravity_enabled = False
                c.close_cercles_break(b)






    # # Gère les collisions entre toutes les paires de balles
    # handled_pairs = set()
    # for i in range(len(balles)):
    #     for j in range(i + 1, len(balles)):
    #         if (i, j) not in handled_pairs:
    #             b1, b2 = balles[i], balles[j]
    #             if check_balls_collision(b1, b2):
    #                 resolve_ball_collision(b1, b2)
    #                 handled_pairs.add((i, j))


    # Dessine tout
    for c in cercles:
        c.draw(screen)

    for b in balles:
        b.draw(screen)



    pygame.display.update()
    clock.tick(60)
    frame_count += 1

pygame.quit()

