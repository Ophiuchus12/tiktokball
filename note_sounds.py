import pygame

def load_note_sounds():
    note_map = {}
    #note_names = ['f4', 'g4', 'c5', 'b4', 'a', 'z']
    note_names = ['a']
    base_midi = 60  # C4

    for i, name in enumerate(note_names):
        note_map[base_midi + i] = pygame.mixer.Sound(f"sounds/{name}.wav")
        note_map[base_midi + i].set_volume(0.4)

    return note_map
