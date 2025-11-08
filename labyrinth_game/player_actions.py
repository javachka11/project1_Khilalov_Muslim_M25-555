from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import (
    random_event,
)


def show_inventory(game_state):
    """
        Показать инвентарь игрока.

        game_state - состояние игры на текущий момент.
    """

    items = game_state['player_inventory']
    if items:
        print(f'Инвентарь: {items}')
    else:
        print('Инвентарь пуст.')



def get_input(prompt="> "):
    """
        Получить команду от игрока.

        prompt - окно приглашения для ввода.
    """

    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        return "quit"



def move_player(game_state, direction):
    """
        Переместиться в заданном направлении.

        game_state - состояние игры на текущий момент;
        direction - направление (north/east/south/west) перехода.
    """

    exits = ROOMS[game_state['current_room']]['exits']

    next_room = exits.get(direction)
    if next_room:
        if next_room == 'treasure_room':
            if 'rusty_key' in game_state['player_inventory']:
                print('Вы используете найденный ключ, ' \
                'чтобы открыть путь в комнату сокровищ.')
            else:
                print('Дверь заперта. Нужен ключ, ' \
                'чтобы пройти дальше.')
                return
        game_state['current_room'] = next_room
        game_state['steps_taken'] += 1
        print(f'Описание комнаты: {ROOMS[next_room]["description"]}')
        random_event(game_state)
    else:
        print('Нельзя пойти в этом направлении.')



def take_item(game_state, item_name):
    """
        Попытаться подобрать предмет.
        В случае успеха он переместится в инвентарь игрока.

        game_state - состояние игры на текущий момент;
        item_name - название предмета.
    """

    room_items = ROOMS[game_state['current_room']]['items']

    if item_name in room_items:
        if item_name == 'treasure_chest':
            print('Вы не можете поднять сундук, он слишком тяжелый.')
        else:
            game_state['player_inventory'].append(item_name)
            room_items.remove(item_name)
            print(f'Вы подняли: {item_name}')
    else:
        print('Такого предмета здесь нет.')
        

def use_item(game_state, item_name):
    """
        Попытаться использовать предмет.

        game_state - состояние игры на текущий момент;
        item_name - название предмета.
    """

    player_items = game_state['player_inventory']
    
    if item_name in player_items:
        if item_name == 'torch':
            print('Стало светлее.')
        elif item_name == 'sword':
            print('Уверенность увеличена!')
        elif item_name == 'bronze_box' and 'rusty_key' not in player_items:
            print('Открытие шкатулки... Вы получаете ржавый ключ!')
            player_items.append('rusty_key')
        elif item_name == 'bronze_box':
            print('Открытие шкатулки... Пусто.')
        else:
            print('Игрок не знает, как использовать предмет.')
    else:
        print('У вас нет такого предмета.')
