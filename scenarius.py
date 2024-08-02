from typing import List, Tuple
from deserialization import GameData, achievements_list
from checkers.base import is_variable_increasing, check_achievement_inventory_radius, was_item_placed
from math import sqrt



def was_item_collected_after_another(game_data: GameData, first_item: str, second_item: str) -> bool:
    ### WRONG!!!
    """
    Check if `second_item` was collected after `first_item`.
    
    Args:
    - game_data (GameData): The game data object.
    - first_item (str): The first item to check in the inventory. Possible items (from PlayerInventory): wood, stonr, coal, iron, pickaxe, sword, armour, potions
    - second_item (str): The second item to check in the inventory. Possible items (from PlayerInventory): wood, stonr, coal, iron, pickaxe, sword, armour, potions

    Returns:
    - bool: True if `second_item` was collected after `first_item`, otherwise False.
    """
    first_item_collected = False
    first_item_index = None

    for index, state in enumerate(game_data.states):
        inventory = state.inventory

        if not first_item_collected:
            if getattr(inventory, first_item, 0) > 0:
                first_item_collected = True
                first_item_index = index
        elif getattr(inventory, second_item, 0) > 0 and first_item_index is not None:
            return index > first_item_index

    return False


def did_placing_item_increase_variable(game_data: GameData, item: str, variable_name: str) -> bool:
    """
    Check if placing `item` caused an increase in `variable_name`.

    Args:
    - game_data (GameData): The game data object.
    - item (str): The inventory item to check; Possible items: table, stone, furnace, plant, torch.
    - variable_name (str): The variable to check for an increase.
    
    Returns:
    - bool: True if placing `item` caused an increase in `variable_name`, otherwise False.
    """
    try:
        # Identify the state where the item was placed
        place_index = was_item_placed(game_data, item, 0, len(game_data.states), verbose=True)
        if not place_index:  # If item was not placed, return False
            return False
        
        # Check if the variable increased after the item was placed
        return is_variable_increasing(game_data, variable_name, place_index[0], place_index[0] + 1)
    except ValueError as e:
        print(f"Error: {e}")
        return False


def was_item_placed_near_another(game_data: GameData, first_item: str, second_item: str) -> bool:
    """
    Check if `second_item` was placed near `first_item`.

    Args:
    - game_data (GameData): The game data object.
    - first_item (str): The first item to check in the inventory. Possible items: table, stone, furnace, plant, torch.
    - second_item (str): The second item to check in the inventory. Possible items: table, stone, furnace, plant, torch.

    Returns:
    - bool: True if `second_item` was placed near `first_item`, otherwise False.
    """
    try:
        # Identify the state where the first item was placed
        first_item_placement_index = was_item_placed(game_data, first_item, 0, len(game_data.states), verbose=True)
        if not first_item_placement_index:  # If the first item was not placed, return False
            return False
        
        # Check if the second item was placed near the first item
        for index in first_item_placement_index:
            # Assuming `check_achievement_inventory_radius` function can be used to check proximity
            if check_achievement_inventory_radius(game_data, game_data.states[index].variables.player_position, 1, item_name=second_item):
                return True
        return False
    except ValueError as e:
        print(f"Error: {e}")
        return False


def is_item_in_closed_contour(game_data: GameData, first_item: str, second_item: str) -> bool:
    """
    Check if `first_item` is placed within a closed contour formed by `second_item`.

    Args:
    - game_data (GameData): The game data object.
    - first_item (str): The first item to check in the inventory. Possible items: table, stone, furnace, plant, torch.
    - second_item (str): The second item to check in the inventory. Possible items: table, stone, furnace, plant, torch.

    Returns:
    - bool: True if `first_item` is within a closed contour formed by `second_item`, otherwise False.
    """
    try:
        # Identify the state where the first item was placed
        first_item_placement_index = was_item_placed(game_data, first_item, 0, len(game_data.states), verbose=True)
        if not first_item_placement_index:  # If the first item was not placed, return False
            return False

        # Check if the first item is within a closed contour formed by the second item
        for index in first_item_placement_index:
            first_item_position = game_data.states[index].variables.player_position

            # Assuming we have a function that checks if a point is within a polygon
            if is_point_within_polygon(first_item_position, game_data, second_item):
                return True
        return False
    except ValueError as e:
        print(f"Error: {e}")
        return False

def is_point_within_polygon(point: Tuple[int, int], game_data: GameData, item_name: str) -> bool:
    """
    Check if a given point is within a polygon formed by the positions of `item_name`.

    Args:
    - point (Tuple[int, int]): The (x, y) coordinates of the point.
    - game_data (GameData): The game data object.
    - item_name (str): The name of the item to form the polygon.

    Returns:
    - bool: True if the point is within the polygon, otherwise False.
    """
    # Find all states where the item is placed
    item_positions = []
    for index, state in enumerate(game_data.states):
        if getattr(state.inventory, item_name, 0) > 0:
            item_positions.append(state.variables.player_position)

    if len(item_positions) < 3:
        return False  # A polygon requires at least 3 points

    # Check if the point is within the polygon formed by item_positions
    return point_in_polygon(point, item_positions)

def point_in_polygon(point: Tuple[int, int], polygon: List[Tuple[int, int]]) -> bool:
    """
    Determine if a point is inside a given polygon or not.

    Args:
    - point (Tuple[int, int]): The (x, y) coordinates of the point.
    - polygon (List[Tuple[int, int]]): The list of (x, y) coordinates forming the polygon.

    Returns:
    - bool: True if the point is inside the polygon, otherwise False.
    """
    x, y = point
    inside = False

    n = len(polygon)
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

if __name__ == "__main__":
    pass

