import pytest
from hangman import Hangman
import time

def test_initialization_basic():
    game = Hangman(level='basic')
    assert game.puzzle != ''  # Puzzle should be a non-empty string
    assert ''.join(game.masked) == '_' * len(game.puzzle)  # Convert list to string for comparison
    assert game.lives == 6  # Initial lives

def test_initialization_intermediate():
    game = Hangman(level='intermediate')
    assert ' ' in game.puzzle  # Phrase has spaces
    assert ' ' in ''.join(game.masked)  # Spaces preserved in mask
    assert game.lives == 6  # Initial lives

def test_correct_guess():
    game = Hangman(level='basic')
    game.puzzle = 'python'  # Mock for determinism
    game.masked = list('______')  # Use list
    updated = game.guess('p')
    assert updated == 'p_____'
    assert game.lives == 6  # No life deduction

def test_incorrect_guess():
    game = Hangman(level='basic')
    game.puzzle = 'python'  # Mock for determinism
    game.masked = list('______')  # Use list
    updated = game.guess('z')
    assert updated == '______'
    assert game.lives == 6  # No life deduction (moved to play_game)

def test_multiple_occurrences():
    game = Hangman(level='basic')
    game.puzzle = 'testing'  # Mock for determinism
    game.masked = list('_______')  # Use list
    updated = game.guess('t')
    assert updated == 't__t___'
    assert game.lives == 6  # No life deduction

def test_is_won():
    game = Hangman(level='basic')
    game.puzzle = 'test'
    game.masked = list('test')  # Use list
    assert game.is_won() == True

    game.masked = list('t_st')  # Use list
    assert game.is_won() == False

def test_is_lost():
    game = Hangman(level='basic')
    game.lives = 0
    assert game.is_lost() == True

    game.lives = 1
    assert game.is_lost() == False

def test_invalid_input_first_attempt():
    game = Hangman(level='basic')
    game.puzzle = 'python'
    game.masked = list('______')  # Use list
    game.guess('abc')  # Simulate invalid input
    assert game.lives == 6  # No life deducted on first invalid input (in play_game)

def test_invalid_input_subsequent_attempt():
    game = Hangman(level='basic')
    game.puzzle = 'python'
    game.masked = list('______')  # Use list
    game.guess('abc')  # First invalid input
    game.guess('123')  # Second invalid input
    assert game.lives == 6  # No life deducted (in play_game)

def test_score_calculation():
    game = Hangman(level='basic')
    game.puzzle = 'test'
    game.masked = list('____')  # Use list
    game.lives = 5  # Simulate some lives used
    game.start_time = time.time() - 10  # Simulate 10 seconds elapsed
    score = game.get_score()
    assert score == (5 * 100) - 10  # 500 - 10 = 490
    # Note: Exact time may vary slightly due to execution, so this is approximate