from game.logic import GameLogic, GuessStatus


class TestGameLogic:
    def test_game_logic_initialization_with_custom_range(self):
        """Test GameLogic initialization with custom min/max values."""
        game_logic = GameLogic(min_number=1, max_number=10)
        assert game_logic.min_number == 1
        assert game_logic.max_number == 10
        assert game_logic.attempts == 0

    def test_game_logic_initialization_with_defaults(self):
        """Test GameLogic initialization with default values from config."""
        # Test with default values (this should use values from config)
        game_logic = GameLogic()
        # The values will depend on the default difficulty from config
        assert game_logic.min_number is not None
        assert game_logic.max_number is not None
        assert game_logic.attempts == 0

    def test_generate_new_number(self):
        """Test that generate_new_number creates a random number in range."""
        game_logic = GameLogic(min_number=1, max_number=10)
        game_logic.generate_new_number()

        # Verify the number is within the expected range
        assert (
            game_logic.min_number <= game_logic.number_to_guess <= game_logic.max_number
        )

    def test_reset_game_logic(self):
        """Test that reset properly resets the game state."""
        game_logic = GameLogic(min_number=1, max_number=10)
        game_logic.generate_new_number()
        game_logic.attempts = 5  # Simulate some attempts

        game_logic.reset()

        # Verify attempts are reset to 0
        assert game_logic.attempts == 0
        # Verify a new number is generated (should be different, though possibly the same value by coincidence)
        assert (
            game_logic.min_number <= game_logic.number_to_guess <= game_logic.max_number
        )

    def test_check_invalid_format_empty_input(self):
        """Test that check returns INVALID_FORMAT for empty input."""
        game_logic = GameLogic(min_number=1, max_number=10)
        game_logic.generate_new_number()

        result = game_logic.check("")
        assert result == GuessStatus.INVALID_FORMAT

    def test_check_invalid_format_non_numeric(self):
        """Test that check returns INVALID_FORMAT for non-numeric input."""
        game_logic = GameLogic(min_number=1, max_number=10)
        game_logic.generate_new_number()

        result = game_logic.check("abc")
        assert result == GuessStatus.INVALID_FORMAT

        result = game_logic.check("12.5")  # Decimal is not valid
        assert result == GuessStatus.INVALID_FORMAT

        result = game_logic.check("!@#")
        assert result == GuessStatus.INVALID_FORMAT

    def test_check_invalid_format_with_special_characters(self):
        """Test that check handles special characters correctly."""
        game_logic = GameLogic(min_number=1, max_number=10)
        game_logic.generate_new_number()

        result = game_logic.check("12a")
        assert result == GuessStatus.INVALID_FORMAT

        result = game_logic.check("a12")
        assert result == GuessStatus.INVALID_FORMAT

    def test_check_out_of_range_low(self):
        """Test that check returns OUT_OF_RANGE for numbers below minimum."""
        game_logic = GameLogic(min_number=5, max_number=10)
        game_logic.generate_new_number()

        result = game_logic.check("3")
        assert result == GuessStatus.OUT_OF_RANGE

    def test_check_out_of_range_high(self):
        """Test that check returns OUT_OF_RANGE for numbers above maximum."""
        game_logic = GameLogic(min_number=1, max_number=5)
        game_logic.generate_new_number()

        result = game_logic.check("10")
        assert result == GuessStatus.OUT_OF_RANGE

    def test_check_too_low(self):
        """Test that check returns TOO_LOW for numbers below the target."""
        game_logic = GameLogic(min_number=1, max_number=10)
        # Set the target to 7 for predictable testing
        game_logic.number_to_guess = 7
        game_logic.min_number = 1
        game_logic.max_number = 10

        result = game_logic.check("3")
        assert result == GuessStatus.TOO_LOW

    def test_check_too_high(self):
        """Test that check returns TOO_HIGH for numbers above the target."""
        game_logic = GameLogic(min_number=1, max_number=10)
        # Set the target to 3 for predictable testing
        game_logic.number_to_guess = 3
        game_logic.min_number = 1
        game_logic.max_number = 10

        result = game_logic.check("8")
        assert result == GuessStatus.TOO_HIGH

    def test_check_correct(self):
        """Test that check returns CORRECT when the guess matches the target."""
        game_logic = GameLogic(min_number=1, max_number=10)
        # Set the target to 5 for predictable testing
        game_logic.number_to_guess = 5
        game_logic.min_number = 1
        game_logic.max_number = 10

        result = game_logic.check("5")
        assert result == GuessStatus.CORRECT

    def test_attempts_count_correctly(self):
        """Test that attempts are counted correctly for valid guesses."""
        game_logic = GameLogic(min_number=1, max_number=10)
        game_logic.number_to_guess = 5

        # First valid attempt
        game_logic.check("3")
        assert game_logic.attempts == 1

        # Second valid attempt
        game_logic.check("7")
        assert game_logic.attempts == 2

        # Invalid attempt should not count
        game_logic.check("invalid")
        assert game_logic.attempts == 2  # Should still be 2

        # Valid attempt should count
        game_logic.check("5")  # Correct guess
        assert game_logic.attempts == 3

    def test_check_negative_numbers_in_range(self):
        """Test that negative numbers work when in the allowed range."""
        game_logic = GameLogic(min_number=-10, max_number=10)
        game_logic.number_to_guess = 0

        result = game_logic.check("-5")
        assert result == GuessStatus.TOO_LOW

        result = game_logic.check("5")
        assert result == GuessStatus.TOO_HIGH

    def test_check_single_digit_range(self):
        """Test game logic with a single-digit range."""
        game_logic = GameLogic(min_number=5, max_number=5)
        game_logic.number_to_guess = 5

        result = game_logic.check("5")
        assert result == GuessStatus.CORRECT

        result = game_logic.check("4")
        assert result == GuessStatus.OUT_OF_RANGE

    def test_check_large_range(self):
        """Test game logic with a large range."""
        game_logic = GameLogic(min_number=1, max_number=1000)
        game_logic.number_to_guess = 500

        result = game_logic.check("250")
        assert result == GuessStatus.TOO_LOW

        result = game_logic.check("750")
        assert result == GuessStatus.TOO_HIGH

    def test_check_with_whitespace(self):
        """Test game logic handles whitespace in input."""
        game_logic = GameLogic(min_number=1, max_number=10)
        game_logic.number_to_guess = 5

        # Test with whitespace (this should still be invalid format as it's not pure numeric)
        result = game_logic.check(" 5 ")
        assert result == GuessStatus.INVALID_FORMAT

    def test_check_handles_multiple_attempts(self):
        """Test the flow of multiple game attempts."""
        game_logic = GameLogic(min_number=1, max_number=10)
        game_logic.number_to_guess = 6

        # First attempt - too low
        result = game_logic.check("3")
        assert result == GuessStatus.TOO_LOW
        assert game_logic.attempts == 1

        # Second attempt - too high
        result = game_logic.check("8")
        assert result == GuessStatus.TOO_HIGH
        assert game_logic.attempts == 2

        # Third attempt - correct
        result = game_logic.check("6")
        assert result == GuessStatus.CORRECT
        assert game_logic.attempts == 3


class TestGuessStatus:
    """Test the GuessStatus enum values."""

    def test_guess_status_values_are_unique(self):
        """Test that all GuessStatus values are unique."""
        statuses = [
            GuessStatus.INVALID_FORMAT,
            GuessStatus.OUT_OF_RANGE,
            GuessStatus.TOO_LOW,
            GuessStatus.TOO_HIGH,
            GuessStatus.CORRECT,
        ]

        # Check that all values are different
        assert len(statuses) == len(set(statuses))

    def test_guess_status_has_expected_members(self):
        """Test that GuessStatus has all expected members."""
        assert hasattr(GuessStatus, "INVALID_FORMAT")
        assert hasattr(GuessStatus, "OUT_OF_RANGE")
        assert hasattr(GuessStatus, "TOO_LOW")
        assert hasattr(GuessStatus, "TOO_HIGH")
        assert hasattr(GuessStatus, "CORRECT")
