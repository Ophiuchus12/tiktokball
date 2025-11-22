"""
Constants used throughout the TikTok Ball Game.
Centralizes all magic numbers, configuration values, and string literals.

Organization:
- Screen dimensions and positions
- Physics parameters (gravity, velocity)
- Entity settings (balls, circles, squares)
- Collision detection parameters
- Game modes and visual effects
- Rendering and UI settings
- Audio configuration
- File paths and resources
"""
import numpy as np

# ==================== SCREEN ====================
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1920
SCREEN_CENTER = np.array([SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2], dtype=float)

# ==================== PHYSICS ====================
GRAVITY = 0.2
DEFAULT_VELOCITY_RANGE = (-5, 5)
VELOCITY_MULTIPLIER = 1.02
DEFAULT_BALL_SPEED = 15
BOUNCE_VELOCITY_MULTIPLIER = 0.95
DEFAULT_ROTATION_SPEED_MIN = 0.005
DEFAULT_ROTATION_SPEED_MAX = 0.01

# ==================== BALL SETTINGS ====================
DEFAULT_BALL_RADIUS = 20
IMAGE_SCALE_FACTOR = 1.8
MAX_TRAIL_LENGTH = 15
BALL_VOLUME = 0.4  # Volume audio des balles (0.0 à 1.0)

# ==================== COLLISION DETECTION ====================
MIN_COLLISION_FRAMES = 3
MIN_CAGE_CHANGE_FRAMES = 10
OVERLAP_CORRECTION_FACTOR = 1.0
COLLISION_OVERLAP_TOLERANCE = 0.1

# ==================== CIRCLE SETTINGS ====================
DEFAULT_MIN_RADIUS = 200
DEFAULT_SPACING = 15
ROTATION_SPEED_MIN = 0.005
ROTATION_SPEED_MAX = 0.01
CERCLE_WIDTH = 9  # Épaisseur du trait des cercles
DEATH_ANIMATION_DURATION = 30
SHARD_COUNT = 10
SHARD_SPEED_MIN = 3
SHARD_SPEED_MAX = 6
SHARD_LENGTH_MIN = 20
SHARD_LENGTH_MAX = 40

# ==================== RENDERING ====================
FPS = 60
FONT_SIZE = 60
DEFAULT_FONT_SIZE = 60

# ==================== AUDIO ====================
AUDIO_FREQUENCY = 44100
AUDIO_SIZE = -16  # 16-bit signed
AUDIO_CHANNELS = 2  # Stéréo
AUDIO_BUFFER = 512
MIXER_CHANNELS = 32  # Nombre de canaux audio simultanés
DEFAULT_VOLUME = 0.4

# ==================== GAME SETTINGS ====================
TOTAL_FRAMES = 60 * 85
TIMER_DURATION = 60  # Durée du timer en secondes
DEFAULT_TIMER = 60  # Alias pour compatibilité

# ==================== FILE PATHS ====================
# Fonts
FONT_PATH = "ressources/font/symbola/Symbola.ttf"

# Sounds
SOUNDS_PATH = "sounds"

# Images
IMAGES_PATH = "images"
DEFAULT_BACKGROUND = "images/noir.jpg"
HIDDEN_IMAGE_PATH = "images/logo.png"
HIDDEN_IMAGE_SIZE = (600, 600)

# Configuration
CONFIG_PATH = "config.json"
CONFIG_FILE = "config.json"  # Alias pour compatibilité

# ==================== GAME MODES ====================
# Modes principaux de jeu
MODE_CLASSIQUE = "classique"
MODE_SIMPLE_CERCLE = "simpleCercle"
MODE_SIMPLE_CERCLE_FERME = "simpleCercleferme"
MODE_REBOND_INFINI = "rebondInfini"
MODE_CAGE_CERCLE = "cageCercle"
MODE_CAGE_CERCLE_4 = "cageCercle4"
MODE_TRIPLE_CERCLE = "tripleCercle"

