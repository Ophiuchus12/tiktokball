#!/usr/bin/env python3
"""
Génère un fichier son minimal pour le jeu
"""
import wave
import struct
import math

def create_note_sound(filename, frequency=440, duration=0.1, sample_rate=44100):
    """Crée un fichier WAV avec une note simple"""
    num_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            # Génère une onde sinusoïdale avec enveloppe
            t = i / sample_rate
            envelope = 1.0 if t < duration * 0.8 else (1.0 - (t - duration * 0.8) / (duration * 0.2))
            value = int(32767.0 * 0.3 * envelope * math.sin(2.0 * math.pi * frequency * t))
            wav_file.writeframes(struct.pack('h', value))

if __name__ == "__main__":
    print("Création du fichier son...")
    create_note_sound("sounds/a.wav", frequency=440, duration=0.15)
    print("✅ sounds/a.wav créé avec succès")