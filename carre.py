import pygame
import math
import numpy as np
import random

class Carre :
    def __init__(self, size, color=(255, 255, 255), index=0):
        self.size = size
        self.position = np.array([540.0, 960.0], dtype=float)
        self.color = color
        self.active = True
        self.dying = False
        self.death_timer = 0
        self.shards = []
        self.index = index  # Nouvel attribut pour l'index du carré
        self.base_angle = math.radians(270)  # Angle moyen (en bas)
        self.amplitude = math.radians(20)    # +/-10° de part et d’autre
        self.oscillation_speed = 0.05        # Vitesse d’oscillation
        self.oscillation_phase = 0           # Phase de l’oscillation
        self.hole_width = math.radians(20)   # Taille de l’ouverture
 

    def check_collision(self, ball):
        if not self.active:
            return

        center = np.array([540.0, 960.0])
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        if distance + ball.radius >= self.size / 2:
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
                    return True

                else:
                    normal = direction / distance
                    ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal
                    overlap = (distance + ball.radius) - self.rayon
                    ball.position -= normal * overlap
                    ball.on_bounce()
        return False  
    

    def update_angles(self):
        self.oscillation_phase += self.oscillation_speed
        angle_center = self.base_angle + math.sin(self.oscillation_phase) * self.amplitude
        self.start_angle = angle_center - self.hole_width / 2
        self.end_angle = angle_center + self.hole_width / 2


    def draw(self, screen): 
        

        int_pos = self.position.astype(int)
        
        pygame.draw.rect(screen, (0, 0, 0), (int_pos[0] - self.size // 2, int_pos[1] - self.size // 2, self.size, self.size), 1)