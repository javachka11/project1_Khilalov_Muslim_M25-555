#!/usr/bin/env python3

from labyrinth_game.utils import describe_current_room, \
                                 solve_puzzle, \
                                 attempt_open_treasure
from labyrinth_game.player_actions import get_input, \
                                          move_player, \
                                          take_item, \
                                          use_item, \
                                          show_inventory
                                          

def process_command(game_state, command):
    command_args = command.strip().lower().split()
    match command_args:
        case ['look']:
            describe_current_room(game_state)
        case ['go', direction]:
            move_player(game_state, direction)
        case ['take', item]:
            take_item(game_state, item)
        case ['use', item]:
            use_item(game_state, item)
        case ['inventory']:
            show_inventory(game_state)
        case ['solve'] if game_state['current_room'] == 'treasure_room':
            attempt_open_treasure(game_state)
        case ['solve']:
            solve_puzzle(game_state)
        case _:
            raise ValueError('Команда не найдена.')

def main():
    # print("Первая попытка запустить проект!")
    game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
    }

    print('Добро пожаловать в Лабиринт сокровищ!')

    describe_current_room(game_state)

    while True:
        command = get_input()
        if command in ['exit', 'quit'] or game_state['game_over']:
            return
        try:
            process_command(game_state, command)
        except ValueError:
            return


if __name__ == '__main__':
    main()
