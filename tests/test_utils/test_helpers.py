"""Unit tests for helper utility functions."""

from utils.helpers import (
    format_timestamp,
    is_signed_integer,
    is_positive_integer,
    is_in_range,
    is_point_in_rect,
)


class TestFormatTimestamp:
    """Test the format_timestamp function."""

    def test_format_timestamp_basic(self):
        """Test format_timestamp with a sample timestamp."""
        # This function relies on datetime parsing, so we'll just verify it does not error
        result = format_timestamp("2025-12-08T10:30:00")
        # Check that result contains expected elements for a readable format
        assert isinstance(result, str)
        assert "Dec" in result or "Dec'" in result  # Month should be represented


class TestIsSignedInteger:
    """Test the is_signed_integer function."""

    def test_is_signed_integer_positive(self):
        """Test is_signed_integer with positive integers."""
        assert is_signed_integer("123")
        assert is_signed_integer("0")
        assert is_signed_integer("42")

    def test_is_signed_integer_negative(self):
        """Test is_signed_integer with negative integers."""
        assert is_signed_integer("-123")
        assert is_signed_integer("-1")

    def test_is_signed_integer_invalid(self):
        """Test is_signed_integer with invalid inputs."""
        assert not is_signed_integer("abc")
        assert not is_signed_integer("12.34")
        assert not is_signed_integer("-")
        assert not is_signed_integer("-ab")
        assert not is_signed_integer("")
        assert not is_signed_integer("12-34")
        assert not is_signed_integer("--123")


class TestIsPositiveInteger:
    """Test the is_positive_integer function."""

    def test_is_positive_integer_positive(self):
        """Test is_positive_integer with positive integers."""
        assert is_positive_integer("123")
        assert is_positive_integer("0")
        assert is_positive_integer("42")

    def test_is_positive_integer_negative(self):
        """Test is_positive_integer with negative integers."""
        assert not is_positive_integer("-123")
        assert not is_positive_integer("-1")

    def test_is_positive_integer_invalid(self):
        """Test is_positive_integer with invalid inputs."""
        assert not is_positive_integer("abc")
        assert not is_positive_integer("12.34")
        assert not is_positive_integer("-")
        assert not is_positive_integer("")
        assert not is_positive_integer("12-34")


class TestIsInRange:
    """Test the is_in_range function."""

    def test_is_in_range_in_range(self):
        """Test is_in_range with values within range."""
        assert is_in_range(5, 1, 10)
        assert is_in_range(1, 1, 10)  # boundary
        assert is_in_range(10, 1, 10)  # boundary
        assert is_in_range(0.5, 0, 1)
        assert is_in_range(-5, -10, 0)

    def test_is_in_range_out_of_range(self):
        """Test is_in_range with values outside range."""
        assert not is_in_range(11, 1, 10)
        assert not is_in_range(0, 1, 10)
        assert not is_in_range(-1, 1, 10)
        assert not is_in_range(10.1, 1, 10)
        assert not is_in_range(-11, -10, 0)


class TestIsPointInRect:
    """Test the is_point_in_rect function."""

    def test_is_point_in_rect_center(self):
        """Test is_point_in_rect with point at center of rectangle."""
        # Point at center of 100x100 rectangle centered at (0,0)
        assert is_point_in_rect(0, 0, 0, 0, 100, 100)

    def test_is_point_in_rect_edge(self):
        """Test is_point_in_rect with point at edge of rectangle."""
        # Point at edge of 100x100 rectangle centered at (0,0)
        assert is_point_in_rect(50, 0, 0, 0, 100, 100)  # Right edge
        assert is_point_in_rect(-50, 0, 0, 0, 100, 100)  # Left edge
        assert is_point_in_rect(0, 50, 0, 0, 100, 100)  # Bottom edge
        assert is_point_in_rect(0, -50, 0, 0, 100, 100)  # Top edge

    def test_is_point_in_rect_outside(self):
        """Test is_point_in_rect with point outside rectangle."""
        assert not is_point_in_rect(51, 0, 0, 0, 100, 100)  # Just outside right
        assert not is_point_in_rect(-51, 0, 0, 0, 100, 100)  # Just outside left
        assert not is_point_in_rect(0, 51, 0, 0, 100, 100)  # Just outside bottom
        assert not is_point_in_rect(0, -51, 0, 0, 100, 100)  # Just outside top

    def test_is_point_in_rect_different_position(self):
        """Test is_point_in_rect with different rectangle position."""
        # Rectangle centered at (10, 20) with size 40x40
        assert is_point_in_rect(10, 20, 10, 20, 40, 40)  # Center
        assert is_point_in_rect(30, 20, 10, 20, 40, 40)  # Right edge
        assert is_point_in_rect(-10, 20, 10, 20, 40, 40)  # Left edge
        assert not is_point_in_rect(31, 20, 10, 20, 40, 40)  # Just outside right
