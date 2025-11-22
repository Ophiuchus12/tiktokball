"""
Game mode interaction handlers.
Manages collision detection and game logic for different modes.
"""
import random
import math
import numpy as np
from config.constants import SCREEN_CENTER, MIN_CAGE_CHANGE_FRAMES


class GameModeHandler:
    """Base class for game mode handlers."""
    
    def __init__(self):
        self.frame_count = 0  # Fixed: frame_count as instance variable
    
    def update(self, screen, cercles, balles):
        """Update game logic. Override in subclasses."""
        self.frame_count += 1
        return [], []  # new_balles, balles_to_remove


def reset_all_balls(balls, vitesse=15, radius=100):
    """
    Reset positions and velocities of balls around screen center.
    
    Args:
        balls: List of balls
        vitesse: Initial velocity of each ball
        radius: Distance around center to avoid overlap
    """
    center = SCREEN_CENTER
    n = len(balls)

    for i, ball in enumerate(balls):
        # Distribute balls evenly in circle around center
        angle_pos = (2 * math.pi / n) * i
        pos_offset = np.array([math.cos(angle_pos), math.sin(angle_pos)]) * radius
        ball.position = center + pos_offset

        # Generate random direction for velocity
        angle_vel = random.uniform(0, 2 * math.pi)
        vx = math.cos(angle_vel) * vitesse
        vy = math.sin(angle_vel) * vitesse
        ball.velocity = np.array([vx, vy])

        ball.gravity_enabled = False


class ClassiqueMode(GameModeHandler):
    """Classic game mode handler."""
    
    def update(self, screen, cercles, balles, mode):
        """Update classic mode."""
        self.frame_count += 1
        new_balles = []
        
        for c in cercles:
            for b in balles:
                passed = c.check_collision(b)
                if passed:
                    for c in cercles:
                        c.rotation_direction *= -1 
                        c.rotation_speed = random.uniform(0.005, 0.01)
                if passed and mode == "multi":
                    clone = b.clone()
                    new_balles.append(clone)
        
        return new_balles, []


class SimpleCercleFermeMode(GameModeHandler):
    """Simple closed circle mode handler."""
    
    def update(self, screen, cercles, balles, mode):
        """Update closed circle mode."""
        self.frame_count += 1
        
        for c in cercles:
            for b in balles:
                c.close_cercle_collision(b)
        
        return [], []


class RebondInfiniMode(GameModeHandler):
    """Infinite bounce mode handler."""
    
    def update(self, screen, cercles, balles, mode):
        """Update infinite bounce mode."""
        self.frame_count += 1
        
        for c in cercles:
            for b in balles:
                b.gravity_enabled = False
                c.close_cercle_nogravity(b)
        
        return [], []


class SimpleCercleMode(GameModeHandler):
    """Simple circle mode with ball multiplication."""
    
    def update(self, screen, cercles, balles, mode):
        """Update simple circle mode."""
        self.frame_count += 1
        new_balles = []
        balles_to_remove = []
        
        for c in cercles:
            for b in balles:
                passed = c.check_collision_simple(b, center=np.array([c.x, c.y]))
                if passed and mode == "simple" and b.active:
                    clone1 = b.clone(position=np.array([c.x, c.y]))
                    clone2 = b.clone(position=np.array([c.x, c.y]))
                    
                    new_balles.append(clone1)
                    new_balles.append(clone2)
                    b.active = False

                # Remove balls outside screen
                if (b.position[0] < 0 or b.position[0] > screen.get_width() or
                    b.position[1] < 0 or b.position[1] > screen.get_height()):
                    balles_to_remove.append(b)
        
        return new_balles, balles_to_remove


class CageCercleMode(GameModeHandler):
    """Cage circle mode with team scoring."""
    
    def update(self, screen, cercles, balles, mode):
        """Update cage circle mode."""
        self.frame_count += 1
        any_goal = False

        for c in cercles:
            for b in balles:
                b.gravity_enabled = False
                goal, teamScored = c.check_collision_cage(b)
                if goal:
                    any_goal = True
                    for ball in balles:
                        if teamScored == ball.cage:
                            ball.score += 1

        if any_goal:
            reset_all_balls(balles)
        
        return [], []


