from typing import List, Tuple
from deserialization import GameData, achievements_list
from checkers.base import did_player_go_north, did_player_go_south, did_player_go_east, did_player_go_west
from math import sqrt
import numpy as np
from scipy.ndimage import label

from typing import Tuple
from math import sqrt

def is_object_near_target(game_data: GameData, placed_object_name: str, target_object_name: str, proximity: int = 1) -> bool:
    """
    Check if an object has been placed near a specific target object.

    Args:
    - game_data (GameData): The game data object containing the player's positions and map information.
    - placed_object_name (str): The name of the object that was placed. Possible values are limited to objects that a player can place.
      Possible values: "CRAFTING_TABLE", "FURNACE", "CHEST", "FOUNTAIN", "ENCHANTMENT_TABLE_FIRE", "ENCHANTMENT_TABLE_ICE", "STONE".
    - target_object_name (str): The name of the target object to check proximity to. The most relevant values include common interactable objects and resources.
      Possible values: "TREE", "WOOD", "STONE", "WATER", "COAL", "IRON", "DIAMOND", "CRAFTING_TABLE", "FURNACE", "CHEST", "FOUNTAIN", 
      "SAPPHIRE", "RUBY", "GRASS", "PATH", "LAVA", "WALL".
    - proximity (int): The maximum distance between the placed object and the target object to be considered "near". Default is 1 block.

    Returns:
    - bool: True if the placed object is near the target object, False otherwise.
    """
    
    # List of objects that a player can place in the game
    placeable_objects = {
        "CRAFTING_TABLE", "FURNACE", "CHEST", "FOUNTAIN", "ENCHANTMENT_TABLE_FIRE", "ENCHANTMENT_TABLE_ICE", "STONE"
    }
    
    if placed_object_name not in placeable_objects:
        raise ValueError(f"The object '{placed_object_name}' cannot be placed by the player.")
    
    # List of relevant target objects in the game
    relevant_target_objects = {
        "TREE", "WOOD", "STONE", "WATER", "COAL", "IRON", "DIAMOND", "CRAFTING_TABLE", "FURNACE", "CHEST", "FOUNTAIN", 
        "SAPPHIRE", "RUBY", "GRASS", "PATH", "LAVA", "WALL"
    }
    
    if target_object_name not in relevant_target_objects:
        raise ValueError(f"The object '{target_object_name}' is not considered a relevant target for this check.")
    
    # Iterate over all game states
    for state in game_data.states:
        map_data = state.map
        
        # Find all coordinates of the target object
        target_coords = np.argwhere(map_data == target_object_name)
        
        # Find all coordinates of the placed object
        placed_object_coords = np.argwhere(map_data == placed_object_name)
        
        # Check if any placed object is within the specified proximity of any target object
        for target_coord in target_coords:
            for placed_coord in placed_object_coords:
                distance = sqrt((target_coord[0] - placed_coord[0]) ** 2 + (target_coord[1] - placed_coord[1]) ** 2)
                if distance <= proximity:
                    return True

    return False

def is_player_within_all_water_sources(game_data: GameData) -> bool:
    """
    Check if the player has been within the bounds of all water clusters across all game states.

    Args:
    - game_data (GameData): The game data object containing the player's positions and map information.

    Returns:
    - bool: True if the player has been within all water clusters at some point, False otherwise.
    """
    water_clusters = find_clusters(game_data)

    # Iterate over all game states
    for state in game_data.states:
        player_position = state.variables.player_position

        # Check if the player has been within any water cluster
        for cluster in water_clusters:
            within_cluster = any(sqrt((x - player_position[0])**2 + (y - player_position[1])**2) <= 1 for (x, y) in cluster)
            if within_cluster:
                water_clusters.remove(cluster)  # Remove the cluster if the player has been within it

        # If all clusters have been covered, return True
        if not water_clusters:
            return True

    # If there are any remaining clusters, return False
    return False

