from balle import Balle
from cercle import Cercle
import random
import math
import numpy as np


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

def interaction (screen, theme, mode, cercles, balles ):
    new_balles=[]
    balles_to_remove = []
    match theme :
        case "classique" :
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

        case "simpleCercleferme":
            for c in cercles:
                for b in balles:
                    passed = c.close_cercle_collision(b)

        case "rebondInfini":
            for c in cercles:
                for b in balles:
                    b.gravity_enabled = False
                    c.close_cercle_nogravity(b)

        case "simpleCercle":
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

        case "cageCercle":
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

        case "tripleCercle":
            frame_count = 0
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

        
        