class TripleCercleMode(GameModeHandler):
    """Triple circle mode with cage transitions."""
    
    def update(self, screen, cercles, balles, mode):
        """Update triple circle mode with fixed frame_count."""
        self.frame_count += 1  # Fixed: use instance variable
        new_balles = []
        balles_to_remove = []
        
        for b in balles:
            if not b.active:
                continue

            # Initial cage assignment if needed
            if b.cage is None:
                closest_circle = None
                min_distance = float('inf')
                for c_init in cercles:
                    distance = np.linalg.norm(b.position - np.array([c_init.x, c_init.y]))
                    if distance < min_distance:
                        min_distance = distance
                        closest_circle = c_init
                b.cage = closest_circle

            # Check passages to other circles
            passage_detected = False
            for c in cercles:
                if c != b.cage:
                    # Check if ball enters new circle
                    if c.check_passage_only(b):
                        # Minimum delay between cage changes to avoid oscillation
                        if self.frame_count - b.last_cage_change_frame > MIN_CAGE_CHANGE_FRAMES:
                            old_cage = b.cage
                            b.cage = c
                            b.last_cage_change_frame = self.frame_count
                            
                            # Smoother position adjustment
                            center_new = np.array([c.x, c.y])
                            
                            # Calculate entry direction into new circle
                            entry_vector = b.position - center_new
                            entry_distance = np.linalg.norm(entry_vector)
                            
                            if entry_distance > 0:
                                # Place ball slightly inside new circle
                                normalized_entry = entry_vector / entry_distance
                                safe_distance = c.rayon - b.radius * 1.5
                                b.position = center_new + normalized_entry * safe_distance
                            
                            passage_detected = True

                            # Create clones in old cage
                            clonedBalle = b.clone(position=np.array([old_cage.x, old_cage.y]))
                            clonedBalle.cage = old_cage
                            clonedBalle.last_cage_change_frame = self.frame_count
                            clonedBalle.color = (
                                random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255)
                            )

                            clonedBalle2 = b.clone(position=np.array([old_cage.x, old_cage.y]))
                            clonedBalle2.cage = old_cage
                            clonedBalle2.last_cage_change_frame = self.frame_count
                            clonedBalle2.color = (
                                random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255)
                            )
                            new_balles.append(clonedBalle)
                            new_balles.append(clonedBalle2)
                            
                            break

            # Collision with current cage
            if not passage_detected and b.cage is not None:
                passed, passedBall = b.cage.check_collision_triple(b)
                if passed and passedBall is not None:
                    if (passedBall.position[0] < 0 or 
                        passedBall.position[0] > screen.get_width() or
                        passedBall.position[1] < 0 or 
                        passedBall.position[1] > screen.get_height()):
                        balles_to_remove.append(passedBall)
        
        return new_balles, balles_to_remove


# Mode handler registry
MODE_HANDLERS = {
    "classique": ClassiqueMode(),
    "simpleCercleferme": SimpleCercleFermeMode(),
    "rebondInfini": RebondInfiniMode(),
    "simpleCercle": SimpleCercleMode(),
    "cageCercle": CageCercleMode(),
    "tripleCercle": TripleCercleMode()
}


def interaction(screen, theme, mode, cercles, balles):
    """
    Main interaction handler that delegates to appropriate mode handler.
    
    Args:
        screen: Pygame screen surface
        theme: Game theme/mode string
        mode: Sub-mode string (e.g., "multi", "simple")
        cercles: List of circle objects
        balles: List of ball objects
    
    Returns:
        Tuple of (new_balles, balles_to_remove) that will be processed by caller
    """
    handler = MODE_HANDLERS.get(theme)
    
    if handler:
        new_balles, balles_to_remove = handler.update(screen, cercles, balles, mode)
        
        # Clean up removed balls
        for b in balles_to_remove:
            if b in balles:
                balles.remove(b)
        
        # Add new balls
        balles.extend(new_balles)
    else:
        print(f"Warning: Unknown theme '{theme}'")