def is_player_within_north_water_sources(game_data: GameData) -> bool:
    """
    Check if the player has been within the bounds of all water clusters in the northern part of the map across all game states.

    Args:
    - game_data (GameData): The game data object containing the player's positions and map information.

    Returns:
    - bool: True if the player has been within all northern water clusters at some point, False otherwise.
    """
    water_clusters = find_clusters(game_data)
    map_height = game_data.states[0].map.shape[0]
    mid_latitude = map_height // 2

    # Filter clusters to only those in the northern part of the map
    north_water_clusters = [
        cluster for cluster in water_clusters if all(y < mid_latitude for (x, y) in cluster)
    ]

    # Iterate over all game states
    for state in game_data.states:
        player_position = state.variables.player_position

        # Check if the player has been within any northern water cluster
        for cluster in north_water_clusters:
            within_cluster = any(sqrt((x - player_position[0])**2 + (y - player_position[1])**2) <= 1 for (x, y) in cluster)
            if within_cluster:
                north_water_clusters.remove(cluster)  # Remove the cluster if the player has been within it

        # If all northern clusters have been covered, return True
        if not north_water_clusters:
            return True

    # If there are any remaining northern clusters, return False
    return False

def is_player_within_south_water_sources(game_data: GameData) -> bool:
    """
    Check if the player has been within the bounds of all water clusters in the southern part of the map across all game states.

    Args:
    - game_data (GameData): The game data object containing the player's positions and map information.

    Returns:
    - bool: True if the player has been within all southern water clusters at some point, False otherwise.
    """
    water_clusters = find_clusters(game_data)
    map_height = game_data.states[0].map.shape[0]
    mid_latitude = map_height // 2

    # Filter clusters to only those in the southern part of the map
    south_water_clusters = [
        cluster for cluster in water_clusters if all(y >= mid_latitude for (x, y) in cluster)
    ]

    # Iterate over all game states
    for state in game_data.states:
        player_position = state.variables.player_position

        # Check if the player has been within any southern water cluster
        for cluster in south_water_clusters:
            within_cluster = any(sqrt((x - player_position[0])**2 + (y - player_position[1])**2) <= 1 for (x, y) in cluster)
            if within_cluster:
                south_water_clusters.remove(cluster)  # Remove the cluster if the player has been within it

        # If all southern clusters have been covered, return True
        if not south_water_clusters:
            return True

    # If there are any remaining southern clusters, return False
    return False


def find_clusters(game_data: GameData, object_index:int=3):
    # Extract the map data
    map_data = game_data.states[0].map
    OBJECT=object_index
    # Identify water blocks (BlockType.WATER.value = 3)
    water_mask = (map_data == OBJECT)

    # Label connected clusters of water blocks
    labeled_array, num_features = label(water_mask)

    # Extract the coordinates of each cluster
    clusters = []
    for cluster_id in range(1, num_features + 1):
        cluster_coords = np.argwhere(labeled_array == cluster_id)
        clusters.append(cluster_coords.tolist())
    return clusters


def if_go_in_direction_until_find_block(game_data: GameData, block_name: str, direction: str) -> bool:
    """
    Check if player goes in the specified direction until finding block_name.
    
    Args:
    - game_data (GameData): The game data object.
    - block_name (str): The block item to be found. Possible items (from PlayerInventory): "GRASS", "WATER", "STONE", "TREE", 
      "WOOD", "PATH", "COAL", "IRON", "DIAMOND", "CRAFTING_TABLE", "FURNACE", "SAND", "LAVA", "PLANT", "RIPE_PLANT", "WALL", 
      "DARKNESS", "WALL_MOSS", "STALAGMITE", "SAPPHIRE", "RUBY", "CHEST", "FOUNTAIN", "FIRE_GRASS", "ICE_GRASS", "GRAVEL", 
      "FIRE_TREE", "ICE_SHRUB", "ENCHANTMENT_TABLE_FIRE", "ENCHANTMENT_TABLE_ICE", "NECROMANCER", "GRAVE", "GRAVE2", 
      "GRAVE3", "NECROMANCER_VULNERABLE"
    - direction (str): The direction in which to move. Possible values: "north", "south", "east", "west".
    
    Returns:
    - bool: True if done, otherwise False.
    """
    direction_map = {
        "north": did_player_go_north,
        "south": did_player_go_south,
        "east": did_player_go_east,
        "west": did_player_go_west
    }

    if direction not in direction_map:
        raise ValueError(f"Invalid direction: {direction}")

    for index, state in enumerate(game_data.states):
        if block_name in state.map.look_around(state.variables.player_position):
            return direction_map[direction](game_data, 0, index)
    
    return False
