"""
Configuration manager for the game.
Handles loading, saving, and accessing configuration values.
"""
import json
import os
from config.constants import CONFIG_FILE, DEFAULT_BACKGROUND, DEFAULT_TIMER, DEFAULT_MIN_RADIUS


class ConfigManager:
    """Manages game configuration with defaults and error handling."""
    
    def __init__(self, config_path=CONFIG_FILE):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file with error handling."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    return config
            else:
                print(f"Config file not found, using defaults")
                return self._get_default_config()
        except json.JSONDecodeError as e:
            print(f"Invalid config file: {e}. Using defaults.")
            return self._get_default_config()
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
            return self._get_default_config()
    
    def _get_default_config(self):
        """Return default configuration."""
        return {
            "background": DEFAULT_BACKGROUND,
            "cerclesTheme": "unicolor",
            "cerclesColor": [255, 56, 60],
            "timer": DEFAULT_TIMER,
            "modeJeu": "classique",
            "min_radius": DEFAULT_MIN_RADIUS,
            "balles_custom": [],
            "balleOptionsAvanced": {
                "mode": "none",
                "onBounce": "none"
            }
        }
    
    def save(self):
        """Save current configuration to file."""
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get a configuration value with optional default."""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value."""
        self.config[key] = value
    
    def get_ball_mode(self):
        """Get ball visual mode (invisible, trainee, trace, none)."""
        advanced = self.config.get("balleOptionsAvanced", {})
        return advanced.get("mode", "none")
    
    def get_bounce_mode(self):
        """Get bounce behavior mode (linked, cage, none)."""
        advanced = self.config.get("balleOptionsAvanced", {})
        return advanced.get("onBounce", "none")
    
    def get_circle_theme(self):
        """Get circle theme."""
        return self.config.get("cerclesTheme", "unicolor")
    
    def get_circle_color(self):
        """Get circle color as tuple."""
        color = self.config.get("cerclesColor", [255, 0, 255])
        return tuple(color) if isinstance(color, list) else color
    
    def get_game_mode(self):
        """Get game mode."""
        return self.config.get("modeJeu", "classique")
    
    def get_custom_balls(self):
        """Get list of custom ball configurations."""
        return self.config.get("balles_custom", [])


# Global config instance
_config_instance = None


def get_config():
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance