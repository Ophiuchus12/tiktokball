"""
Square obstacle class for the game.
"""
import pygame
import numpy as np
import math
import random


class Carre:
    """Represents a square obstacle with dynamic opening."""
    
    def __init__(self, size, color=(255, 255, 255), index=0):
        """Initialize a square obstacle."""
        self.size = size
        self.position = np.array([540.0, 960.0], dtype=float)
        self.color = color
        self.active = True
        self.index = index
        self.rotation_speed = random.uniform(0.01, 0.03)
        self.rotation_direction = random.choice([-1, 1])

        # Bottom segment only
        self.opening_center = 0.0  # From -1 to 1 (oscillation percentage)
        self.opening_width = 0.4   # Width percentage (e.g., 40%)

    def update_angles(self):
        """Update opening position."""
        self.opening_center += self.rotation_speed * self.rotation_direction
        if abs(self.opening_center) > 0.6:
            self.rotation_direction *= -1

    def check_collision(self, ball):
        """Check collision with ball."""
        if not self.active:
            return False

        x, y = ball.position
        cx, cy = self.position
        half = self.size / 2
        r = ball.radius

        # Check if ball touches bottom edge
        if (cy + half - r <= y <= cy + half + r) and (cx - half <= x <= cx + half):
            # Relative X coordinate (0 to 1)
            relative_x = (x - (cx - half)) / self.size

            # Define dynamic opening
            open_start = 0.5 + self.opening_center - self.opening_width / 2
            open_end = 0.5 + self.opening_center + self.opening_width / 2

            if open_start <= relative_x <= open_end:
                ball.score += 1
                return True
            else:
                # Bounce on bottom
                ball.velocity[1] *= -1
                ball.on_bounce()
                return False

        # Bounce on other sides
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
        """Draw the square."""
        pos = self.position.astype(int)
        rect = pygame.Rect(
            pos[0] - self.size // 2,
            pos[1] - self.size // 2,
            self.size,
            self.size
        )

        pygame.draw.rect(screen, self.color, rect, 4)

        # Draw opening at bottom
        start_x = pos[0] - self.size // 2 + int(
            (0.5 + self.opening_center - self.opening_width / 2) * self.size
        )
        end_x = pos[0] - self.size // 2 + int(
            (0.5 + self.opening_center + self.opening_width / 2) * self.size
        )
        y = pos[1] + self.size // 2

        pygame.draw.line(screen, (0, 255, 0), (start_x, y), (end_x, y), 6)