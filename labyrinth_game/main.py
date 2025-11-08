#!/usr/bin/env python3

from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    quit_game,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command):
    """
        Обработать команду в соответствии с логикой игры.

        game_state - состояние игры на текущий момент;
        command - команда интерфейса (для информации - help).
    """

    command_args = command.strip().lower().split()
    match command_args:
        case ['look']:
            describe_current_room(game_state)
        case ['go', direction]:
            move_player(game_state, direction)
        case ['north']:
            move_player(game_state, 'north')
        case ['east']:
            move_player(game_state, 'east')
        case ['south']:
            move_player(game_state, 'south')
        case ['west']:
            move_player(game_state, 'west')
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
        case ['help']:
            show_help()
        case ['quit']:
            quit_game(game_state)
        case _:
            print('Команда не найдена.')


def main():
    """
        Основная функция игры.
    """

    # print("Первая попытка запустить проект!")
    game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
    }

    print('Добро пожаловать в Лабиринт сокровищ!\n')

    describe_current_room(game_state)
    print('')
    while not game_state['game_over']:
        command = get_input()
        process_command(game_state, command)
        print('')

if __name__ == '__main__':
    main()
