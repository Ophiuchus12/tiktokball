import pygame
import numpy as np
import random
import os
import colorsys
from concurrent.futures import ThreadPoolExecutor
import math
import json

from note_sounds import load_note_sounds

with open ("config.json", "r") as f:
    config = json.load(f)

configAvanced = config.get("balleOptionsAvanced", {})
mode = configAvanced.get("mode", "none")
onBounce = configAvanced.get("onBounce", "none")

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(32)

note_sounds = load_note_sounds()

def rotate_point_around_center(point, center, angle_rad):
    translated = point - center
    cos_a, sin_a = np.cos(angle_rad), np.sin(angle_rad)
    rotated = np.array([
        translated[0] * cos_a - translated[1] * sin_a,
        translated[0] * sin_a + translated[1] * cos_a
    ])
    return rotated + center


mode = mode  # Modes possibles : "invisible", "trainee", "trace"
onBounce = onBounce #linked , #none
look = "none"

class Balle:

    
    def __init__(self, radius, color, colorIn, note_sounds=note_sounds, image_path=None, hidden_image=None, image_rect=None, position=None, velocity=None, cage=None, rond= None):

        self.position = np.array(position if position is not None else [540.0, 600.0], dtype=float)
        self.velocity = np.array(velocity if velocity is not None else [random.uniform(-5, 5), 0.0], dtype=float)
        self.radius = radius
        self.score = 0
        self.color = color
        self.colorIn = colorIn
        self.note_sounds = note_sounds  # Dictionnaire {midi_note: sound}
        self.trail = []
        self.max_trail_length = 15
        self.path = []
        self.hidden_image = hidden_image
        self.image_rect = image_rect
        self.active = True
        self.gravity_enabled = True
        self.rebonds_segments= []
        self.rotate_angle = 0.005 
        self.cage = cage
        self.rond = rond
        self.last_cage_change_frame = 0
        self.last_collision_frame = 0  
        self.transition_cooldown = 0


        # Chargement de l'image si fournie
        if image_path and os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
            diameter = self.radius * 1.8
            self.image = pygame.transform.smoothscale(self.image, (diameter, diameter))

        else:
            self.image = None

    def update(self):
        if self.gravity_enabled:
            self.velocity[1] += 0.2  # Gravité
        self.position += self.velocity

        if self.transition_cooldown > 0:
            self.transition_cooldown -= 1

        if mode == "trainee":
            self.trail.append(self.position.copy())
            if len(self.trail) > self.max_trail_length:
                self.trail.pop(0)
        if mode == "trace":        
            self.path.append((self.position.copy(), self.radius))


    


    def on_bounce(self):

        # Évite les rebonds trop fréquents
        current_frame = pygame.time.get_ticks() // (1000 // 60)  # Frame approximative
        if current_frame - self.last_collision_frame < 3:  # Minimum 3 frames entre rebonds
            return
            
        self.last_collision_frame = current_frame

        note = random.choice(list(self.note_sounds.values()))
        channel = note.play()
        if channel:
            channel.stop()
            note.play()

        if onBounce == "linked":
            center = np.array([540.0, 960.0])
            direction = self.position - center
            distance = np.linalg.norm(direction)

            if distance != 0:
                direction /= distance
                point_on_surface = self.position + direction * self.radius
                self.rebonds_segments.append([point_on_surface.copy(), self.position.copy()])
            else:
                self.rebonds_segments.append([self.position.copy(), self.position.copy()])





    def draw(self, screen):
        int_pos = self.position.astype(int)

        if mode == "invisible" and self.hidden_image and self.image_rect:
            # Taille de la zone à révéler (double du rayon)
            reveal_size = self.radius * 2

            # Position relative dans l'image cachée
            rel_x = int(self.position[0] - self.radius - self.image_rect.left)
            rel_y = int(self.position[1] - self.radius - self.image_rect.top)

            # Sécurité : ne pas dépasser les bords
            rel_x = max(0, min(rel_x, self.hidden_image.get_width() - reveal_size))
            rel_y = max(0, min(rel_y, self.hidden_image.get_height() - reveal_size))

            # Découpe et masque circulaire
            reveal_part = pygame.Surface((reveal_size, reveal_size), pygame.SRCALPHA)
            reveal_part.blit(self.hidden_image, (0, 0), (rel_x, rel_y, reveal_size, reveal_size))

            mask = pygame.Surface((reveal_size, reveal_size), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255, 255, 255, 255), (self.radius, self.radius), self.radius)
            reveal_part.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            # Dessine la partie révélée
            screen.blit(reveal_part, (self.position[0] - self.radius, self.position[1] - self.radius))

            # Dessine juste le contour, pas le centre
            pygame.draw.circle(screen, self.color, int_pos, self.radius + 2, width=1)  # épaisseur 3
        else:
            # Modes normaux : trail ou trace
            if mode == "trainee":
                for i, pos in enumerate(self.trail):
                    alpha = int(255 * (i + 1) / len(self.trail))
                    trail_color = (*self.color, alpha)
                    s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(s, trail_color, (self.radius, self.radius), self.radius)
                    screen.blit(s, (pos[0] - self.radius, pos[1] - self.radius))

            if mode == "trace":
                for i in range(0, len(self.path), 2):
                    pos, radius = self.path[i]
                    t = i / len(self.path)
                    r, g, b = colorsys.hsv_to_rgb(t, 1, 1)
                    alpha = int(100 * (i + 1) / len(self.path))
                    trail_color = (int(r * 255), int(g * 255), int(b * 255), alpha)

                    s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(s, trail_color, (radius, radius), radius)
                    screen.blit(s, (int(pos[0]) - radius, int(pos[1]) - radius))


            # Dessin complet de la balle normale
            pygame.draw.circle(screen, self.color, int_pos, self.radius + 5)
            if self.image:
                rect = self.image.get_rect(center=int_pos)
                screen.blit(self.image, rect)
            else:
                pygame.draw.circle(screen, self.colorIn, int_pos, self.radius)

        if onBounce == "linked":
            center = np.array([540.0, 960.0])
            for segment in self.rebonds_segments:
                start = segment[0]
                end = self.position  # toujours actuel
                pygame.draw.line(screen, self.colorIn, start, end, 2)
                start = segment[0]
                rotated_start = rotate_point_around_center(start, center, self.rotate_angle)
                segment[0] = rotated_start


    def clone(self, position=None):
        new_balle = Balle(
            radius=self.radius,
            color=self.color,
            colorIn=self.colorIn,
            note_sounds=self.note_sounds,
            image_path=None,
            hidden_image=self.hidden_image,
            image_rect=self.image_rect
        )
        new_balle.position = position if position is not None else self.position.copy()
        new_balle.velocity = np.array([random.uniform(-5, 5), 0.0])
        new_balle.score = self.score
        new_balle.image = self.image
        return new_balle



    