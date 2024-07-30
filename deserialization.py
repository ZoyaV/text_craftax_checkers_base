import json
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass, field

achievements_list = [
    "COLLECT_WOOD", "PLACE_TABLE", "EAT_COW", "COLLECT_SAPLING", "COLLECT_DRINK",
    "MAKE_WOOD_PICKAXE", "MAKE_WOOD_SWORD", "PLACE_PLANT", "DEFEAT_ZOMBIE", "COLLECT_STONE",
    "PLACE_STONE", "EAT_PLANT", "DEFEAT_SKELETON", "MAKE_STONE_PICKAXE", "MAKE_STONE_SWORD",
    "WAKE_UP", "PLACE_FURNACE", "COLLECT_COAL", "COLLECT_IRON", "COLLECT_DIAMOND",
    "MAKE_IRON_PICKAXE", "MAKE_IRON_SWORD", "MAKE_ARROW", "MAKE_TORCH", "PLACE_TORCH",
    "COLLECT_SAPPHIRE", "COLLECT_RUBY", "MAKE_DIAMOND_PICKAXE", "MAKE_DIAMOND_SWORD",
    "MAKE_IRON_ARMOUR", "MAKE_DIAMOND_ARMOUR", "ENTER_GNOMISH_MINES", "ENTER_DUNGEON",
    "ENTER_SEWERS", "ENTER_VAULT", "ENTER_TROLL_MINES", "ENTER_FIRE_REALM", "ENTER_ICE_REALM",
    "ENTER_GRAVEYARD", "DEFEAT_GNOME_WARRIOR", "DEFEAT_GNOME_ARCHER", "DEFEAT_ORC_SOLIDER",
    "DEFEAT_ORC_MAGE", "DEFEAT_LIZARD", "DEFEAT_KOBOLD", "DEFEAT_KNIGHT", "DEFEAT_ARCHER",
    "DEFEAT_TROLL", "DEFEAT_DEEP_THING", "DEFEAT_PIGMAN", "DEFEAT_FIRE_ELEMENTAL",
    "DEFEAT_FROST_TROLL", "DEFEAT_ICE_ELEMENTAL", "DAMAGE_NECROMANCER", "DEFEAT_NECROMANCER",
    "EAT_BAT", "EAT_SNAIL", "FIND_BOW", "FIRE_BOW", "LEARN_FIREBALL", "CAST_FIREBALL",
    "LEARN_ICEBALL", "CAST_ICEBALL", "OPEN_CHEST", "DRINK_POTION", "ENCHANT_SWORD", "ENCHANT_ARMOUR"
]

@dataclass
class PlayerVariables:
    player_position: Tuple[int, int] = (0, 0)
    player_level: int = 0
    player_direction: int = 0
    player_health: float = 0.0
    player_food: int = 0
    player_drink: int = 0
    player_energy: int = 0
    player_mana: int = 0
    is_sleeping: bool = False
    is_resting: bool = False
    player_recover: float = 0.0
    player_hunger: float = 0.0
    player_thirst: float = 0.0
    player_fatigue: float = 0.0
    player_recover_mana: float = 0.0
    player_xp: int = 0
    player_dexterity: int = 0
    player_strength: int = 0
    player_intelligence: int = 0
    learned_spells: List[bool] = field(default_factory=list)
    sword_enchantment: int = 0
    bow_enchantment: int = 0
    boss_progress: int = 0
    boss_timesteps_to_spawn_this_round: int = 0
    light_level: float = 0.0
    state_rng: Tuple[int, int] = (0, 0)
    timestep: int = 0

@dataclass
class PlayerAchievements:
    achievements: List[str] = field(default_factory=list)

@dataclass
class PlayerInventory:
    wood: int = 0
    stone: int = 0
    coal: int = 0
    iron: int = 0
    pickaxe: int = 0
    sword: int = 0
    armour: List[int] = field(default_factory=lambda: [0, 0, 0, 0])
    potions: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0, 0])

@dataclass
class PlayerState:
    variables: PlayerVariables
    achievements: PlayerAchievements
    inventory: PlayerInventory

@dataclass
class GameData:
    states: List[PlayerState] = field(default_factory=list)

    @staticmethod
    def from_json(data: Dict[str, Any]) -> 'GameData':
        states = []
        for key in data['variables']['player_position'].keys():
            key = int(key)
            variables = PlayerVariables(
                player_position=tuple(data['variables']['player_position'][str(key)]),
                player_level=data['variables']['player_level'].get(str(key), 0),
                player_direction=data['variables']['player_direction'].get(str(key), 0),
                player_health=data['variables']['player_health'].get(str(key), 0.0),
                player_food=data['variables']['player_food'].get(str(key), 0),
                player_drink=data['variables']['player_drink'].get(str(key), 0),
                player_energy=data['variables']['player_energy'].get(str(key), 0),
                player_mana=data['variables']['player_mana'].get(str(key), 0),
                is_sleeping=data['variables']['is_sleeping'].get(str(key), False),
                is_resting=data['variables']['is_resting'].get(str(key), False),
                player_recover=data['variables']['player_recover'].get(str(key), 0.0),
                player_hunger=data['variables']['player_hunger'].get(str(key), 0.0),
                player_thirst=data['variables']['player_thirst'].get(str(key), 0.0),
                player_fatigue=data['variables']['player_fatigue'].get(str(key), 0.0),
                player_recover_mana=data['variables']['player_recover_mana'].get(str(key), 0.0),
                player_xp=data['variables']['player_xp'].get(str(key), 0),
                player_dexterity=data['variables']['player_dexterity'].get(str(key), 0),
                player_strength=data['variables']['player_strength'].get(str(key), 0),
                player_intelligence=data['variables']['player_intelligence'].get(str(key), 0),
                learned_spells=data['variables']['learned_spells'].get(str(key), [False, False]),
                sword_enchantment=data['variables']['sword_enchantment'].get(str(key), 0),
                bow_enchantment=data['variables']['bow_enchantment'].get(str(key), 0),
                boss_progress=data['variables']['boss_progress'].get(str(key), 0),
                boss_timesteps_to_spawn_this_round=data['variables']['boss_timesteps_to_spawn_this_round'].get(str(key), 0),
                light_level=data['variables']['light_level'].get(str(key), 0.0),
                state_rng=tuple(data['variables']['state_rng'].get(str(key), (0, 0))),
                timestep=data['variables']['timestep'].get(str(key), 0)
            )
            achievements = PlayerAchievements(
                achievements=data['achievements'].get(str(key), [])
            )
            inventory = PlayerInventory(**data['inventory'].get(str(key), {}))
            states.append(PlayerState(variables=variables, achievements=achievements, inventory=inventory))
        
        return GameData(states=states)

def validate_achievements(player_achievements: List[str]) -> bool:
    return all(achievement in achievements_list for achievement in player_achievements)

def load_game_data(file_path: str) -> GameData:
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return GameData.from_json(json_data)

if __name__ == "__main__":
    # Загрузка данных игры
    game_data = load_game_data('compressed_changes.json')
    
    # Валидация достижений для каждого игрока
    for state in game_data.states:
        if validate_achievements(state.achievements.achievements):
            print(f"State with timestep {state.variables.timestep} achievements are valid.")
        else:
            print(f"State with timestep {state.variables.timestep} has invalid achievements.")

    # Отображение десериализованных данных
    for i, state in enumerate(game_data.states):
        print()
        print(f"===================State {i}=====================")
        print("Variables:", state.variables)
        print("Achievements:", state.achievements)
        print("Inventory:", state.inventory)
        print("==================================================")
        print()
