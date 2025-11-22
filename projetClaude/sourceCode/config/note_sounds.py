"""
Module de chargement des sons
"""
import pygame
from constants import *


def load_note_sounds():
    """Charge les sons de notes"""
    note_map = {}
    note_names = ['a']
    base_midi = 60  # C4
    
    for i, name in enumerate(note_names):
        try:
            sound = pygame.mixer.Sound(f"{SOUNDS_PATH}/{name}.wav")
            sound.set_volume(BALL_VOLUME)
            note_map[base_midi + i] = sound
        except Exception as e:
            print(f"Warning: Could not load sound {name}.wav: {e}")
            # Créer un son silencieux par défaut
            note_map[base_midi + i] = pygame.mixer.Sound(buffer=b'\x00' * 1000)
    
    return note_map