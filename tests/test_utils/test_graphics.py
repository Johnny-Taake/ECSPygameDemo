"""Unit tests for graphics utility functions."""

from utils.graphics import apply_alpha


class TestApplyAlpha:
    """Test the apply_alpha function."""

    def test_apply_alpha_with_rgb_tuple(self):
        """Test apply_alpha with RGB tuple."""
        result = apply_alpha((255, 100, 50), 0.5)
        assert result == (127, 50, 25)

    def test_apply_alpha_with_rgba_tuple(self):
        """Test apply_alpha with RGBA tuple."""
        result = apply_alpha((255, 128, 64, 200), 0.5)
        assert result == (127, 64, 32, 100)

    def test_apply_alpha_with_alpha_1(self):
        """Test apply_alpha with alpha 1.0 (no change)."""
        result = apply_alpha((100, 200, 50), 1.0)
        assert result == (100, 200, 50)

    def test_apply_alpha_with_alpha_0(self):
        """Test apply_alpha with alpha 0.0 (fully transparent)."""
        result = apply_alpha((255, 128, 64), 0.0)
        assert result == (0, 0, 0)

    def test_apply_alpha_with_empty_tuple(self):
        """Test apply_alpha with empty tuple."""
        result = apply_alpha((), 0.5)
        assert result == ()

    def test_apply_alpha_with_large_values(self):
        """Test apply_alpha with values exceeding 255."""
        result = apply_alpha((300, 400, 500), 0.5)
        assert result == (150, 200, 250)

    def test_apply_alpha_with_negative_alpha(self):
        """Test apply_alpha with negative alpha."""
        result = apply_alpha((100, 150, 200), -0.5)
        assert result == (-50, -75, -100)