# Modes de gameplay (pour le launcher)
GAMEPLAY_MODE_CLASSIQUE = "classique"
GAMEPLAY_MODE_DOUBLE = "double"
GAMEPLAY_MODE_QUADRUPLE = "quadruple"
GAMEPLAY_MODE_MULTI = "multi"
GAMEPLAY_MODE_SIMPLE = "simple"
GAMEPLAY_MODE_INFINI = "infini"

# ==================== VISUAL BALL MODES ====================
# Modes d'affichage des balles
BALL_MODE_NONE = "none"
BALL_MODE_INVISIBLE = "invisible"
BALL_MODE_TRAINEE = "trainee"
BALL_MODE_TRACE = "trace"

# ==================== BOUNCE EFFECT MODES ====================
# Effets lors du rebond
BOUNCE_MODE_NONE = "none"
BOUNCE_MODE_LINKED = "linked"
BOUNCE_MODE_CAGE = "cage"

# ==================== CIRCLE THEMES ====================
# Thèmes d'apparence des cercles
THEME_UNICOLOR = "unicolor"
THEME_MULTICOLOR = "multicolor"
THEME_SIMPLE_CERCLE = "simpleCercle"
THEME_SIMPLE_CERCLE_FERME = "simpleCercleferme"
THEME_INFINI = "infini"
THEME_CAGE_CERCLE = "cageCercle"
THEME_CAGE_CERCLE_4 = "cageCercle4"
THEME_TRIPLE = "triple"

# ==================== ROTATION MODES ====================
# Modes de rotation des cercles
ROTATION_FREE = "free"
ROTATION_STUCK = "stuck"
ROTATION_NONE = "none"

# ==================== COLORS (RGB) ====================
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_MAGENTA = (255, 0, 255)

# Couleurs par défaut
DEFAULT_CIRCLE_COLOR = (255, 56, 60)
DEFAULT_BALL_COLOR_IN = (255, 255, 78)
DEFAULT_BALL_COLOR_BORDER = (255, 255, 60)

# ==================== UI SETTINGS ====================
LOGO_SIZE = (120, 100)
SCORE_SPACING = 300
SCORE_Y_OFFSET = 1250
TIMER_Y_OFFSET = 30
TEXT_Y_POSITION = 300
TITLE_Y_POSITION = 100

# ==================== SCREEN BOUNDARIES ====================
# Marges pour détection de sortie d'écran
SCREEN_MARGIN = 100
OFFSCREEN_THRESHOLD = SCREEN_MARGIN

# ==================== DEFAULT CONFIGURATIONS ====================
# Configuration par défaut des cercles
DEFAULT_CIRCLE_CONFIG = {
    "min_radius": DEFAULT_MIN_RADIUS,
    "spacing": DEFAULT_SPACING,
    "rotation_speed_min": ROTATION_SPEED_MIN,
    "rotation_speed_max": ROTATION_SPEED_MAX,
    "width": CERCLE_WIDTH,
}

# Configuration par défaut des balles
DEFAULT_BALL_CONFIG = {
    "radius": DEFAULT_BALL_RADIUS,
    "color_in": DEFAULT_BALL_COLOR_IN,
    "color_border": DEFAULT_BALL_COLOR_BORDER,
    "gravity_enabled": True,
    "mode": BALL_MODE_NONE,
    "on_bounce": BOUNCE_MODE_NONE,
}

# Configuration par défaut du jeu
DEFAULT_GAME_CONFIG = {
    "background": DEFAULT_BACKGROUND,
    "cercles_theme": THEME_UNICOLOR,
    "cercles_color": DEFAULT_CIRCLE_COLOR,
    "timer": TIMER_DURATION,
    "mode_jeu": MODE_CLASSIQUE,
    "min_radius": DEFAULT_MIN_RADIUS,
}

# ==================== AUDIO NOTES ====================
# Notes MIDI pour les sons
NOTE_NAMES = ['a']  # Peut être étendu: ['c4', 'f4', 'g4', 'a4', 'c5', 'd5', 'f5', 'g5']

# ==================== DEBUG ====================
DEBUG_MODE = False
SHOW_FPS = False
SHOW_COLLISION_ZONES = False