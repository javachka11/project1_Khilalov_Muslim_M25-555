from labyrinth_game.constants import ROOMS

def describe_current_room(game_state):
    cur_room = ROOMS[game_state['current_room']]

    print(f'== {game_state["current_room"].upper()} ==')
    print(f'Описание комнаты: {cur_room["description"]}')
    print(f'Заметные предметы: {cur_room["items"]}')
    print(f'Выходы: {list(cur_room["exits"].keys())}')
    if cur_room["puzzle"] is not None:
        print(f'Кажется, здесь есть загадка (используйте команду solve).')
