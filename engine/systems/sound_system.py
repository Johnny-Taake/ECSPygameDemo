"""Sound system for the ECS framework."""

import pygame
from typing import Dict

from engine.components import SoundComponent


class SoundSystem:
    """System to handle sound playback."""

    def __init__(self):
        pygame.mixer.init()
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.enabled = True

    def load_sound(self, name: str, filepath: str) -> bool:
        """Load a sound file and store it with the given name."""
        try:
            sound = pygame.mixer.Sound(filepath)
            self.sounds[name] = sound
            return True
        except pygame.error as e:
            print(f"Could not load sound {filepath}: {e}")
            return False

    def play_sound(self, name: str, volume: float = 1.0) -> bool:
        """Play a sound by its name."""
        if not self.enabled:
            return False

        if name in self.sounds:
            sound = self.sounds[name]
            sound.set_volume(volume)
            sound.play()
            return True
        return False

    def play_sound_from_entity(self, entity) -> bool:
        """Play a sound from an entity's SoundComponent."""
        if not self.enabled:
            return False

        sound_component = entity.get(SoundComponent)
        if sound_component:
            return self.play_sound(sound_component.sound_name, sound_component.volume)
        return False

    def update(self, entities: list):
        """Process all entities with SoundComponents."""
        for entity in entities:
            sound_component = entity.get(SoundComponent)
            if sound_component and sound_component.play_on_add:
                # Play the sound and then disable play_on_add to avoid repeated playing
                self.play_sound(sound_component.sound_name, sound_component.volume)
                sound_component.play_on_add = False

    def set_volume(self, volume: float):
        """Set the global volume for all sounds."""
        if 0.0 <= volume <= 1.0:
            for sound in self.sounds.values():
                sound.set_volume(volume)

    def stop_all_sounds(self):
        """Stop all currently playing sounds."""
        pygame.mixer.stop()

    def enable_sounds(self):
        """Enable sound playback."""
        self.enabled = True

    def disable_sounds(self):
        """Disable sound playback."""
        self.enabled = False
