
from typing import List, Tuple
from deserialization import GameData, achievements_list
from math import sqrt

def is_table_placed(game_data: GameData, verbose: bool = False):
    """
    Check if the table was placed in the game.

    Args:
    - game_data (GameData): The game data object.
    - verbose (bool): If True, return the state index where the condition was met.

    Returns:
    - bool or int: True if the table was placed, otherwise False.
                   If verbose is True, return the state index instead of True.
    """
    # Loop through game states to check if the table was placed
    for index, state in enumerate(game_data.states):
        # Check if the action to place table was pressed
        if 'place_table' in state.actions:
            # Check if there were enough resources (at least 2 wood)
            if state.inventory.get('wood', 0) >= 2:
                return index if verbose else True
    return -1 if verbose else False

def is_wood_pickaxe_made(game_data: GameData, verbose: bool = False):
    """
    Check if the wood pickaxe was made in the game.

    Args:
    - game_data (GameData): The game data object.
    - verbose (bool): If True, return the state index where the condition was met.

    Returns:
    - bool or int: True if the wood pickaxe was made, otherwise False.
                   If verbose is True, return the state index instead of True.
    """
    table_index = is_table_placed(game_data, verbose=True)
    
    if table_index == -1:
        return -1 if verbose else False
    
    # Loop through game states starting from table placement to check if the wood pickaxe was made
    for index in range(table_index, len(game_data.states)):
        state = game_data.states[index]
        # Check if the action to make wood pickaxe was pressed
        if 'make_wood_pickaxe' in state.actions:
            return index if verbose else True

    return -1 if verbose else False
