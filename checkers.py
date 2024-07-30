from typing import List
from deserialization import GameData, achievements_list

def validate_achievements(player_achievements: List[str]) -> bool:
    return all(achievement in achievements_list for achievement in player_achievements)

def is_variable_increasing(game_data: GameData, variable_name: str, start_index: int, end_index: int) -> bool:
    try:
        start_value = getattr(game_data.states[start_index].variables, variable_name)
        end_value = getattr(game_data.states[end_index].variables, variable_name)
        return start_value < end_value
    except AttributeError:
        raise ValueError(f"Variable '{variable_name}' does not exist in PlayerVariables.")
    except IndexError:
        raise ValueError("Index out of range. Ensure the indices are within the correct range of states.")

def is_variable_decreasing(game_data: GameData, variable_name: str, start_index: int, end_index: int) -> bool:
    try:
        start_value = getattr(game_data.states[start_index].variables, variable_name)
        end_value = getattr(game_data.states[end_index].variables, variable_name)
        return start_value > end_value
    except AttributeError:
        raise ValueError(f"Variable '{variable_name}' does not exist in PlayerVariables.")
    except IndexError:
        raise ValueError("Index out of range. Ensure the indices are within the correct range of states.")

def has_item_in_inventory(game_data: GameData, state_index: int, item_name: str) -> bool:
    try:
        inventory = game_data.states[state_index].inventory
        return getattr(inventory, item_name, 0) > 0
    except IndexError:
        raise ValueError("State index out of range. Ensure the index is within the correct range of states.")
    except AttributeError:
        raise ValueError(f"Item '{item_name}' does not exist in PlayerInventory.")

def find_item_in_inventory(game_data: GameData, item_name: str) -> List[int]:
    states_with_item = []
    for i, state in enumerate(game_data.states):
        inventory = state.inventory
        if getattr(inventory, item_name, 0) > 0:
            states_with_item.append(i)
    return states_with_item[0]

def is_achievement_obtained(game_data: GameData, achievement_name: str, start_index: int, end_index: int = None) -> bool:
    end_index = end_index if end_index is not None else start_index
    try:
        for i in range(start_index, end_index + 1):
            if achievement_name in game_data.states[i].achievements.achievements:
                return True
        return False
    except IndexError:
        raise ValueError("Index out of range. Ensure the indices are within the correct range of states.")

def find_achievement_state(game_data: GameData, achievement_name: str) -> List[int]:
    states_with_achievement = [-1]
    for i, state in enumerate(game_data.states):
        if achievement_name in state.achievements.achievements:
            states_with_achievement.append(i)
    return states_with_achievement[1]

def did_player_go_north(game_data, start_index, end_index):
    """
    Check if the player has moved north between two game states.

    Args:
    - game_data (GameData): The game data object.
    - start_index (int): The index of the starting game state.
    - end_index (int): The index of the ending game state.

    Returns:
    - bool: True if the player moved north, otherwise False.
    """
    if not (0 <= start_index < len(game_data.states) and 0 <= end_index < len(game_data.states)):
        raise IndexError("start_index or end_index is out of the valid range of game states.")
    
    start_state = game_data.states[start_index]
    end_state = game_data.states[end_index]
    
    # Assuming we have a 'position' attribute with 'x' and 'y' coordinates in PlayerState
    start_position = start_state.variables.player_position
    end_position = end_state.variables.player_position
    
    return end_position[1] > start_position[1]

def did_player_go_south(game_data, start_index, end_index):
    """
    Check if the player has moved south between two game states.

    Args:
    - game_data (GameData): The game data object.
    - start_index (int): The index of the starting game state.
    - end_index (int): The index of the ending game state.

    Returns:
    - bool: True if the player moved south, otherwise False.
    """
    if not (0 <= start_index < len(game_data.states) and 0 <= end_index < len(game_data.states)):
        raise IndexError("start_index or end_index is out of the valid range of game states.")
    
    start_state = game_data.states[start_index]
    end_state = game_data.states[end_index]
    
    # Assuming we have a 'position' attribute with 'x' and 'y' coordinates in PlayerState
    start_position = start_state.variables.player_position
    end_position = end_state.variables.player_position
    
    return end_position[1] < start_position[1]



def did_player_go_west(game_data, start_index, end_index):
    """
    Check if the player has moved west between two game states.

    Args:
    - game_data (GameData): The game data object.
    - start_index (int): The index of the starting game state.
    - end_index (int): The index of the ending game state.

    Returns:
    - bool: True if the player moved west, otherwise False.
    """
    if not (0 <= start_index < len(game_data.states) and 0 <= end_index < len(game_data.states)):
        raise IndexError("start_index or end_index is out of the valid range of game states.")
    
    start_state = game_data.states[start_index]
    end_state = game_data.states[end_index]
    
    # Assuming we have a 'position' attribute with 'x' and 'y' coordinates in PlayerState
    start_position = start_state.variables.player_position
    end_position = end_state.variables.player_position
    
    return end_position[0] < start_position[0]

def did_player_go_east(game_data, start_index, end_index):
    """
    Check if the player has moved east between two game states.

    Args:
    - game_data (GameData): The game data object.
    - start_index (int): The index of the starting game state.
    - end_index (int): The index of the ending game state.

    Returns:
    - bool: True if the player moved east, otherwise False.
    """
    if not (0 <= start_index < len(game_data.states) and 0 <= end_index < len(game_data.states)):
        raise IndexError("start_index or end_index is out of the valid range of game states.")
    
    start_state = game_data.states[start_index]
    end_state = game_data.states[end_index]
    
    # Assuming we have a 'position' attribute with 'x' and 'y' coordinates in PlayerState
    start_position = start_state.variables.player_position
    end_position = end_state.variables.player_position
    
    return end_position[0] > start_position[0]
