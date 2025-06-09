import pygame
import math
import numpy as np
import random

rotate = "free"
onBounce = "none"  # "linked" ou "none"
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
    def __init__(self, rayon, start_deg, end_deg, color=(255, 255, 255), index=0):
        self.rayon = rayon
        self.start_angle = math.radians(start_deg)
        self.end_angle = math.radians(end_deg)
        self.active = True
        self.color = color
        self.dying = False
        self.death_timer = 0
        self.shards = []


        if rotate == "free":
            self.rotation_speed = random.uniform(0.005, 0.01)
            self.rotation_direction = random.choice([-1, 1])  # -1 : anti-horaire, 1 : horaire
        
        elif rotate == "stuck":
            self.rotation_speed = 0.01
            self.rotation_direction = 1

        self.index = index  # <- nouvel attribut
        self.close = False  # Indique si le cercle est fermé

    def update_angles(self):
        delta = self.rotation_speed * self.rotation_direction
        self.start_angle += delta
        self.end_angle += delta

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
                    self.start_death()  # <- ici
                    return True

                else:
                    normal = direction / distance
                    ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal
                    overlap = (distance + ball.radius) - self.rayon
                    ball.position -= normal * overlap
                    ball.on_bounce()
        return False  

    def check_collision_simple(self, ball):
        if not self.active:
            return False

        center = np.array([540.0, 960.0])
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        # Collision dès que le bord extérieur touche le cercle
        if distance >= self.rayon - ball.radius:
            if distance != 0:
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
                    # Rebond réaliste en fonction du bord
                    normal = direction / distance
                    ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal

                    # Corriger le chevauchement pour éviter la pénétration visuelle
                    overlap = self.rayon - (distance + ball.radius)
                    if overlap < 0:
                        ball.position += normal * overlap

                    ball.on_bounce()
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

                ball.radius += 4



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

        elif self.close:
            if look == "sabre":
                bright_color = tuple(min(255, int(c * 1.5)) for c in self.color[:3])
                pygame.draw.circle(screen, bright_color, (540, 960), self.rayon, 10)
            else:
                pygame.draw.circle(screen, self.color, (540, 960), self.rayon, 10)

        elif self.active:
            rect = pygame.Rect(550 - self.rayon, 960 - self.rayon, 2 * self.rayon, 2 * self.rayon)

            if look == "sabre":
                bright_color = tuple(min(255, int(c * 1.5)) for c in self.color[:3])
                pygame.draw.arc(screen, bright_color, rect, self.end_angle, self.start_angle, 6)

            else:
                pygame.draw.arc(screen, self.color, rect, self.end_angle, self.start_angle, 6)
