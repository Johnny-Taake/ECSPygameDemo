"""Sound component for the ECS system."""


class SoundComponent:
    """Component to hold sound-related data."""

    def __init__(self, sound_name: str):
        """
        Initialize the sound component.

        :param sound_name: Name of the sound to play (will be mapped to a sound file)
        """
        self.sound_name: str = sound_name
        self.play_on_add: bool = False  # Whether to play the sound when component is added
        self.volume: float = 1.0  # Volume level (0.0 to 1.0)
        self.loop: bool = False  # Whether to loop the sound
