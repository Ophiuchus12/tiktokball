"""
Circle class for the game.
Handles circle collision detection, rendering, and animations.
"""
import pygame
import math
import numpy as np
import random

from config.config_manager import get_config
from config.constants import (
    SCREEN_CENTER, DEFAULT_ROTATION_SPEED_MIN, DEFAULT_ROTATION_SPEED_MAX,
    DEATH_ANIMATION_DURATION, SHARD_COUNT, SHARD_SPEED_MIN, SHARD_SPEED_MAX,
    SHARD_LENGTH_MIN, SHARD_LENGTH_MAX
)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(32)



def reflect(velocity, normal):
    """Reflect velocity vector across a normal vector."""
    dot = velocity[0] * normal[0] + velocity[1] * normal[1]
    reflected = (
        velocity[0] - 2 * dot * normal[0],
        velocity[1] - 2 * dot * normal[1]
    )
    return reflected


class Cercle:
    """Represents a circle obstacle in the game."""
    
    def __init__(self, rayon, start_deg, end_deg, color=(255, 255, 255), index=0, 
                 cages=None, x=540.0, y=960.0, rotation_mode="stuck"):
        """Initialize a circle with given parameters."""
        self.rayon = rayon
        self.start_angle = math.radians(start_deg)
        self.end_angle = math.radians(end_deg)
        self.active = True
        self.color = color
        self.dying = False
        self.death_timer = 0
        self.shards = []
        self.cages = cages if cages else {}
        self.x = x
        self.y = y
        self.index = index
        self.close = False

        # Set rotation based on mode
        if rotation_mode == "free":
            self.rotation_speed = random.uniform(
                DEFAULT_ROTATION_SPEED_MIN, 
                DEFAULT_ROTATION_SPEED_MAX
            )
            self.rotation_direction = random.choice([-1, 1])
        elif rotation_mode == "stuck":
            self.rotation_speed = 0.01
            self.rotation_direction = -1
        else:
            self.rotation_speed = 0
            self.rotation_direction = 0

    def update_angles(self):
        """Update circle rotation angles."""
        delta = self.rotation_speed * self.rotation_direction

        # Rotate angles in radians
        self.start_angle += delta
        self.end_angle += delta

        # Also rotate cages
        if self.cages:
            new_cages = {}
            for index, (start_deg, end_deg) in self.cages.items():
                start_deg = (start_deg + math.degrees(delta)) % 360
                end_deg = (end_deg + math.degrees(delta)) % 360
                new_cages[index] = (start_deg, end_deg)
            self.cages = new_cages

    def rotate_around_center(self, center_x, center_y):
        """Rotate circle position around a center point."""
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
        """Update circle radius."""
        self.rayon = new_radius

    def check_collision(self, ball):
        """Check collision with ball (classic mode with hole)."""
        if not self.active:
            return False

        center = SCREEN_CENTER
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
                    config = get_config()
                    if config.get_bounce_mode() == "linked":
                        ball.rebonds_segments.clear() 
                        ball.velocity = np.array([
                            random.randint(8, 15) * 2, 
                            random.randint(8, 15) * 2
                        ])

                    self.start_death()
                    return True
                else:
                    normal = direction / distance
                    ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal
                    overlap = (distance + ball.radius) - self.rayon
                    ball.position -= normal * overlap
                    ball.on_bounce()
        return False

    def check_collision_simple(self, ball, center=None):
        """Check collision with ball (simple mode, no death animation)."""
        if not self.active:
            return False

        if center is None:
            center = np.array([self.x, self.y], dtype=float)
        
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        if distance == 0:
            return False

        # If ball touches or exceeds the edge
        if distance + ball.radius >= self.rayon:
            angle = math.degrees(math.atan2(-direction[1], direction[0])) % 360
            start_deg = math.degrees(self.start_angle) % 360
            end_deg = math.degrees(self.end_angle) % 360

            # Check if ball passes through opening
            if start_deg < end_deg:
                in_hole = start_deg <= angle <= end_deg
            else:
                in_hole = angle >= start_deg or angle <= end_deg

            if in_hole:
                ball.score += 1
                return True
            else:
                # Calculate bounce
                normal = direction / distance
                ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal
                ball.position = center + normal * (self.rayon - ball.radius)
                ball.on_bounce()

                # Adjust last segment position for linked mode
                config = get_config()
                if config.get_bounce_mode() == "linked" and len(ball.rebonds_segments) > 1:
                    last_segment = ball.rebonds_segments[-1]
                    seg_dir = last_segment[0] - center
                    seg_dist = np.linalg.norm(seg_dir)
                    if seg_dist != 0:
                        seg_dir /= seg_dist
                        dist_center_to_ball = np.linalg.norm(ball.position - center)
                        last_segment[0] = center + seg_dir * (dist_center_to_ball + ball.radius)

        return False
    
    def check_collision_triple(self, ball):
        """Improved collision detection to avoid multiple bounces."""
        if not self.active:
            return False, None

        center = np.array([self.x, self.y], dtype=float)
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        if distance == 0:
            return False, None

        # Collision with circle edge
        if distance + ball.radius >= self.rayon:
            angle = math.degrees(math.atan2(-direction[1], direction[0])) % 360
            start_deg = math.degrees(self.start_angle) % 360
            end_deg = math.degrees(self.end_angle) % 360

            # Check if in opening (free passage)
            if start_deg < end_deg:
                in_hole = start_deg <= angle <= end_deg
            else:
                in_hole = angle >= start_deg or angle <= end_deg

            if in_hole:
                # Free passage
                ball.score += 1
                return True, ball
            else:
                # Bounce on solid wall
                normal = direction / distance
                
                # Check to avoid multiple bounces
                velocity_towards_surface = np.dot(ball.velocity, normal)
                if velocity_towards_surface <= 0:
                    return False, None  # Ball already moving away
                
                # Perform bounce
                ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal
                ball.position = center + normal * (self.rayon - ball.radius)
                ball.on_bounce()

                # Handle bounce segments if enabled
                config = get_config()
                if config.get_bounce_mode() == "linked" and len(ball.rebonds_segments) > 1:
                    last_segment = ball.rebonds_segments[-1]
                    seg_dir = last_segment[0] - center
                    seg_dist = np.linalg.norm(seg_dir)
                    if seg_dist != 0:
                        seg_dir /= seg_dist
                        dist_center_to_ball = np.linalg.norm(ball.position - center)
                        last_segment[0] = center + seg_dir * (dist_center_to_ball + ball.radius)

        return False, None
    
    def check_passage_only(self, ball):
        """Improved passage detection."""
        if not self.active:
            return False

        center = np.array([self.x, self.y], dtype=float)
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        # Check if ball is in circle's influence zone
        if self.rayon - ball.radius * 2 < distance < self.rayon + ball.radius * 2:
            angle = math.degrees(math.atan2(-direction[1], direction[0])) % 360
            start_deg = math.degrees(self.start_angle) % 360
            end_deg = math.degrees(self.end_angle) % 360

            # Check if ball is in opening
            if start_deg < end_deg:
                in_hole = start_deg <= angle <= end_deg
            else:
                in_hole = angle >= start_deg or angle <= end_deg

            # Additional check: is ball heading inward?
            velocity_towards_center = np.dot(ball.velocity, -direction / distance) if distance > 0 else 0
            
            return in_hole and velocity_towards_center > 0

        return False

    def close_cercle_collision(self, ball):
        """Collision for closed circle mode."""
        if not self.active:
            return False

        center = SCREEN_CENTER
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        # Collision with inner edge of circle
        if distance + ball.radius >= self.rayon:
            if distance != 0 and ball.radius < self.rayon:
                normal = direction / distance
                ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal

                # Correct overlap
                overlap = (distance + ball.radius) - self.rayon
                ball.position -= normal * overlap

                ball.on_bounce()

                # Adjust last segment position for linked mode
                config = get_config()
                if config.get_bounce_mode() == "linked" and len(ball.rebonds_segments) > 1:
                    last_segment = ball.rebonds_segments[-1]
                    seg_dir = last_segment[0] - center
                    seg_dist = np.linalg.norm(seg_dir)
                    if seg_dist != 0:
                        seg_dir /= seg_dist
                        dist_center_to_ball = np.linalg.norm(ball.position - center)
                        last_segment[0] = center + seg_dir * (dist_center_to_ball + ball.radius)

        return False
    
    def close_cercle_nogravity(self, ball):
        """Closed circle collision without gravity."""
        if not self.active:
            return False

        center = SCREEN_CENTER
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        if distance + ball.radius >= self.rayon:
            if distance != 0 and ball.radius < self.rayon:
                normal = direction / distance
                ball.velocity = reflect(ball.velocity, normal)
                ball.on_bounce()

        return False
    
    def check_collision_cage(self, ball):
        """Check collision for cage mode (team scoring)."""
        if not self.active:
            return False, None

        center = SCREEN_CENTER
        direction = ball.position - center
        distance = np.linalg.norm(direction)

        if distance + ball.radius >= self.rayon:
            if distance != 0 and ball.radius < self.rayon:
                normal = direction / distance
                ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal
                overlap = (distance + ball.radius) - self.rayon
                ball.position -= normal * overlap
                ball.on_bounce()

                config = get_config()
                if config.get_bounce_mode() == "cage":
                    # Convert ball position to angle (in radians)
                    angle = math.atan2(-direction[1], direction[0]) % (2 * math.pi)

                    for index, (start_deg, end_deg) in self.cages.items():
                        if index in [1, 2]:  # Red and green cages
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
        """Start death animation."""
        self.active = False
        self.dying = True
        self.death_timer = 0
        self.shards = []
        for _ in range(SHARD_COUNT):
            angle = math.radians(random.uniform(0, 360))
            speed = random.uniform(SHARD_SPEED_MIN, SHARD_SPEED_MAX)
            self.shards.append({
                "angle": angle,
                "speed": speed,
                "length": random.randint(SHARD_LENGTH_MIN, SHARD_LENGTH_MAX),
                "alpha": 255
            })

    def update_mort(self):
        """Update death animation."""
        if self.dying:
            self.death_timer += 1
            if self.death_timer > DEATH_ANIMATION_DURATION:
                return False  # Ready to be removed
        return True

    def draw(self, screen):
        """Draw the circle."""
        if self.dying:
            self._draw_death_animation(screen)
        else:
            self._draw_normal(screen)

    def _draw_death_animation(self, screen):
        """Draw death animation with shards."""
        center = (int(self.x), int(self.y))
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

    def _draw_normal(self, screen):
        """Draw normal circle (non-dying)."""
        center = (int(self.x), int(self.y))
        rect = pygame.Rect(
            self.x - self.rayon, 
            self.y - self.rayon, 
            2 * self.rayon, 
            2 * self.rayon
        )

        # Si cercle fermé (plein)
        if self.close:
            pygame.draw.circle(screen, self.color, center, self.rayon, 6)
            return

        # Si le cercle a des cages, les dessiner
        if self.cages and len(self.cages) > 0:
            if len(self.cages) <= 4:
                for index, (start_deg, end_deg) in self.cages.items():
                    if index == 1:  # Red cages
                        color = (205, 1, 23)
                        start = math.radians(start_deg + 5)
                        end = math.radians(end_deg - 5)
                    elif index == 2:  # Green cages
                        color = (89, 24, 52)
                        start = math.radians(start_deg + 5)
                        end = math.radians(end_deg - 5)
                    else:  # White arcs
                        color = (23, 211, 0)
                        start = math.radians(start_deg)
                        end = math.radians(end_deg)

                    pygame.draw.arc(screen, color, rect, start, end, 8)
            else:
                for index, (start_deg, end_deg) in self.cages.items():
                    if index == 1:
                        color = (0, 0, 255)
                        start = math.radians(start_deg + 3)
                        end = math.radians(end_deg - 3)
                    elif index == 2:
                        color = (255, 0, 0)
                        start = math.radians(start_deg + 3)
                        end = math.radians(end_deg - 3)
                    elif index == 3:
                        color = (174, 174, 174)
                        start = math.radians(start_deg + 3)
                        end = math.radians(end_deg - 3)
                    elif index == 4:
                        color = (255, 154, 0)
                        start = math.radians(start_deg + 3)
                        end = math.radians(end_deg - 3)
                    else:  # Gray arcs
                        color = (63, 63, 63)
                        start = math.radians(start_deg)
                        end = math.radians(end_deg)

                    pygame.draw.arc(screen, color, rect, end, start, 5)
        

        else:
            if self.active:
                pygame.draw.arc(
                    screen, 
                    self.color, 
                    rect,
                    self.end_angle,    # ✅ END après 
                    self.start_angle,  # ✅ START avant

                    9
                )
                                              