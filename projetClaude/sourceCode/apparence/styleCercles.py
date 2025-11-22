"""
Circle style generator for different game themes.
Creates circles with various configurations and visual styles.
"""
import colorsys
import math
import random
import numpy as np
import pygame

from entite.cercle import Cercle
from entite.balle import Balle
from config.constants import SCREEN_CENTER

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(32)



def generate_circle_colors(n):
    """
    Generate n colors evenly distributed across the HSV color spectrum.
    
    Args:
        n: Number of colors to generate
    
    Returns:
        List of RGB tuples with alpha channel
    """
    colors = []
    for i in range(n):
        hue = i / n
        r, g, b = colorsys.hsv_to_rgb(hue, 0.6, 1.0)
        colors.append((int(r * 255), int(g * 255), int(b * 255), 120))
    return colors


def chooseStyleGame(screen, theme, min_radius=10, spacing=15, color=(255, 0, 255), balles=[]):
    """
    Create circles based on the chosen theme.
    
    Args:
        screen: Pygame screen surface
        theme: Theme name string
        min_radius: Minimum radius for circles
        spacing: Spacing between concentric circles
        color: Default color for circles
        balles: List of balls (may be modified for some themes)
    
    Returns:
        List of Cercle objects
    """
    cercles = []

    if theme == "unicolor":
        cercles = _create_unicolor_circles(screen, min_radius, spacing, color)
    
    elif theme == "multicolor":
        cercles = _create_multicolor_circles(screen, min_radius, spacing)
    
    elif theme == "simpleCercle":
        cercles = _create_simple_circle(screen, min_radius)
    
    elif theme == "simpleCercleferme":
        cercles = _create_closed_circle(screen, min_radius)
    
    elif theme == "cageCercle":
        cercles = _create_cage_circle_2teams()
    
    elif theme == "cageCercle4":
        cercles = _create_cage_circle_4teams()
    
    elif theme == "triple":
        cercles = _create_triple_circles(balles)
    
    return cercles


def _create_unicolor_circles(screen, min_radius, spacing, color):
    """Create concentric circles with uniform color."""
    cercles = []
    for i in range(100):
        radius = min_radius + i * spacing
        if 2 * radius < min(screen.get_width(), screen.get_height()):
            start_deg = (i * 5) % 360
            end_deg = (start_deg + 20) % 360
            cercles.append(Cercle(radius, start_deg, end_deg, color=color))
    return cercles


def _create_multicolor_circles(screen, min_radius, spacing):
    """Create concentric circles with rainbow colors."""
    cercles = []
    colors = generate_circle_colors(60)
    for i in range(60):
        radius = min_radius + i * spacing
        if 2 * radius < min(screen.get_width(), screen.get_height()):
            start_deg = (i * 8) % 360
            end_deg = (start_deg + 20) % 360
            color = colors[i]
            cercles.append(Cercle(radius, start_deg, end_deg, color=color[:3]))
    return cercles


def _create_simple_circle(screen, min_radius):
    """Create a single simple circle."""
    cercles = []
    if 2 * min_radius < min(screen.get_width(), screen.get_height()):
        start_deg = 320
        end_deg = 360
        cercles.append(Cercle(min_radius, start_deg, end_deg, color=(248, 0, 154)))
    return cercles


def _create_closed_circle(screen, min_radius):
    """Create a closed circle (no opening)."""
    cercle1 = Cercle(min_radius, 0, 360, color=(217, 15, 241))
    cercle1.close = True
    return [cercle1]


def _create_cage_circle_2teams():
    """Create cage circle for 2-team mode."""
    rayon = 525
    cages = {
        1: (-20, 20),      # Red cage
        2: (160, 200),     # Green cage
        3: (20, 160),      # Solid white section
        4: (200, 340)      # Solid white section
    }

    cercle_cages = Cercle(rayon, 0, 360, color=(255, 0, 255), index=0, cages=cages)
    return [cercle_cages]


def _create_cage_circle_4teams():
    """Create cage circle for 4-team mode."""
    rayon = 525
    cages = {
        1: (0, 40),         # Red cage
        2: (90, 130),       # Red cage
        3: (180, 220),      # Red cage
        4: (270, 310),      # Red cage

        5: (40, 90),        # Solid white section
        6: (130, 180),      # Solid white section
        7: (220, 270),      # Solid white section
        8: (310, 360)       # Solid white section
    }

    cercle_cages = Cercle(rayon, 0, 360, color=(255, 0, 255), index=0, cages=cages)
    return [cercle_cages]


def _create_triple_circles(balles):
    """
    Create three circles positioned in a triangle around the center.
    Also creates initial balls for this mode.
    
    Args:
        balles: List to append created balls to
    
    Returns:
        List of three Cercle objects
    """
    cercles = []
    rayon = 250
    cx, cy = SCREEN_CENTER[0], SCREEN_CENTER[1]
    angle_offset = math.radians(120)
    
    for i in range(3):
        angle = i * angle_offset
        x = cx + 1.15 * rayon * math.cos(angle)
        y = cy + 1.15 * rayon * math.sin(angle)
        
        # Calculate angle toward center
        angle_vers_centre = math.atan2(cy - y, cx - x)
        
        # Opening span to create connection between circles
        arc_span = math.radians(30)
        
        # Reverse opening for circles 1 and 2
        if i == 1:
            angle_vers_centre += math.pi / 1.5
        if i == 2:
            angle_vers_centre -= math.pi / 1.5
        
        # Opening angles centered on direction toward center
        start_deg = math.degrees(angle_vers_centre - arc_span / 2)
        end_deg = math.degrees(angle_vers_centre + arc_span / 2)
        
        cercle = Cercle(rayon, start_deg, end_deg, color=(30, 14, 255), x=x, y=y)
        cercle.rotation_direction = 1 if i % 2 == 0 else -1
        cercles.append(cercle)
        
        # Create a ball for each circle
        balle = Balle(
            10,
            (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            ),
            (255, 255, 255),
            image_path=None,
            hidden_image=None,
            image_rect=None,
            position=(x, y),
            velocity=np.array([-8.0, -3.0]),
            rond=cercle
        )
        balles.append(balle)
    
    return cercles