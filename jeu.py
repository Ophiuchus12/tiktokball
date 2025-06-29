import pygame
from balle import Balle
from cercle import Cercle
import math
import numpy as np
import random
import os
from common import handleBallCollision
from interaction import interaction
from note_sounds import load_note_sounds
from concurrent.futures import ThreadPoolExecutor
from styleApparence import chooseMode
from styleCercles import chooseStyleGame


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(32)

note_sounds = load_note_sounds()



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



ball1 = Balle(90,(205, 1, 23), (0, 0, 0), note_sounds, image_path='images/toulouse.png', position =np.array([540.0, 600.0]), velocity= np.array([vx, vy]),cage=2)
ball2 = Balle(90,(89, 24, 52 ), (0, 0, 0), note_sounds, image_path='images/bordeaux.png', position=np.array([580.0, 600.0]),velocity= np.array([-vx, vy]),cage=1)
#ball3 = Balle(60,( 163, 167, 162 ), (0, 0, 0), note_sounds, image_path='images/mercedes.png', position=np.array([520.0, 600.0]),velocity= np.array([-vx, vy]),cage=3)
#ball4 = Balle(60,( 255, 154, 0), (0, 0, 0), note_sounds, image_path='images/maclaren.png', position=np.array([480.0, 600.0]),velocity= np.array([-vx, vy]),cage=4)

ball0 = Balle(20,( 0,0,0 ), (0, 0, 0), note_sounds, image_path='images/rugby.png', position=np.array([560.0, 600.0]),velocity= np.array([vx, vy]),cage=0)
ball0.gravity_enabled = False  



balles = [ball1, ball2, ball0  ]

# Avant la boucle principale
logo1 = logo2 = None
logo_size = (120, 100)

if os.path.exists("images/barca.png") and os.path.exists("images/rm.png"):
    logo1 = pygame.image.load("images/toulouse.png").convert_alpha()
    logo2 = pygame.image.load("images/bordeaux.png").convert_alpha()
    logo3 = pygame.image.load("images/mercedes.png").convert_alpha()
    logo4 = pygame.image.load("images/maclaren.png").convert_alpha()


    logo1 = pygame.transform.scale(logo1, logo_size)
    logo2 = pygame.transform.scale(logo2, logo_size)
    logo3 = pygame.transform.scale(logo3, logo_size)
    logo4 = pygame.transform.scale(logo4, logo_size)




#---------------------cercles init-------------------

cercles = []

cercles = chooseStyleGame(screen, theme = "cageCercle", min_radius=80, spacing=15, color= (255,0,0))






TOTAL_FRAMES = 60 * 85
running = True
mode = None  # "double", "multi", "simple", "infini", "simpleCercleferme"
visu = "clean"  

countdown_duration = 60 
theme = "cageCercle"  # "classique" ou "simpleCercle"
nbBalles = 1  # une balle au départ
rotate = "none"  #rotateCercles
collision = True 

background_image = pygame.image.load("images/terrain3.jpg").convert()
background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

# capture_image = pygame.image.load("images/losetime.png").convert_alpha()
capture_image = None  
#capture_image = False
# Optionnel : redimensionne si besoin, par exemple largeur max 500 px
max_width = 500
if capture_image:
    if capture_image.get_width() > max_width:
        
        capture_image = pygame.transform.smoothscale(capture_image, (800,100))







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
    frame_count=0
    screen.blit(background_image, (0, 0))

    chooseMode(screen, mode = "double", countdown_duration=60, balles = balles, visu = None, logo1=logo1, logo2=logo2)

    if mode == "infini":
        shadow = font.render(f"{current_start_index}", True, (255,255,255))
        shadow_rect = shadow.get_rect(center=(screen.get_width() // 2 + 2, screen.get_height() // 2 + 2))
        screen.blit(shadow, shadow_rect)
        passed_text = font.render(f"{current_start_index}", True, (255, 151, 0))
        passed_rect = passed_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(passed_text, passed_rect)
    
 
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


    interaction (screen,theme = "cageCercle",mode = "simple", cercles=cercles, balles= balles )
        

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

    if collision == True :
        handleBallCollision(balles)


    # Dessine tout
    for c in cercles:
        c.draw(screen)

    for b in balles:
        b.draw(screen)



    pygame.display.update()
    clock.tick(60)
    frame_count += 1

pygame.quit()

