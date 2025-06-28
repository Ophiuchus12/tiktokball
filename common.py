import numpy as np


def check_balls_collision(b1, b2):
    direction = b2.position - b1.position
    distance = np.linalg.norm(direction)
    sum_radius = b1.radius + b2.radius

    return distance < sum_radius

def resolve_ball_collision(ball1, ball2):
    direction = ball2.position - ball1.position
    distance = np.linalg.norm(direction)

    if distance == 0:
        return  # éviter division par zéro

    # Normalisation
    normal = direction / distance

    # Vitesse relative
    relative_velocity = ball2.velocity - ball1.velocity

    # Projeter la vitesse relative sur la normale
    velocity_along_normal = np.dot(relative_velocity, normal)

    if velocity_along_normal >= 0:
        return  # Les balles s’éloignent déjà

    # Masse (si tu veux généraliser plus tard, ici masses égales)
    restitution = 1.0  # collision parfaitement élastique

    # Impulsion scalaire
    impulse_scalar = -(1 + restitution) * velocity_along_normal / 2
    impulse = impulse_scalar * normal

    # Appliquer l'impulsion (conservation quantité de mouvement)
    ball1.velocity -= impulse
    ball2.velocity += impulse

    # Correction position : éviter que les balles restent collées
    overlap = (ball1.radius + ball2.radius) - distance
    if overlap > 0:
        correction = normal * (overlap / 2)
        ball1.position -= correction
        ball2.position += correction

    # Optionnel : déclencher effet rebond visuel/sonore
    ball1.on_bounce()
    ball2.on_bounce()




def handleBallCollision (balles):
    # Gère les collisions entre toutes les paires de balles
    handled_pairs = set()
    for i in range(len(balles)):
        for j in range(i + 1, len(balles)):
            if (i, j) not in handled_pairs:
                b1, b2 = balles[i], balles[j]
                if check_balls_collision(b1, b2):
                    resolve_ball_collision(b1, b2)
                    handled_pairs.add((i, j))