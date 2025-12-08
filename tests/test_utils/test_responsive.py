"""Unit tests for responsive scaling utilities."""

from utils.responsive import ResponsiveScaleManager


class TestResponsiveScaleManager:
    """Test the ResponsiveScaleManager class."""

    def test_initialization_default_values(self):
        """Test initialization with default values."""
        manager = ResponsiveScaleManager()
        assert manager.base_width == 640
        assert manager.base_height == 400
        assert manager.window_width == 640
        assert manager.window_height == 400
        assert manager.scale == 1.0
        assert manager.offset_x == 0
        assert manager.offset_y == 0

    def test_initialization_custom_values(self):
        """Test initialization with custom base dimensions."""
        manager = ResponsiveScaleManager(base_width=800, base_height=600)
        assert manager.base_width == 800
        assert manager.base_height == 600
        assert manager.window_width == 800
        assert manager.window_height == 600

    def test_update_window_size_same_aspect_ratio(self):
        """Test updating window size with same aspect ratio."""
        manager = ResponsiveScaleManager(
            base_width=640, base_height=400
        )  # 16:10 aspect ratio
        manager.update_window_size(800, 500)  # Also 16:10 aspect ratio

        assert manager.scale == 1.25  # 800 / 640 = 1.25
        assert manager.offset_x == 0
        assert manager.offset_y == 0

    def test_update_window_size_wider_window(self):
        """Test updating window size when window is wider than base aspect ratio."""
        manager = ResponsiveScaleManager(
            base_width=640, base_height=400
        )  # 16:10 aspect ratio
        manager.update_window_size(
            1000, 500
        )  # Wider window (2:1) compared to base (16:10)

        # Height should be limiting factor: scale = 500 / 400 = 1.25
        # Width at this scale: 640 * 1.25 = 800
        # Offset_x = (1000 - 800) / 2 = 100
        assert manager.scale == 1.25
        assert manager.offset_x == 100
        assert manager.offset_y == 0

    def test_update_window_size_narrower_window(self):
        """Test updating window size when window is narrower than base aspect ratio."""
        manager = ResponsiveScaleManager(
            base_width=640, base_height=400
        )  # 16:10 aspect ratio
        manager.update_window_size(
            640, 600
        )  # Narrower window (8:15) compared to base (16:10)

        # Width should be limiting factor: scale = 640 / 640 = 1.0
        # Height at this scale: 400 * 1.0 = 400
        # Offset_y = (600 - 400) / 2 = 100
        assert manager.scale == 1.0
        assert manager.offset_x == 0
        assert manager.offset_y == 100

    def test_world_to_screen_conversion(self):
        """Test conversion from world coordinates to screen coordinates."""
        manager = ResponsiveScaleManager()
        # Set up a scenario: window is 1280x800, so scale would be 2.0, with no offset
        manager.update_window_size(1280, 800)  # scale = 2.0, no offset

        screen_x, screen_y = manager.world_to_screen(100, 50)
        # Expected: 0 + 100*2 = 200, 0 + 50*2 = 100
        assert screen_x == 200
        assert screen_y == 100

    def test_world_to_screen_with_offset(self):
        """Test conversion from world to screen with offset (letterboxing)."""
        manager = ResponsiveScaleManager()
        # Window is 1600x800 but base is 640x400, so scale = 2, offset_x = (1600-1280)/2 = 160
        manager.update_window_size(1600, 800)  # scale = 2.0, offset_x = 160

        screen_x, screen_y = manager.world_to_screen(100, 50)
        # Expected: 160 + 100*2 = 360, 0 + 50*2 = 100
        assert screen_x == 360
        assert screen_y == 100

    def test_screen_to_world_conversion(self):
        """Test conversion from screen coordinates to world coordinates."""
        manager = ResponsiveScaleManager()
        manager.update_window_size(1280, 800)  # scale = 2.0, no offset

        world_x, world_y = manager.screen_to_world(200, 100)
        # Expected: (200 - 0) / 2 = 100, (100 - 0) / 2 = 50
        assert world_x == 100
        assert world_y == 50

    def test_screen_to_world_with_offset(self):
        """Test conversion from screen to world with offset."""
        manager = ResponsiveScaleManager()
        # Window is 1600x800 but base is 640x400, so scale = 2, offset_x = 160
        manager.update_window_size(1600, 800)  # scale = 2.0, offset_x = 160

        world_x, world_y = manager.screen_to_world(360, 100)
        # Expected: (360 - 160) / 2 = 100, (100 - 0) / 2 = 50
        assert world_x == 100
        assert world_y == 50

    def test_no_scaling_needed(self):
        """Test scenario where no scaling is needed."""
        manager = ResponsiveScaleManager()
        manager.update_window_size(640, 400)  # Same as base dimensions

        assert manager.scale == 1.0
        assert manager.offset_x == 0
        assert manager.offset_y == 0

    def test_extreme_window_ratio(self):
        """Test with very wide or very tall window."""
        # Very wide window
        manager = ResponsiveScaleManager(base_width=640, base_height=400)
        manager.update_window_size(2000, 400)  # Very wide

        # Height is limiting: scale = 400/400 = 1.0
        # Rendered width: 640 * 1.0 = 640
        # Offset_x = (2000 - 640) / 2 = 680
        assert manager.scale == 1.0
        assert manager.offset_x == 680
        assert manager.offset_y == 0

    def test_square_to_rectangle_scaling(self):
        """Test scaling from square to rectangular display."""
        manager = ResponsiveScaleManager(base_width=400, base_height=400)  # Square base
        manager.update_window_size(600, 400)  # Rectangular window

        # Width is limiting: scale = 600/400 = 1.5
        # Rendered height: 400 * 1.5 = 600, but window is only 400
        # Actually: scale = 400/400 = 1.0 (height limiting)
        # Rendered width: 400 * 1.0 = 400
        # Offset_x = (600 - 400) / 2 = 100
        assert manager.scale == 1.0
        assert manager.offset_x == 100
        assert manager.offset_y == 0
