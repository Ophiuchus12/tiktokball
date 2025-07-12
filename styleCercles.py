import colorsys
from cercle import Cercle
import math
import random 
from balle import Balle
import numpy as np
import pygame


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(32)

from note_sounds import load_note_sounds




## Param 
## screen 
## theme -> style de cercles String
## min_radius -> int 
## spacing -> int 
## color -> rgb (x,x,x)
## return -> cerlces []

def generate_circle_colors(n):
    colors = []
    for i in range(n):
        hue = i / n
        r, g, b = colorsys.hsv_to_rgb(hue, 0.6, 1.0)
        colors.append((int(r * 255), int(g * 255), int(b * 255), 120))  # avec transparence
    return colors


note_sounds = load_note_sounds()

def chooseStyleGame(screen, theme, min_radius=10 ,spacing=15, color = (255,255,255), balles = []):

    cercles = []

    match theme : 
        case "unicolor":
            for i in range(100):
                radius = min_radius + i * spacing
                if 2 * radius < min(screen.get_width(), screen.get_height()):
                    start_deg = (i * 5) % 360  # Décalage progressif
                    end_deg = (start_deg + 20) % 360
                    cercles.append(Cercle(radius, start_deg, end_deg, color=color))


        case "multicolor":
            colors = generate_circle_colors(60)
            for i in range(60):
                radius = min_radius + i * spacing
                if 2 * radius < min(screen.get_width(), screen.get_height()):
                    start_deg = (i * 8) % 360
                    end_deg = (start_deg + 20) % 360
                    color = colors[i]
                    cercles.append(Cercle(radius, start_deg, end_deg, color=color[:3]))

        case "simpleCercle":
            if 2 * min_radius < min(screen.get_width(), screen.get_height()):
                start_deg = 320
                end_deg = 360
                cercles.append(Cercle(min_radius, start_deg, end_deg, color=(248, 0, 154)))

        case "simpleCercleferme":
            cercle1 = Cercle(radius, 0, 360, color=( 217, 15, 241 ))
            cercle1.close = True
            cercles.append(cercle1)

        case "infini" :
            TOTAL_CERCLES = 500
            DISPLAYED_CERCLES = 50
            all_cercles = []
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

        case "cageCercle" :
            #rayon 525
            rayon = 525
            cages = {
            1: (-20, 20),      # cage rouge
            2: (160, 200),     # cage rouge
            3: (20, 160),      # partie pleine blanche
            4: (200, 340)      # partie pleine blanche
        }

            cercle_cages = Cercle(rayon, 0, 360, color=(255, 255, 255), index=0, cages=cages)
            cercles.append(cercle_cages)
        
        case "cageCercle4":
            #rayon 525
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

        case "triple" :
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
                
                cercle = Cercle(rayon, start_deg, end_deg, color=( 30, 14, 255  ), x=x, y=y)
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
                    note_sounds=note_sounds,  
                    image_path=None, 
                    hidden_image=None, 
                    image_rect=None,
                    position=(x, y),
                    velocity=np.array([-8.0, -3.0]),  # balle statique au départ
                    rond=cercle
                )
                balles.append(balle)
    
    

    return cercles 

        
