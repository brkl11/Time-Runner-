import pygame
import unittest
from unittest.mock import patch, MagicMock
import time
from game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        """Set up a Game instance for testing."""
        self.nickname = "TestPlayer"
        self.game = Game(self.nickname)

    def test_singleton_pattern(self):
        """Test that Game follows the Singleton pattern."""
        game2 = Game(self.nickname)
        self.assertIs(self.game, game2, "Game class is not following the Singleton pattern.")

    def test_save_game_history(self):
        """Test saving game history to a CSV file."""
        with patch("builtins.open", new_callable=MagicMock) as mock_open:
            self.game.save_game_history("win")
            mock_open.assert_called_once_with("game_history.csv", mode="a", newline="")
            # Ensure data is written using csv.writer
            with patch("csv.writer") as mock_csv_writer:
                self.game.save_game_history("win")
                mock_csv_writer().writerow.assert_called_with([self.nickname, unittest.mock.ANY, "win"])

    def test_display_message(self):
        """Test that display_message is called with correct arguments."""
        with patch.object(self.game, "display_message") as mock_display_message:
            self.game.start_time = time.time() - 120  # Simulate 2 minutes of gameplay
            self.game.game_won()
            mock_display_message.assert_called_once_with(
                "You Win!", unittest.mock.ANY, "Press R to Restart or Q to Quit"
            )

    def test_game_won_message(self):
        """Test that the game_won method displays the correct message."""
        with patch.object(self.game, "display_message") as mock_display_message:
            self.game.start_time = time.time() - 120  # Simulate 2 minutes of gameplay
            self.game.game_won()
            mock_display_message.assert_called_once_with(
                "You Win!", unittest.mock.ANY, "Press R to Restart or Q to Quit"
            )

    def test_game_over_message(self):
        """Test that the game_over method displays the correct message."""
        with patch.object(self.game, "display_message") as mock_display_message:
            self.game.start_time = time.time() - 90  # Simulate 1.5 minutes of gameplay
            self.game.game_over()
            mock_display_message.assert_called_once_with(
                "Game Over!", unittest.mock.ANY, "Press R to Restart or Q to Quit"
            )

    @patch.object(Game, "setup", return_value=None)
    def test_restart_game(self, mock_setup):
        """Test that the restart_game method resets the game state."""
        # Simulate game state before restart
        self.game.game_over_state = True
        self.game.enemy_sprites.add(MagicMock())  # Simulate an enemy sprite
        self.game.all_sprites.add(MagicMock())  # Simulate a sprite

        # Call restart_game
        self.game.restart_game()

        # Assertions
        self.assertFalse(self.game.game_over_state, "Game over state was not reset.")
        self.assertEqual(len(self.game.enemy_sprites), 0, "Enemy sprites were not cleared.")
        self.assertEqual(len(self.game.all_sprites), 0, "All sprites were not cleared.")

    def test_arrow_timer(self):
        """Test that the arrow timer correctly handles cooldown."""
        with patch("pygame.time.get_ticks", return_value=1000):
            self.game.shoot_time = 200  # Simulate a shoot time of 200ms
            self.game.arrow_cooldown = 800
            self.game.arrow_timer()
            self.assertTrue(self.game.can_shoot, "Arrow cooldown was not handled correctly.")


if __name__ == "__main__":
    unittest.main()