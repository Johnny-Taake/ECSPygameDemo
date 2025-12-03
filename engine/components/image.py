"""Image component for the ECS system."""

from typing import Optional
import pygame


class ImageComponent:
    """Component to hold image-related data."""

    def __init__(
        self,
        image_path: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        """
        Initialize the image component.

        :param image_path: Path to the image file
        :param width: Optional width to resize the image
        :param height: Optional height to resize the image
        """
        self.image_path = image_path
        self.width = width
        self.height = height
        self.pygame_image: Optional[pygame.Surface] = None
