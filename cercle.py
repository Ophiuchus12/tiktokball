import pygame
import math
import numpy as np
import random

from note_sounds import load_note_sounds

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(32)

note_sounds = load_note_sounds()

rotate = "stuck"
onBounce = "cage"  # "linked" ou "none"
look = "none"


def reflect(velocity, normal):
        # R = V - 2 * (V • N) * N
        dot = velocity[0]*normal[0] + velocity[1]*normal[1]
        reflected = (
            velocity[0] - 2 * dot * normal[0],
            velocity[1] - 2 * dot * normal[1]
        )
        return reflected

class Cercle:
    def __init__(self, rayon, start_deg, end_deg, color=(255, 255, 255), index=0, cages=None, x=540.0, y=960.0):
        self.rayon = rayon
        self.start_angle = math.radians(start_deg)
        self.end_angle = math.radians(end_deg)
        self.active = True   #cercle apparait
        self.color = color
        self.dying = False
        self.death_timer = 0
        self.shards = []
        self.cages = cages if cages else {}
        self.x = x
        self.y = y


        if rotate == "free":
            self.rotation_speed = random.uniform(0.005, 0.01)
            self.rotation_direction = random.choice([-1, 1])  # -1 : anti-horaire, 1 : horaire
        
        elif rotate == "stuck":
            self.rotation_speed = 0.01
            self.rotation_direction = -1

        self.index = index  # <- nouvel attribut
        self.close = False  # Indique si le cercle est fermé

    def update_angles(self):
        delta = self.rotation_speed * self.rotation_direction

        # Tourne les angles en radians
        self.start_angle += delta
        self.end_angle += delta

        # Fait tourner aussi les cages
        if self.cages:
            new_cages = {}
            for index, (start_deg, end_deg) in self.cages.items():
                start_deg = (start_deg + math.degrees(delta)) % 360
                end_deg = (end_deg + math.degrees(delta)) % 360
                new_cages[index] = (start_deg, end_deg)
            self.cages = new_cages

    def rotate_around_center(self, center_x, center_y):
        """Fait tourner uniquement la position du cercle autour du centre de l'écran, sans changer les angles."""
        dx = self.x - center_x
        dy = self.y - center_y

        angle = self.rotation_speed * self.rotation_direction

        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        new_dx = dx * cos_a - dy * sin_a
        new_dy = dx * sin_a + dy * cos_a

        self.x = center_x + new_dx
        self.y = center_y + new_dy



    def update_radius(self, new_radius):
        self.rayon = new_radius

    def check_collision(self, ball):
        if not self.active:
            return

        center = np.array([540.0, 960.0])
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        if distance + ball.radius >= self.rayon:
            if distance != 0:
                angle = math.degrees(math.atan2(-direction[1], direction[0])) % 360
                start_deg = math.degrees(self.start_angle) % 360
                end_deg = math.degrees(self.end_angle) % 360

                in_hole = False
                if start_deg < end_deg:
                    in_hole = start_deg <= angle <= end_deg
                else:
                    in_hole = angle >= start_deg or angle <= end_deg

                if in_hole:
                    ball.score += 1
                    if onBounce == "linked":
                        ball.rebonds_segments.clear() 
                        ball.velocity= np.array([random.randint(8,15)*2, random.randint(8,15)*2])

                    self.start_death()  # <- ici
                    return True

                else:
                    normal = direction / distance
                    ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal
                    overlap = (distance + ball.radius) - self.rayon
                    ball.position -= normal * overlap
                    ball.on_bounce()
        return False  

    def check_collision_simple(self, ball, center = np.array([540.0, 960.0])):
        if not self.active:
            return False

        center = center
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        if distance == 0:
            return False  # La balle est au centre : on ignore

        # Si la balle touche ou dépasse le bord
        if distance + ball.radius >= self.rayon:
            angle = math.degrees(math.atan2(-direction[1], direction[0])) % 360
            start_deg = math.degrees(self.start_angle) % 360
            end_deg = math.degrees(self.end_angle) % 360

            # Vérifie si la balle passe dans l'ouverture
            if start_deg < end_deg:
                in_hole = start_deg <= angle <= end_deg
            else:
                in_hole = angle >= start_deg or angle <= end_deg

            if in_hole:
                ball.score += 1
                return True
            else:
                # Calcul du rebond
                normal = direction / distance

                # Rebond : réflexion par rapport à la normale
                ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal

                # ✅ Repositionne exactement sur la courbe
                ball.position = center + normal * (self.rayon - ball.radius)

                ball.on_bounce()

                 # Ajuster la position du dernier segment pour qu'il soit sur la surface
                if onBounce == "linked" and len(ball.rebonds_segments) > 1:
                    last_segment = ball.rebonds_segments[-1]
                    seg_dir = last_segment[0] - center
                    seg_dist = np.linalg.norm(seg_dir)
                    if seg_dist != 0:
                        seg_dir /= seg_dist
                        # distance entre centre du cercle et centre de la balle
                        dist_center_to_ball = np.linalg.norm(ball.position - center)
                        # position du point sur la surface de la balle
                        last_segment[0] = center + seg_dir * (dist_center_to_ball + ball.radius)

        return False
    
    def check_collision_triple(self, ball):
        """Version améliorée de la collision pour éviter les rebonds multiples"""
        if not self.active:
            return False, None

        center = np.array([self.x, self.y], dtype=float)
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        if distance == 0:
            return False, None

        # Collision avec le bord du cercle
        if distance + ball.radius >= self.rayon:
            angle = math.degrees(math.atan2(-direction[1], direction[0])) % 360
            start_deg = math.degrees(self.start_angle) % 360
            end_deg = math.degrees(self.end_angle) % 360

            # Vérifie si c'est dans l'ouverture (passage libre)
            if start_deg < end_deg:
                in_hole = start_deg <= angle <= end_deg
            else:
                in_hole = angle >= start_deg or angle <= end_deg

            if in_hole:
                # Passage libre, on laisse passer
                ball.score += 1
                return True, ball
            else:
                # Rebond sur la paroi solide
                normal = direction / distance
                
                # Vérification pour éviter les rebonds multiples
                # Si la balle se dirige déjà vers l'extérieur, ne pas rebondir
                velocity_towards_surface = np.dot(ball.velocity, normal)
                if velocity_towards_surface <= 0:
                    return False, None  # La balle s'éloigne déjà
                
                # Effectuer le rebond
                ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal
                
                # Repositionner exactement sur la surface
                ball.position = center + normal * (self.rayon - ball.radius)
                
                ball.on_bounce()

                # Gestion des segments de rebond si activé
                if onBounce == "linked" and len(ball.rebonds_segments) > 1:
                    last_segment = ball.rebonds_segments[-1]
                    seg_dir = last_segment[0] - center
                    seg_dist = np.linalg.norm(seg_dir)
                    if seg_dist != 0:
                        seg_dir /= seg_dist
                        dist_center_to_ball = np.linalg.norm(ball.position - center)
                        last_segment[0] = center + seg_dir * (dist_center_to_ball + ball.radius)

        return False, None
    
    def check_passage_only(self, ball):
        """Version améliorée de la détection de passage"""
        if not self.active:
            return False

        center = np.array([self.x, self.y], dtype=float)
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        # Vérification si la balle est dans la zone d'influence du cercle
        # mais pas trop près (pour éviter les faux positifs)
        if self.rayon - ball.radius * 2 < distance < self.rayon + ball.radius * 2:
            angle = math.degrees(math.atan2(-direction[1], direction[0])) % 360
            start_deg = math.degrees(self.start_angle) % 360
            end_deg = math.degrees(self.end_angle) % 360

            # Vérifie si la balle est dans l'ouverture
            if start_deg < end_deg:
                in_hole = start_deg <= angle <= end_deg
            else:
                in_hole = angle >= start_deg or angle <= end_deg

            # Vérification supplémentaire : la balle se dirige-t-elle vers l'intérieur ?
            velocity_towards_center = np.dot(ball.velocity, -direction / distance) if distance > 0 else 0
            
            return in_hole and velocity_towards_center > 0

        return False





    
    def close_cercle_collision(self, ball):
        if not self.active:
            return False

        center = np.array([540.0, 960.0])
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        # Collision avec le bord intérieur du cercle
        if distance + ball.radius >= self.rayon:
            if distance != 0 and ball.radius < self.rayon:
                normal = direction / distance
                ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal

                # Correction du chevauchement
                overlap = (distance + ball.radius) - self.rayon
                ball.position -= normal * overlap

                ball.on_bounce()

                
                # Ajuster la position du dernier segment pour qu'il soit sur la surface
                if onBounce == "linked" and len(ball.rebonds_segments) > 1:
                    last_segment = ball.rebonds_segments[-1]
                    seg_dir = last_segment[0] - center
                    seg_dist = np.linalg.norm(seg_dir)
                    if seg_dist != 0:
                        seg_dir /= seg_dist
                        # distance entre centre du cercle et centre de la balle
                        dist_center_to_ball = np.linalg.norm(ball.position - center)
                        # position du point sur la surface de la balle
                        last_segment[0] = center + seg_dir * (dist_center_to_ball + ball.radius)

                # ball.velocity *= 1.02  # +x% de vitesse


        return False
    
    
    
    def close_cercle_nogravity(self, ball):
        if not self.active:
            return False

        center = np.array([540.0, 960.0])
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        if distance + ball.radius >= self.rayon:
            if distance != 0 and ball.radius < self.rayon:
                normal = direction / distance  # Normalisée
                ball.velocity = reflect(ball.velocity, normal)
                ball.on_bounce()

        return False
    

    def close_cercles_break(self, ball):
        if not self.active:
            return False

        center = np.array([540.0, 960.0])
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        if distance + ball.radius >= self.rayon:
            if distance != 0 and ball.radius < self.rayon:
                normal = direction / distance  # Normalisée
                ball.velocity = reflect(ball.velocity, normal)
                ball.on_bounce()
        
        return False
    
    def check_collision_cage(self, ball):
        if not self.active:
            return False, None

        center = np.array([540.0, 960.0])
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        if distance + ball.radius >= self.rayon:
            if distance != 0 and ball.radius < self.rayon:
                normal = direction / distance
                ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal
                overlap = (distance + ball.radius) - self.rayon
                ball.position -= normal * overlap
                ball.on_bounce()

                if onBounce == "cage":
                    # Convertir la position de la balle en angle (en radians)
                    angle = math.atan2(-direction[1], direction[0]) % (2 * math.pi)

                    for index, (start_deg, end_deg) in self.cages.items():
                        if index in [1, 2]:  # cages rouges et vertes
                            start_rad = math.radians(start_deg) % (2 * math.pi)
                            end_rad = math.radians(end_deg) % (2 * math.pi)

                            in_cage = False
                            if start_rad < end_rad:
                                in_cage = start_rad <= angle <= end_rad
                            else:
                                in_cage = angle >= start_rad or angle <= end_rad

                            if in_cage and ball.cage == 0:
                                teamScored = index
                                return True, teamScored
                        else:
                            return False, None

        return False, None



    def start_death(self):
        self.active = False
        self.dying = True
        self.death_timer = 0
        self.shards = []
        for _ in range(10):
            angle = math.radians(random.uniform(0, 360))
            speed = random.uniform(3, 6)
            self.shards.append({
                "angle": angle,
                "speed": speed,
                "length": random.randint(20, 40),
                "alpha": 255
            })

    def update_mort(self):
        if self.dying:
            self.death_timer += 1
            if self.death_timer > 30:
                return False  # prêt à être supprimé
        return True


    

            

    def draw(self, screen):
        if self.dying:
            center = (540, 960)
            for shard in self.shards:
                angle = shard["angle"]
                dist = self.death_timer * shard["speed"]
                length = shard["length"]
                alpha = max(0, 255 - self.death_timer * 10)

                x1 = center[0] + math.cos(angle) * dist
                y1 = center[1] + math.sin(angle) * dist
                x2 = center[0] + math.cos(angle) * (dist + length)
                y2 = center[1] + math.sin(angle) * (dist + length)

                color = (*self.color[:3], alpha)
                pygame.draw.line(screen, color, (x1, y1), (x2, y2), 5)

        else:
            if self.close:
                pygame.draw.circle(screen, self.color, (540, 960), self.rayon, 6)

            center = (self.x, self.y)
            rect = pygame.Rect(self.x - self.rayon, self.y - self.rayon, 2 * self.rayon, 2 * self.rayon)

            if len(self.cages.items())<=4:
                for index, (start_deg, end_deg) in self.cages.items():
                    if index in [1]:  # cages rouges
                        color = (205, 1, 23)
                        start = math.radians(start_deg + 5)
                        end = math.radians(end_deg - 5)
                    
                    elif index in [2]:  # cages vertes
                        color = ( 89, 24, 52)
                        start = math.radians(start_deg + 5)
                        end = math.radians(end_deg - 5)
                    else:  # arcs blancs
                        color =  (23, 211, 0) 
                        start = math.radians(start_deg )
                        end = math.radians(end_deg )

                    pygame.draw.arc(screen, color, rect, start, end, 8)

            if len (self.cages.items())>4:
                for index, (start_deg, end_deg) in self.cages.items():
                    if index in [1]:  # cages rouges
                        color = (0, 0, 255)
                        start = math.radians(start_deg + 3)
                        end = math.radians(end_deg - 3)
                    
                    elif index in [2]:  # cages vertes
                        color = (255, 0, 0)
                        start = math.radians(start_deg + 3)
                        end = math.radians(end_deg - 3)
                    
                    elif index in [3]:
                        color = ( 174, 174, 174)
                        start = math.radians(start_deg + 3)
                        end = math.radians(end_deg - 3)
                    
                    elif index in [4]:
                        color = (  255, 154, 0 )
                        start = math.radians(start_deg + 3)
                        end = math.radians(end_deg - 3)

                    else:  # arcs blancs
                        color =  ( 63, 63, 63 ) 
                        start = math.radians(start_deg )
                        end = math.radians(end_deg )

                    pygame.draw.arc(screen, color, rect, start, end, 5)


            elif self.active and not self.close:
                pygame.draw.arc(screen, self.color, rect, self.end_angle, self.start_angle, 9)


