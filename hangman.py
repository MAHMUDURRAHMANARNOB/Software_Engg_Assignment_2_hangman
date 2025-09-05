import random
import sys
import select
import time

class Hangman:
    def __init__(self, level='basic'):
        self.dictionary_basic = ['python', 'hangman', 'testing', 'development', 'challenge',    'function', 'variable', 'iteration', 'condition', 'exception', 'algorithm', 'parameter', 'argument', 'string', 'integer', 'boolean', 'list', 'dictionary', 'tuple', 'set']
        self.dictionary_intermediate = ['test driven development', 'unit testing tool', 'continuous integration', 'object oriented programming', 'asynchronous programming', 'dependency injection', 'design patterns', 'software architecture', 'version control system', 'code refactoring']
        if level == 'basic':
            self.puzzle = random.choice(self.dictionary_basic)
        else:
            self.puzzle = random.choice(self.dictionary_intermediate)
        self.masked = list('_' if c.isalpha() else c for c in self.puzzle)  # List for easier manipulation
        self.lives = 6
        self.guessed = set()  # Track guessed letters to avoid duplicates
        self.start_time = time.time()  # Record start time

    def guess(self, letter):
        letter = letter.lower()  # Case-insensitive guessing
        if letter in self.guessed:
            return ''.join(self.masked)  # No change if already guessed
        self.guessed.add(letter)
        if letter in self.puzzle.lower():
            for i in range(len(self.puzzle)):
                if self.puzzle[i].lower() == letter.lower():
                    self.masked[i] = self.puzzle[i]
        # Do not deduct life here; handle in play_game
        return ''.join(self.masked)

    def is_won(self):
        return ''.join(self.masked) == self.puzzle

    def is_lost(self):
        return self.lives <= 0

    def get_score(self):
        elapsed_time = time.time() - self.start_time
        # Score = (lives remaining * 100) - (elapsed time in seconds)
        return max(0, (self.lives * 100) - int(elapsed_time))

def load_high_score():
    try:
        with open('highscore.txt', 'r') as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    with open('highscore.txt', 'w') as file:
        file.write(str(score))

def play_game():
    print("\n=== Welcome to Hangman! ===")
    print("Guess the word or phrase one letter at a time.")
    print("You have 15 seconds per guess. Type 'quit' to exit.")
    print("-------------------\n")
    level = input("Choose level (basic/intermediate): ").strip().lower()
    game = Hangman(level)
    high_score = load_high_score()
    print("\n=== Hangman Game ===")
    print(f"Puzzle: {''.join(game.masked)}")
    print(f"Lives remaining: {game.lives}")
    print(f"High score: {high_score} points")
    print("-------------------\n")

    while not game.is_won() and not game.is_lost():
        print("You have 15 seconds to guess...")
        for remaining in range(15, 0, -1):
            print(f"Time left: {remaining} seconds", end='\r\n')
            i, _, _ = select.select([sys.stdin], [], [], 1)
            if i:
                guess = sys.stdin.readline().strip().lower()
                print()  # Move to new line after input
                if guess == 'quit':
                    print(f"Game ended. The answer was: {game.puzzle}")
                    return
                elif len(guess) != 1 or not guess.isalpha():
                    if game.lives > 1:  # Allow one free invalid input
                        print("Invalid input. Please enter a single letter or 'quit'.")
                        print("-------------------\n")
                    else:
                        game.lives -= 1  # Deduct life after free attempt
                        print("Invalid input. Life deducted. Please enter a single letter or 'quit'.")
                        print("-------------------\n")
                else:
                    updated = game.guess(guess)
                    if guess not in game.puzzle.lower():  # Wrong guess deducts life
                        game.lives -= 1
                    print(f"Updated puzzle: {updated}")
                    print(f"Guessed letters: {', '.join(sorted(game.guessed))}")
                    print(f"Lives remaining: {game.lives}")
                    print("-------------------\n")
                break
            time.sleep(1)
        else:
            print("\nTime's up!")
            game.lives -= 1
            print(f"Lives remaining: {game.lives}")
            print("-------------------\n")

    if game.is_won():
        score = game.get_score()
        high_score = load_high_score()
        if score > high_score:
            save_high_score(score)
            print("=== Congratulations! You won! ===")
            print(f"Your score: {score} points")
            print(f"New high score! {score} points")
        else:
            print("=== Congratulations! You won! ===")
            print(f"Your score: {score} points")
            print(f"High score remains: {high_score} points")
    elif game.is_lost():
        print("=== Game Over! You lost. Answer was:", game.puzzle, "===")

if __name__ == "__main__":
    play_game()