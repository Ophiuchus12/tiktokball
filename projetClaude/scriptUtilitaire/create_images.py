#!/usr/bin/env python3
"""
Génère une image de fond pour le jeu
"""
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  PIL/Pillow non disponible")

def create_gradient_background():
    """Crée un fond avec gradient"""
    if not PIL_AVAILABLE:
        print("Installation: pip install Pillow")
        return False
    
    # Dimensions du jeu
    width, height = 1080, 1920
    
    # Crée l'image
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Gradient du haut vers le bas (noir vers bleu foncé)
    for y in range(height):
        # Calcule la couleur du gradient
        ratio = y / height
        r = int(10 * ratio)
        g = int(20 * ratio)
        b = int(40 + 40 * ratio)
        
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Ajoute quelques "étoiles"
    import random
    random.seed(42)  # Pour reproductibilité
    
    for _ in range(200):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        
        draw.ellipse([x-size, y-size, x+size, y+size], fill=(brightness, brightness, brightness))
    
    # Sauvegarde
    img.save("images/noir.jpg", quality=95)
    print("✅ images/noir.jpg créé avec succès")
    return True

def create_simple_background():
    """Crée un fond simple noir si PIL n'est pas disponible"""
    if not PIL_AVAILABLE:
        print("Création d'un fond noir simple...")
        return False
    
    img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))
    img.save("images/noir.jpg", quality=95)
    print("✅ images/noir.jpg (noir) créé avec succès")
    return True

if __name__ == "__main__":
    print("Création de l'image de fond...")
    if not create_gradient_background():
        create_simple_background()