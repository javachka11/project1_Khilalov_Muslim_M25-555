#!/usr/bin/env python3

from labyrinth_game.utils import describe_current_room

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
        break



if __name__ == '__main__':
    main()
