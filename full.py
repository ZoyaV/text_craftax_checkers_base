import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Tuple
@dataclass
class Inventory:
    wood: int
    stone: int
    coal: int
    iron: int = 0
    pickaxe: int = 0
    sword: int = 0
    armour: List[int] = field(default_factory=lambda: [0, 0, 0, 0])
    potions: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0, 0])

@dataclass
class Variables:
    player_position: Dict[int, Tuple[int, int]]
    player_level: Dict[int, int]
    player_direction: Dict[int, int]
    player_health: Dict[int, float]
    player_food: Dict[int, int]
    player_drink: Dict[int, int]
    player_energy: Dict[int, int]
    player_mana: Dict[int, int]
    is_sleeping: Dict[int, bool]
    is_resting: Dict[int, bool]
    player_recover: Dict[int, float]
    player_hunger: Dict[int, float]
    player_thirst: Dict[int, float]
    player_fatigue: Dict[int, float]
    player_recover_mana: Dict[int, float]
    player_xp: Dict[int, int]
    player_dexterity: Dict[int, int]
    player_strength: Dict[int, int]
    player_intelligence: Dict[int, int]
    learned_spells: Dict[int, List[bool]]
    sword_enchantment: Dict[int, int]
    bow_enchantment: Dict[int, int]
    boss_progress: Dict[int, int]
    boss_timesteps_to_spawn_this_round: Dict[int, int]
    light_level: Dict[int, float]
    state_rng: Dict[int, Tuple[int, int]]
    timestep: Dict[int, int]

@dataclass
class Achievement:
    COLLECT_WOOD: bool = False
    PLACE_TABLE: bool = False
    EAT_COW: bool = False
    COLLECT_SAPLING: bool = False
    COLLECT_DRINK: bool = False
    MAKE_WOOD_PICKAXE: bool = False
    MAKE_WOOD_SWORD: bool = False
    PLACE_PLANT: bool = False
    DEFEAT_ZOMBIE: bool = False
    COLLECT_STONE: bool = False
    PLACE_STONE: bool = False
    EAT_PLANT: bool = False
    DEFEAT_SKELETON: bool = False
    MAKE_STONE_PICKAXE: bool = False
    MAKE_STONE_SWORD: bool = False
    WAKE_UP: bool = False
    PLACE_FURNACE: bool = False
    COLLECT_COAL: bool = False
    COLLECT_IRON: bool = False
    COLLECT_DIAMOND: bool = False
    MAKE_IRON_PICKAXE: bool = False
    MAKE_IRON_SWORD: bool = False
    MAKE_ARROW: bool = False
    MAKE_TORCH: bool = False
    PLACE_TORCH: bool = False
    COLLECT_SAPPHIRE: bool = False
    COLLECT_RUBY: bool = False
    MAKE_DIAMOND_PICKAXE: bool = False
    MAKE_DIAMOND_SWORD: bool = False
    MAKE_IRON_ARMOUR: bool = False
    MAKE_DIAMOND_ARMOUR: bool = False
    ENTER_GNOMISH_MINES: bool = False
    ENTER_DUNGEON: bool = False
    ENTER_SEWERS: bool = False
    ENTER_VAULT: bool = False
    ENTER_TROLL_MINES: bool = False
    ENTER_FIRE_REALM: bool = False
    ENTER_ICE_REALM: bool = False
    ENTER_GRAVEYARD: bool = False
    DEFEAT_GNOME_WARRIOR: bool = False
    DEFEAT_GNOME_ARCHER: bool = False
    DEFEAT_ORC_SOLIDER: bool = False
    DEFEAT_ORC_MAGE: bool = False
    DEFEAT_LIZARD: bool = False
    DEFEAT_KOBOLD: bool = False
    DEFEAT_KNIGHT: bool = False
    DEFEAT_ARCHER: bool = False
    DEFEAT_TROLL: bool = False
    DEFEAT_DEEP_THING: bool = False
    DEFEAT_PIGMAN: bool = False
    DEFEAT_FIRE_ELEMENTAL: bool = False
    DEFEAT_FROST_TROLL: bool = False
    DEFEAT_ICE_ELEMENTAL: bool = False
    DAMAGE_NECROMANCER: bool = False
    DEFEAT_NECROMANCER: bool = False
    EAT_BAT: bool = False
    EAT_SNAIL: bool = False
    FIND_BOW: bool = False
    FIRE_BOW: bool = False
    LEARN_FIREBALL: bool = False
    CAST_FIREBALL: bool = False
    LEARN_ICEBALL: bool = False
    CAST_ICEBALL: bool = False
    OPEN_CHEST: bool = False
    DRINK_POTION: bool = False
    ENCHANT_SWORD: bool = False
    ENCHANT_ARMOUR: bool = False

