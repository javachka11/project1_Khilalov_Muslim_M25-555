import math

from labyrinth_game.constants import (
    COMMANDS,
    CRITICAL_HEALTH,
    EVENTS,
    INDENT_INFO,
    PROBABILITIES,
    ROOMS,
)


def describe_current_room(game_state):
    """
        Показать полное описание комнаты.

        game_state - состояние игры на текущий момент.
    """

    cur_room = ROOMS[game_state['current_room']]

    print(f'== {game_state["current_room"].upper()} ==')
    print(f'Описание комнаты: {cur_room["description"]}')
    print(f'Заметные предметы: {cur_room["items"]}')
    print(f'Выходы: {list(cur_room["exits"].keys())}')
    if cur_room["puzzle"] is not None:
        print('Кажется, здесь есть загадка (используйте команду solve).')


def solve_puzzle(game_state):
    """
        Попытаться решить загадку, если она присутствует в комнате.
        За правильное решение загадки игрок получает награду.
        Исключением является загадка в комнате с ловушкой.
        За её правильное решение игрок не получит приз,
        но если он ошибётся, то активирует ловушку.

        game_state - состояние игры на текущий момент.
    """

    cur_room = ROOMS[game_state['current_room']]

    if cur_room['puzzle'] is None:
        print('Загадок здесь нет.')
    else:
        print(f'Загадка: {cur_room["puzzle"]["riddle"]}')
        puzzle_answer = ' '.join(input('Ваш ответ: ').strip().lower().split())
        true_answers = cur_room['puzzle']['answer']
        if puzzle_answer in true_answers:
            print('Ответ правильный.')
            award = cur_room['puzzle'].get('award')            
            # if-clause здесь соответствует комнате с ловушкой
            if award is not None:
                print(award['message'])
                game_state['player_inventory'].append(award['prize'])
            cur_room['puzzle'] = None
        else:
            if game_state['current_room'] == 'trap_room':
                trigger_trap(game_state)
            else:
                print('Неверно. Попробуйте снова.')


def attempt_open_treasure(game_state):
    """
        Попытаться открыть сундук с сокровищем.

        game_state - состояние игры на текущий момент.
    """

    cur_room = ROOMS[game_state['current_room']]

    if 'treasure_key' not in game_state['player_inventory']:
        need_puzzle = input('Сундук заперт. ... Ввести код? (да/нет) ')
        if need_puzzle == 'да':
            solve_puzzle(game_state)
            if cur_room['puzzle'] is None:
                game_state['game_over'] = True
        else:
            print('Вы отступаете от сундука.')
    else:
        print('Вы применяете ключ, и замок щёлкает. Сундук открыт!')
        game_state['game_over'] = True
    
    if game_state['game_over']:
        cur_room['items'].remove('treasure_chest')
        print('В сундуке сокровище! Вы победили!')


def pseudo_random(seed, modulo):
    """
        Сгенерировать псевдослучайное целое число в интервале [0, modulo).

        seed - сид генерации;
        modulo - натуральное число, верхняя граница генерации.
    """

    a = 12.9898
    b = 43758.5453

    num = math.sin(seed * a) * b
    num = num - math.floor(num)
    num = num * modulo
    num = math.floor(num)

    return num


def trigger_trap(game_state):
    """
        Активировать ловушку.

        game_state - состояние игры на текущий момент.
    """

    print('Ловушка активирована! Пол стал дрожать...')

    inventory = game_state['player_inventory']
    if inventory:
        lost_item_ind = pseudo_random(game_state['steps_taken'],
                                      len(inventory))
        lost_item = inventory.pop(lost_item_ind)
        print(f'Вы потеряли предмет {lost_item}')
    else:
        health = pseudo_random(game_state['steps_taken'],
                               PROBABILITIES['damage'])
        if health < CRITICAL_HEALTH:
            print('Поражение. Вы не уцелели.')
            game_state['game_over'] = True
        else:
            print('Вы уцелели.')


def random_event(game_state):
    """
        Сгенерировать случайное событие в комнате.
        Наиболее вероятно, что никакого события не произойдёт.

        game_state - состояние игры на текущий момент.
    """

    not_event = pseudo_random(game_state['steps_taken'],
                              PROBABILITIES['event'])
    if not not_event:
        event = pseudo_random(game_state['steps_taken'],
                              len(EVENTS))
        if event == EVENTS['find_coin']:
            print('Вы увидели на полу монетку.')
            ROOMS[game_state['current_room']]['items'].append('coin')
        elif event == EVENTS['meet_monster']:
            print('Вы слышите шорох.')
            if 'sword' in game_state['player_inventory']:
                print('Вы отпугнули существо.')
        else:
            if (game_state['current_room'] == 'trap_room' and
                'torch' not in game_state['player_inventory']):
                print('Опасность!')
                trigger_trap(game_state)


def show_help():
    """
        Показать панель помощи игроку.
    """
    
    s = 'Доступные команды:\n'
    for command, description in COMMANDS.items():
        s += f'{command:{INDENT_INFO}} - {description}\n'
    print(s)


def quit_game(game_state):
    """
        Завершить игру досрочно.

        game_state - состояние игры на текущий момент.
    """

    game_state['game_over'] = True
    print('Выход из игры.')
