class AlphaComponent:
    def __init__(self, alpha: float = 1.0):
        """
        Alpha component for transparency
        :param alpha: 0.0 (fully transparent) to 1.0 (fully opaque)
        """
        self.alpha = alpha  # 0.0 (transparent) to 1.0 (opaque)
        self.target_alpha = alpha  # Target alpha for smooth transitions
        self.animation_speed = (
            3.0  # How fast alpha changes - faster for more immediate response
        )