@dataclass
class Data:
    variables: Variables
    achievements: Dict[int, Achievement]
    inventory: Dict[int, Inventory]

def from_dict(data_class, data: Dict[str, Any]):
    """Recursively converts a nested dictionary to a dataclass"""
    if hasattr(data_class, '__dataclass_fields__'):
        fieldtypes = {f.name: f.type for f in data_class.__dataclass_fields__.values()}
        return data_class(**{f: from_dict(fieldtypes[f], data[f]) if f in data else None for f in data_class.__dataclass_fields__.keys()})
    elif isinstance(data, dict):
        return {k: from_dict(data_class.__args__[1], v) for k, v in data.items()}
    elif isinstance(data, list):
        return [from_dict(data_class.__args__[0], item) for item in data]
    else:
        return data
        
def predominant_direction(coords_dict):
    start_i = min(list(coords_dict.keys()))
    end_i = max(list(coords_dict.keys()))
    if not coords_dict or len(coords_dict) < 2:
        return "insufficient data"

    start_x, start_y = coords_dict[start_i]
    end_x, end_y = coords_dict[end_i]

    dx = end_x - start_x
    dy = end_y - start_y

    if dx == 0 and dy == 0:
        return "no movement"

    if abs(dx) > abs(dy):
        if dx > 0:
            if dy > 0:
                return "northeast"
            elif dy < 0:
                return "southeast"
            else:
                return "east"
        else:
            if dy > 0:
                return "northwest"
            elif dy < 0:
                return "southwest"
            else:
                return "west"
    else:
        if dy > 0:
            if dx > 0:
                return "northeast"
            elif dx < 0:
                return "northwest"
            else:
                return "north"
        else:
            if dx > 0:
                return "southeast"
            elif dx < 0:
                return "southwest"
            else:
                return "south"

def is_predominantly_ascending(values_dict):
    start_i = min(list(values_dict.keys()))
    end_i = max(list(values_dict.keys()))
    if not values_dict or len(values_dict) < 2:
        return False  # Not enough data to evaluate

    return values_dict[end_i] > values_dict[start_i]

def is_predominantly_descending(values_dict):
    start_i = min(list(values_dict.keys()))
    end_i = max(list(values_dict.keys()))
    if not values_dict or len(values_dict) < 2:
        return False  # Not enough data to evaluate

    return values_dict[end_i] < values_dict[start_i]

def contains_object(lst, obj):
    return obj in lst

def find_object_states(dict_of_lsts, obj):
    for state_index in dict_of_lsts.keys():
        if obj in dict_of_lsts[state_index]:
            return state_index
    return -1

if __name__ == "__main__":
    # Load JSON data from file
    with open('/mnt/data/compressed_changes.json') as file:
        json_data = json.load(file)
    
    # Deserialize JSON to Data class
    data = from_dict(Data, json_data)
    
    # Example usage of the check functions
    state_id = 1  # Example state index
    print(f"Predominant direction: {predominant_direction(data.variables.player_position)}")
    print(f"Health predominantly ascending: {is_predominantly_ascending(data.variables.player_health)}")
    print(f"Health predominantly descending: {is_predominantly_descending(data.variables.player_health)}")

    
    print(f"Contains wood in inventory: {contains_object(data.inventory[state_id].__dict__, 'wood')}")
    state_where_is_sword = find_object_states(data.inventory, 'sword')
    print(f"Object state id for sword: {state_where_is_sword}")
    
    # Check achivments in state where was sword
    player_achievements_list = [k for k, v in asdict(data.achievements[state_where_is_sword]).items() if v]

    # Check if the player has a specific achievement using contains_object
    achievement_to_check = 'COLLECT_WOOD'
    has_collect_wood = contains_object(player_achievements_list, achievement_to_check)
    print(f"Player has '{achievement_to_check}' achievement: {has_collect_wood}")

    achievement_to_check = 'MAKE_WOOD_SWORD'
    has_make_wood_sword = contains_object(player_achievements_list, achievement_to_check)
    print(f"Player has '{achievement_to_check}' achievement: {has_make_wood_sword}")
