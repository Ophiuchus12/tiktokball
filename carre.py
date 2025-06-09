import pygame
import numpy as np
import math
import random

class Carre:
    def __init__(self, size, color=(255, 255, 255), index=0):
        self.size = size
        self.position = np.array([540.0, 960.0], dtype=float)
        self.color = color
        self.active = True
        self.index = index
        self.rotation_speed = random.uniform(0.01, 0.03)
        self.rotation_direction = random.choice([-1, 1])

        # Segment bas seulement
        self.opening_center = 0.0  # De -1 à 1 (pourcentage d'oscillation)
        self.opening_width = 0.4   # Pourcentage de largeur (ex: 40%)

    def update_angles(self):
        self.opening_center += self.rotation_speed * self.rotation_direction
        if abs(self.opening_center) > 0.6:
            self.rotation_direction *= -1

    def check_collision(self, ball):
        if not self.active:
            return False

        x, y = ball.position
        cx, cy = self.position
        half = self.size / 2
        r = ball.radius

        # Détection si balle touche le bord bas
        if (cy + half - r <= y <= cy + half + r) and (cx - half <= x <= cx + half):
            # Coordonnée X relative (0 à 1)
            relative_x = (x - (cx - half)) / self.size

            # Définir ouverture dynamique
            open_start = 0.5 + self.opening_center - self.opening_width / 2
            open_end = 0.5 + self.opening_center + self.opening_width / 2

            if open_start <= relative_x <= open_end:
                ball.score += 1
                return True
            else:
                # Rebonds sur bas
                ball.velocity[1] *= -1
                ball.on_bounce()
                return False

        # Rebonds sur les autres côtés
        if (cx - half - r <= x <= cx + half + r) and (cy - half <= y <= cy + half):
            if x <= cx - half or x >= cx + half:
                ball.velocity[0] *= -1
                ball.on_bounce()
        if (cy - half - r <= y <= cy + half + r) and (cx - half <= x <= cx + half):
            if y <= cy - half:
                ball.velocity[1] *= -1
                ball.on_bounce()
        return False

    def draw(self, screen):
        pos = self.position.astype(int)
        rect = pygame.Rect(pos[0] - self.size // 2, pos[1] - self.size // 2, self.size, self.size)

        pygame.draw.rect(screen, self.color, rect, 4)

        # Dessine l’ouverture en bas
        start_x = pos[0] - self.size // 2 + int((0.5 + self.opening_center - self.opening_width / 2) * self.size)
        end_x = pos[0] - self.size // 2 + int((0.5 + self.opening_center + self.opening_width / 2) * self.size)
        y = pos[1] + self.size // 2

        pygame.draw.line(screen, (0, 255, 0), (start_x, y), (end_x, y), 6)
