"""Sound system for the ECS framework."""

import pygame
from typing import Dict

from engine.components import SoundComponent
from logger import get_logger

log = get_logger("engine/sound_system")


class SoundSystem:
    """System to handle sound playback."""

    def __init__(self):
        pygame.mixer.init()
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.enabled = True
        log.info("SoundSystem initialized")

    def load_sound(self, name: str, filepath: str) -> bool:
        """Load a sound file and store it with the given name."""
        try:
            sound = pygame.mixer.Sound(filepath)
            self.sounds[name] = sound
            log.debug(f"Sound loaded successfully: {name} from {filepath}")
            return True
        except pygame.error as e:
            log.error(f"Could not load sound {filepath}: {e}")
            return False

    def play_sound(self, name: str, volume: float = 1.0) -> bool:
        """Play a sound by its name."""
        if not self.enabled:
            return False

        if name in self.sounds:
            sound = self.sounds[name]
            sound.set_volume(volume)
            sound.play()
            log.debug(f"Sound played: {name} (volume: {volume})")
            return True
        else:
            log.warning(f"Sound not found: {name}")
        return False

    def play_sound_from_entity(self, entity) -> bool:
        """Play a sound from an entity's SoundComponent."""
        if not self.enabled:
            return False

        sound_component = entity.get(SoundComponent)
        if sound_component:
            result = self.play_sound(sound_component.sound_name, sound_component.volume)
            if result:
                log.debug(f"Sound played from entity: {sound_component.sound_name}")
            return result
        return False

    def update(self, entities: list):
        """Process all entities with SoundComponents."""
        for entity in entities:
            sound_component = entity.get(SoundComponent)
            if sound_component and sound_component.play_on_add:
                # Play the sound and then disable play_on_add to avoid repeated playing
                self.play_sound(sound_component.sound_name, sound_component.volume)
                sound_component.play_on_add = False
                log.debug(f"Played sound from entity component: {sound_component.sound_name}")

    def set_volume(self, volume: float):
        """Set the global volume for all sounds."""
        if 0.0 <= volume <= 1.0:
            for sound in self.sounds.values():
                sound.set_volume(volume)
            log.debug(f"Global volume set to: {volume}")
        else:
            log.warning(f"Invalid volume value: {volume}, must be between 0.0 and 1.0")

    def stop_all_sounds(self):
        """Stop all currently playing sounds."""
        pygame.mixer.stop()
        log.debug("All sounds stopped")

    def enable_sounds(self):
        """Enable sound playback."""
        if not self.enabled:
            log.info("Sounds enabled")
        self.enabled = True

    def disable_sounds(self):
        """Disable sound playback."""
        if self.enabled:
            log.info("Sounds disabled")
        self.enabled = False
