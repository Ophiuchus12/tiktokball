"""
Gestion de la configuration du jeu
"""
import json
from typing import Any, Dict, List
from constants import *


class GameConfig:
    """Classe pour gérer la configuration du jeu"""
    
    def __init__(self, config_path: str = CONFIG_PATH):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration depuis le fichier JSON"""
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Configuration file not found: {self.config_path}")
            print("Using default configuration")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in config file: {e}")
            print("Using default configuration")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Retourne la configuration par défaut"""
        return {
            "background": "images/noir.jpg",
            "cerclesTheme": "unicolor",
            "cerclesColor": [255, 56, 60],
            "timer": TIMER_DURATION,
            "modeJeu": MODE_CLASSIQUE,
            "min_radius": DEFAULT_MIN_RADIUS,
            "balles_custom": [],
            "balleOptionsAvanced": {
                "mode": BALL_MODE_NONE,
                "onBounce": BOUNCE_MODE_NONE
            }
        }
    
    def save(self):
        """Sauvegarde la configuration actuelle"""
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur de configuration"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Définit une valeur de configuration"""
        self.config[key] = value
    
    # Propriétés pratiques
    @property
    def background(self) -> str:
        return self.get("background", "images/noir.jpg")
    
    @property
    def cercles_theme(self) -> str:
        return self.get("cerclesTheme", "unicolor")
    
    @property
    def cercles_color(self) -> List[int]:
        return self.get("cerclesColor", [255, 56, 60])
    
    @property
    def timer(self) -> int:
        return self.get("timer", TIMER_DURATION)
    
    @property
    def mode_jeu(self) -> str:
        return self.get("modeJeu", MODE_CLASSIQUE)
    
    @property
    def min_radius(self) -> int:
        return self.get("min_radius", DEFAULT_MIN_RADIUS)
    
    @property
    def balles_custom(self) -> List[Dict]:
        return self.get("balles_custom", [])
    
    @property
    def balle_mode(self) -> str:
        return self.get("balleOptionsAvanced", {}).get("mode", BALL_MODE_NONE)
    
    @property
    def balle_on_bounce(self) -> str:
        return self.get("balleOptionsAvanced", {}).get("onBounce", BOUNCE_MODE_NONE)