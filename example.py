from deserialization import load_game_data
from checkers import validate_achievements, is_variable_increasing, is_variable_decreasing, find_item_in_inventory, is_achievement_obtained, find_achievement_state

# Загрузка данных игры
game_data = load_game_data('compressed_changes.json')

# Проверка, увеличивается ли определенная переменная в выбранном диапазоне стейтов
variable_name = 'player_health'
start_index = 0
end_index = 7

try:
    if is_variable_increasing(game_data, variable_name, start_index, end_index):
        print(f"The variable '{variable_name}' is increasing from state {start_index} to {end_index}.")
    else:
        print(f"The variable '{variable_name}' is not consistently increasing from state {start_index} to {end_index}.")
except ValueError as e:
    print(e)

# Проверка, убывает ли определенная переменная в выбранном диапазоне стейтов
try:
    if is_variable_decreasing(game_data, variable_name, start_index, end_index):
        print(f"The variable '{variable_name}' is decreasing from state {start_index} to {end_index}.")
    else:
        print(f"The variable '{variable_name}' is not consistently decreasing from state {start_index} to {end_index}.")
except ValueError as e:
    print(e)

# Проверка в каких стейтах присутствует определенный объект в инвентаре
item_name = 'wood'

states_with_item = find_item_in_inventory(game_data, item_name)
if states_with_item:
    print(f"The item '{item_name}' is present in the inventory of states: {states_with_item}.")
else:
    print(f"The item '{item_name}' is not present in the inventory of any state.")

# Проверка, была ли получена определенная ачивка в определенном промежутке стейтов
achievement_name = 'COLLECT_WOOD'
start_index = 0
end_index = 4

try:
    if is_achievement_obtained(game_data, achievement_name, start_index, end_index):
        print(f"The achievement '{achievement_name}' was obtained between states {start_index} and {end_index}.")
    else:
        print(f"The achievement '{achievement_name}' was not obtained between states {start_index} and {end_index}.")
except ValueError as e:
    print(e)

# Поиск стейтов, в которых была получена определенная ачивка
states_with_achievement = find_achievement_state(game_data, achievement_name)
if states_with_achievement!=-1:
    print(f"The achievement '{achievement_name}' was obtained in the states: {states_with_achievement}.")
else:
    print(f"The achievement '{achievement_name}' was not obtained in any state.")


import deserialization
import checkers

# Load game data
game_data = deserialization.load_game_data('compressed_changes.json')

# Check if the player moved south between states 0 and 1
try:
    moved_south = checkers.did_player_go_south(game_data, 0, 1)
    print(f"Player moved south: {moved_south}")
except IndexError as e:
    print(f"Error: {e}")

