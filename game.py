import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('fonts/arial.ttf', 25)

class Direction(Enum):
    """Enumeration class for representing directions."""
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

BLOCK_SIZE = 20
SPEED = 60
size = 600
nb_cell = 12
cell_size = int(size / nb_cell)

class AIvsEnni:
    """Class representing the AIvsEnni."""
    
    def __init__(self, w=480, h=480):
        """
        Initialize the game environment.

        Parameters:
            w (int): Width of the game window.
            h (int): Height of the game window.
        """
        self.w = w
        self.h = h
        self.grid = [[0] * nb_cell for _ in range(nb_cell)]
        self.blocks = [[2, 1], [2, 2], [2, 3], [2, 4],
                       [3, 2], [3, 3], [3, 4],
                       [4, 2], [4, 3], [4, 4],
                       [7, 1], [7, 2], [7, 3], [7, 4],
                       [8, 2], [8, 3], [8, 4],
                       [9, 2], [9, 3],
                       [2, 8], [2, 9],
                       [3, 7], [3, 8], [3, 9],
                       [4, 7], [4, 8], [4, 9], [4, 10],
                       [7, 7], [7, 8], [7, 9],
                       [8, 7], [8, 8], [8, 9], [8, 10],
                       [9, 7], [9, 8], [9, 9], [9, 10],
                       [10, 7]]

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('AI VS Ennemi')
        self.clock = pygame.time.Clock()
        self.reset()

        self.Background = pygame.display.set_mode((size, size))  # Set the background with size
        self.Background.fill(WHITE)  # Fill the background with white color
        self._initialize_grid_and_blocks()  # Initialize the grid and blocks

        # Initialize memory mechanism
        self.moves_history = []
        self.memory_size = 100  # Maximum number of moves to remember
        self.memory = []

    def _initialize_grid_and_blocks(self):
        """Initialize the grid and blocks."""
        for i in range(0, size, cell_size):
            pygame.draw.line(self.Background, BLACK, (0, i), (size, i))  # Vertical lines
            pygame.draw.line(self.Background, BLACK, (i, 0), (i, size))  # Horizontal lines
        for row, col in self.blocks:
            pygame.draw.rect(self.Background, ORANGE, (row * cell_size, col * cell_size, cell_size, cell_size))
        pygame.display.update()

    def reset(self):
        """Reset the game state."""
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(cell_size * (self.w // (2 * cell_size)), cell_size * (self.h // (2 * cell_size)))
        self.aigame = [self.head]

        self.score = 0
        self.ennemi = None
        self._place_ennemi()
        self.frame_iteration = 0

        # Reset memory
        self.moves_history = []
        self.memory = []

    def _place_ennemi(self):
        """Place ennemi randomly on the grid."""
        x = random.randint(0, (self.w - cell_size)//cell_size)*cell_size
        y = random.randint(0, (self.h - cell_size)//cell_size)*cell_size

        while [x // cell_size, y // cell_size] in self.blocks:
            x = random.randint(0, (self.w - cell_size)//cell_size)*cell_size
            y = random.randint(0, (self.h - cell_size)//cell_size)*cell_size

        self.ennemi = Point(x, y)

    def play_step(self, action):
        """
        Play one step of the game.

        Parameters:
            action (list): Action to take.

        Returns:
            tuple: A tuple containing the reward, game over flag, and current score.
        """
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self._move(action)
        self.aigame.insert(0, self.head)

        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.aigame):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.ennemi:
            self.score += 1
            reward = 10
            self._place_ennemi()
        else:
            self.aigame.pop()

        self._update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score

    def is_collision(self, pt=None):
        """
        Check if there is a collision in the game.

        Parameters:
            pt (Point): The point to check for collision.

        Returns:
            bool: True if collision is detected, False otherwise.
        """
        if pt is None:
            pt = self.head

        # Check if out of bounds
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True

        # Check if it hits itself
        if pt in self.aigame[1:]:
            return True

        # Check if it hits any block
        if [pt.x // cell_size, pt.y // cell_size] in self.blocks:
            return True

        return False

    def _update_ui(self):
        """Update the game user interface."""
        self.display.fill(WHITE)

        # Draw the grid
        for i in range(0, size, cell_size):
            pygame.draw.line(self.display, BLACK, (0, i), (size, i))  # Vertical lines
            pygame.draw.line(self.display, BLACK, (i, 0), (i, size))  # Horizontal lines

        # Draw the blocks
        for row, col in self.blocks:
            pygame.draw.rect(self.display, ORANGE, (row * cell_size, col * cell_size, cell_size, cell_size))

        # Draw the aigame
        for pt in self.aigame:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, cell_size, cell_size))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, cell_size - 8, cell_size - 8))

        # Draw the ennemi
        pygame.draw.rect(self.display, RED, pygame.Rect(self.ennemi.x, self.ennemi.y, cell_size, cell_size))

        text = font.render("Score: " + str(self.score), True, BLACK)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        """
        Move the s based on the action.

        Parameters:
            action (list): Action to take.
        """
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # Right turn relative to current direction
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # Left turn relative to current direction

        # Prevent reversing
        if new_dir == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = new_dir
        elif new_dir == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = new_dir
        elif new_dir == Direction.UP and self.direction != Direction.DOWN:
            self.direction = new_dir
        elif new_dir == Direction.DOWN and self.direction != Direction.UP:
            self.direction = new_dir

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += cell_size
        elif self.direction == Direction.LEFT:
            x -= cell_size
        elif self.direction == Direction.DOWN:
            y += cell_size
        elif self.direction == Direction.UP:
            y -= cell_size

        self.head = Point(x, y)

        # Update moves history
        self.moves_history.append(self.head)

        # Limit moves history to prevent excessive memory usage
        if len(self.moves_history) > self.memory_size:
            self.moves_history.pop(0)

        # Update memory with current position
        self.memory.append(self.head)

        # Trim memory to the specified size
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)

    def _is_repetitive_move(self):
        """
        Check if the last few moves are repetitive.

        Returns:
            bool: True if the last few moves are repetitive, False otherwise.
        """
        # Check if the last few moves are repetitive
        if len(self.moves_history) < self.memory_size:
            return False
        last_moves = self.moves_history[-self.memory_size:]
        return len(set(last_moves)) == 1

    def _is_repetitive_position(self):
        """
        Check if the AI is stuck in the same position.

        Returns:
            bool: True if the AI is stuck in the same position, False otherwise.
        """
        # Check if the AI is stuck in the same position
        if len(self.memory) < self.memory_size:
            return False
        last_positions = [move for move in self.memory[-self.memory_size:]]
        return len(set(last_positions)) == 1


if __name__ == "__main__":
    game = AIvsEnni()
    game.reset()

    # Main loop
    while True:
        # AI action
        action = [0, 0, 1]  # Change this according to your AI logic
        reward, game_over, score = game.play_step(action)

        if game_over:
            game.reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
