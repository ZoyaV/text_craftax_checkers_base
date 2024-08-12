from typing import List, Tuple
from deserialization import GameData
import numpy as np

def is_cross_formed(game_data: GameData, block_name: str) -> bool:
    """
    Check if a cross is formed using the specified block.

    Args:
    - game_data (GameData): The game data object containing the player's positions and map information.
    - block_name (str): The name of the block to check. Possible items (from PlayerInventory): "CRAFTING_TABLE", "FURNACE", "CHEST", "FOUNTAIN", "ENCHANTMENT_TABLE_FIRE", "ENCHANTMENT_TABLE_ICE", "PLANT"

    Returns:
    - bool: True if a cross is formed using the block, otherwise False.
    """
    
    cross_offsets = [
        (0, 0),  # center
        (-1, 0), # left
        (1, 0),  # right
        (0, -1), # up
        (0, 1),  # down
    ]
    
    # Iterate over all game states
    for state in game_data.states:
        map_data = state.map

        # Find all coordinates of the specified block
        block_coords = np.argwhere(map_data == block_name)

        for coord in block_coords:
            if all(tuple(coord + np.array(offset)) in block_coords for offset in cross_offsets):
                return True
    
    return False

def is_square_formed(game_data: GameData, block_name: str, size: int = 2) -> bool:
    """
    Check if a square of a given size is formed using the specified block.

    Args:
    - game_data (GameData): The game data object containing the player's positions and map information.
    - block_name (str): The name of the block to check. Possible items (from PlayerInventory): "CRAFTING_TABLE", "FURNACE", "CHEST", "FOUNTAIN", "ENCHANTMENT_TABLE_FIRE", "ENCHANTMENT_TABLE_ICE", "PLANT"
    - size (int): The size of the square to check for. Default is 2 (2x2 square).

    Returns:
    - bool: True if a square of the specified size is formed using the block, otherwise False.
    """
    
    # Generate all offset pairs for a square of the given size
    square_offsets = [(i, j) for i in range(size) for j in range(size)]
    
    # Iterate over all game states
    for state in game_data.states:
        map_data = state.map

        # Find all coordinates of the specified block
        block_coords = np.argwhere(map_data == block_name)

        for coord in block_coords:
            if all(tuple(coord + np.array(offset)) in block_coords for offset in square_offsets):
                return True
    
    return False

from typing import List, Tuple
from deserialization import GameData
import numpy as np

def is_line_formed(game_data: GameData, block_name: str, length: int, check_diagonal: bool = False) -> bool:
    """
    Check if a line of a given length is formed using the specified block.

    Args:
    - game_data (GameData): The game data object containing the player's positions and map information.
    - block_name (str): The name of the block to check. Possible items (from PlayerInventory): "CRAFTING_TABLE", "FURNACE", "CHEST", "FOUNTAIN", "ENCHANTMENT_TABLE_FIRE", "ENCHANTMENT_TABLE_ICE", "PLANT"
    - length (int): The length of the line to check for.
    - check_diagonal (bool): If True, checks for diagonal lines as well. Default is False.

    Returns:
    - bool: True if a line of the specified length is formed using the block, otherwise False.
    """

    directions = [
        (1, 0),  # Horizontal
        (0, 1),  # Vertical
    ]
    
    if check_diagonal:
        directions.extend([(1, 1),  # Diagonal (top-left to bottom-right)
                           (1, -1)])  # Diagonal (top-right to bottom-left)

    # Iterate over all game states
    for state in game_data.states:
        map_data = state.map

        # Find all coordinates of the specified block
        block_coords = np.argwhere(map_data == block_name)

        for coord in block_coords:
            for direction in directions:
                line_coords = [tuple(coord + np.array(direction) * i) for i in range(length)]
                if all(tuple(c) in block_coords for c in line_coords):
                    return True
    
    return False
