"""
Common utility functions for the game.
Handles ball creation and collision physics.
"""
import numpy as np
from entite.balle import Balle


def createBall(
    radius=None,
    color=None,
    colorIn=None,
    note_sounds=None,
    image_path=None,
    hidden_image=None,
    image_rect=None,
    position=None,
    velocity=None,
    cage=None,
    rond=None
):
    """Create a ball with the given parameters."""
    return Balle(
        radius=radius,
        color=color,
        colorIn=colorIn,
        image_path=image_path,
        hidden_image=hidden_image,
        image_rect=image_rect,
        position=position,
        velocity=velocity,
        cage=cage,
        rond=rond
    )


def check_balls_collision(b1, b2):
    """Check if two balls are colliding."""
    direction = b2.position - b1.position
    distance = np.linalg.norm(direction)
    sum_radius = b1.radius + b2.radius

    return distance < sum_radius


def resolve_ball_collision(ball1, ball2):
    """Resolve collision between two balls using elastic collision physics."""
    
    # ⭐ FIX: Convertir en float
    ball1.velocity = ball1.velocity.astype(float)
    ball2.velocity = ball2.velocity.astype(float)
    direction = ball2.position - ball1.position
    distance = np.linalg.norm(direction)

    if distance == 0:
        return  # Avoid division by zero

    # Normalization
    normal = direction / distance

    # Relative velocity
    relative_velocity = ball2.velocity - ball1.velocity

    # Project relative velocity onto normal
    velocity_along_normal = np.dot(relative_velocity, normal)

    if velocity_along_normal >= 0:
        return  # Balls are already separating

    # Restitution coefficient (perfectly elastic collision)
    restitution = 1.0

    # Scalar impulse
    impulse_scalar = -(1 + restitution) * velocity_along_normal / 2
    impulse = impulse_scalar * normal

    # Apply impulse (conservation of momentum)
    ball1.velocity -= impulse
    ball2.velocity += impulse

    # Position correction: prevent balls from staying stuck
    overlap = (ball1.radius + ball2.radius) - distance
    if overlap > 0:
        correction = normal * (overlap / 2)
        ball1.position -= correction
        ball2.position += correction

    # Trigger bounce effects
    ball1.on_bounce()
    ball2.on_bounce()


def handleBallCollision(balles):
    """
    Handle collisions between all pairs of balls.
    Uses a set to track handled pairs and avoid duplicate processing.
    """
    handled_pairs = set()
    for i in range(len(balles)):
        for j in range(i + 1, len(balles)):
            if (i, j) not in handled_pairs:
                b1, b2 = balles[i], balles[j]
                if check_balls_collision(b1, b2):
                    resolve_ball_collision(b1, b2)
                    handled_pairs.add((i, j))