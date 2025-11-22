"""
Ball class for the game.
Handles ball physics, rendering, and visual effects.
"""
import pygame
import numpy as np
import random
import os
import colorsys
import math

from config.config_manager import get_config
from config.constants import (
    SCREEN_CENTER, GRAVITY, IMAGE_SCALE_FACTOR, 
    MAX_TRAIL_LENGTH, MIN_COLLISION_FRAMES, FPS
)

# Initialize pygame mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(32)




def rotate_point_around_center(point, center, angle_rad):
    """Rotate a point around a center by a given angle in radians."""
    translated = point - center
    cos_a, sin_a = np.cos(angle_rad), np.sin(angle_rad)
    rotated = np.array([
        translated[0] * cos_a - translated[1] * sin_a,
        translated[0] * sin_a + translated[1] * cos_a
    ])
    return rotated + center


class Balle:
    """Represents a ball in the game with physics and rendering."""
    
    def __init__(self, radius, color, colorIn, image_path=None, 
             hidden_image=None, image_rect=None, position=None, velocity=None, 
             cage=None, rond=None):
            self.position = np.array(
                position if position is not None else [SCREEN_CENTER[0], 600.0], 
                dtype=float
            )
            self.velocity = np.array(
                velocity if velocity is not None else [random.uniform(-5, 5), 0.0], 
                dtype=float
            )
            self.radius = radius
            self.score = 0
            self.color = color
            self.colorIn = colorIn
            self.trail = []
            self.max_trail_length = MAX_TRAIL_LENGTH
            self.path = []
            self.hidden_image = hidden_image
            self.image_rect = image_rect
            self.active = True
            self.gravity_enabled = True
            self.rebonds_segments = []
            self.rotate_angle = 0.005 
            self.cage = cage
            self.rond = rond
            self.last_cage_change_frame = 0
            self.last_collision_frame = 0  
            self.transition_cooldown = 0

            # Load image if provided
            if image_path and os.path.exists(image_path):
                self.image = pygame.image.load(image_path).convert_alpha()
                diameter = self.radius * IMAGE_SCALE_FACTOR
                self.image = pygame.transform.smoothscale(self.image, (diameter, diameter))
            else:
                self.image = None

    def update(self):
        """Update ball position and state."""
        if self.gravity_enabled:
            self.velocity[1] += GRAVITY
        self.position += self.velocity

        if self.transition_cooldown > 0:
            self.transition_cooldown -= 1

        # Get current mode from config
        config = get_config()
        mode = config.get_ball_mode()

        if mode == "trainee":
            self.trail.append(self.position.copy())
            if len(self.trail) > self.max_trail_length:
                self.trail.pop(0)
        elif mode == "trace":        
            self.path.append((self.position.copy(), self.radius))

    def on_bounce(self):
        """Handle bounce event with sound and visual effects."""
        # Prevent too frequent bounces
        current_frame = pygame.time.get_ticks() // (1000 // FPS)
        if current_frame - self.last_collision_frame < MIN_COLLISION_FRAMES:
            return
            
        self.last_collision_frame = current_frame

        # # Play sound
        # note = random.choice(list(self.note_sounds.values()))
        # channel = note.play()
        # if channel:
        #     channel.stop()
        #     note.play()

        # Visual effect for linked mode
        config = get_config()
        onBounce = config.get_bounce_mode()
        
        if onBounce == "linked":
            direction = self.position - SCREEN_CENTER
            distance = np.linalg.norm(direction)

            if distance != 0:
                direction /= distance
                point_on_surface = self.position + direction * self.radius
                self.rebonds_segments.append([point_on_surface.copy(), self.position.copy()])
            else:
                self.rebonds_segments.append([self.position.copy(), self.position.copy()])

    def draw(self, screen):
        """Draw the ball and its effects."""
        int_pos = self.position.astype(int)
        config = get_config()
        mode = config.get_ball_mode()
        onBounce = config.get_bounce_mode()

        if mode == "invisible" and self.hidden_image and self.image_rect:
            self._draw_invisible_mode(screen, int_pos)
        else:
            self._draw_normal_mode(screen, int_pos, mode, onBounce)

    def _draw_invisible_mode(self, screen, int_pos):
        """Draw ball in invisible mode (reveals hidden image)."""
        reveal_size = self.radius * 2

        # Relative position in hidden image
        rel_x = int(self.position[0] - self.radius - self.image_rect.left)
        rel_y = int(self.position[1] - self.radius - self.image_rect.top)

        # Safety: don't exceed borders
        rel_x = max(0, min(rel_x, self.hidden_image.get_width() - reveal_size))
        rel_y = max(0, min(rel_y, self.hidden_image.get_height() - reveal_size))

        # Cut and circular mask
        reveal_part = pygame.Surface((reveal_size, reveal_size), pygame.SRCALPHA)
        reveal_part.blit(self.hidden_image, (0, 0), (rel_x, rel_y, reveal_size, reveal_size))

        mask = pygame.Surface((reveal_size, reveal_size), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (self.radius, self.radius), self.radius)
        reveal_part.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Draw revealed part
        screen.blit(reveal_part, (self.position[0] - self.radius, self.position[1] - self.radius))

        # Draw outline only
        int_pos = self.position.astype(int)
        pygame.draw.circle(screen, self.color, int_pos, self.radius + 2, width=1)

    def _draw_normal_mode(self, screen, int_pos, mode, onBounce):
        """Draw ball in normal modes with trails."""
        # Draw trail effects
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

        # Draw main ball
        pygame.draw.circle(screen, self.color, int_pos, self.radius + 5)
        if self.image:
            rect = self.image.get_rect(center=int_pos)
            screen.blit(self.image, rect)
        else:
            pygame.draw.circle(screen, self.colorIn, int_pos, self.radius)

        # Draw linked bounce segments
        if onBounce == "linked":
            for segment in self.rebonds_segments:
                start = segment[0]
                end = self.position
                pygame.draw.line(screen, self.colorIn, start, end, 2)
                rotated_start = rotate_point_around_center(start, SCREEN_CENTER, self.rotate_angle)
                segment[0] = rotated_start

    def clone(self, position=None):
        """Create a clone of this ball."""
        new_balle = Balle(
            radius=self.radius,
            color=self.color,
            colorIn=self.colorIn,
            image_path=None,
            hidden_image=self.hidden_image,
            image_rect=self.image_rect
        )

        new_balle.position = position if position is not None else self.position.copy()
        new_balle.velocity = np.array([random.uniform(-5, 5), 0.0])
        new_balle.score = self.score
        new_balle.image = self.image
        return new_balle