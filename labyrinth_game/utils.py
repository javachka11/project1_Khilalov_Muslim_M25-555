import math

from labyrinth_game.constants import COMMANDS, ROOMS


def describe_current_room(game_state):
    cur_room = ROOMS[game_state['current_room']]

    print(f'== {game_state["current_room"].upper()} ==')
    print(f'Описание комнаты: {cur_room["description"]}')
    print(f'Заметные предметы: {cur_room["items"]}')
    print(f'Выходы: {list(cur_room["exits"].keys())}')
    if cur_room["puzzle"] is not None:
        print('Кажется, здесь есть загадка (используйте команду solve).')


def solve_puzzle(game_state):
    ALL_ANSWERS = {'hall': ['10', 'десять', 'ten'],
                   'trap_room': ['шаг шаг шаг', 'шагшагшаг',
                                 'шагшаг шаг', 'шагшаг шаг'],
                    'library': ['резонанс', 'resonance'],
                    'treasure_room': ['10', 'десять', 'ten'],
                    'skeleton_room': ['01:40', '1:40',
                                      '01 40', '0140',
                                      '1 40', '140',
                                      '01:40:00', '1:40:00',
                                      '1 hour 40 minutes',
                                      'one hour fourty minutes',
                                      '1 час 40 минут',
                                      'один час сорок минут',
                                      'час сорок',
                                      'час сорок минут',
                                      'без 20 2',
                                      'без двадцати два']}

    AWARDS = {'hall': {'message': 'Сундукт открылся и вы получаете rusty_key.',
                       'prize': 'rusty_key'},
              'library': {'message': 'Свиток указывает вам на ключ от сокровищницы.',
                          'prize': 'treasure_key'},
              'treasure_room': {'message': 'Код открывает сундук.',
                                'prize': 'treasure'},
              'skeleton_room': {'message': 'Скелет рассыпается и ' \
                                'роняет ключ от сокровищницы.',
                                'prize': 'treasure_key'}}
    
    RIDDLE = 0

    cur_room = ROOMS[game_state['current_room']]
    if cur_room['puzzle'] is None:
        print('Загадок здесь нет.')
    else:
        print(f'Загадка. {cur_room["puzzle"][RIDDLE]}')
        puzzle_answer = ' '.join(input('Ваш ответ: ').strip().lower().split())
        true_answers = ALL_ANSWERS[game_state['current_room']]
        if puzzle_answer in true_answers:
            print('Ответ правильный.')
            cur_room['puzzle'] = None
            award = AWARDS.get(game_state['current_room'])
            if award is not None:
                print(award['message'])
                game_state['player_inventory'].append(award['prize'])
        else:
            print('Неверно. Попробуйте снова.')
            if game_state['current_room'] == 'trap_room':
                trigger_trap(game_state)


def attempt_open_treasure(game_state):
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
    a = 12.9898
    b = 43758.5453

    num = math.sin(seed * a) * b
    num = num - math.floor(num)
    num = num * modulo
    num = math.floor(num)

    return num


def trigger_trap(game_state):
    DAMAGE_PROBABILITY = 10
    CRITICAL_HEALTH = 3

    print('Ловушка активирована! Пол стал дрожать...')

    inventory = game_state['player_inventory']
    if inventory:
        health = pseudo_random(game_state['steps_taken'],
                               DAMAGE_PROBABILITY)
        if health < CRITICAL_HEALTH:
            print('Поражение. Вы не уцелели.')
            game_state['game_over'] = True
        else:
            print('Вы уцелели.')
    else:
        lost_item_ind = pseudo_random(game_state['steps_taken'],
                                      len(inventory))
        lost_item = inventory.pop(lost_item_ind)
        print(f'Вы потеряли предмет {lost_item}')


def random_event(game_state):
    EVENT_PROBABILITY = 10
    NUM_EVENTS = 3
    FIND_COIN = 0
    MEET_MONSTER = 1

    not_event = pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY)
    if not not_event:
        event = pseudo_random(game_state['steps_taken'], NUM_EVENTS)
        if event == FIND_COIN:
            print('Вы увидели на полу монетку.')
            ROOMS[game_state['current_room']]['items'].append('coin')
        elif event == MEET_MONSTER:
            print('Вы слышите шорох.')
            if 'sword' in game_state['player_inventory']:
                print('Вы отпугнули существо.')
        else:
            if (game_state['current_room'] == 'trap_room' and
                'torch' not in game_state['player_inventory']):
                print('Опасность!')
                trigger_trap(game_state)


def show_help():
    INDENT = 16

    s = 'Доступные команды:\n'
    for command, description in COMMANDS.items():
        s += f'{command:{INDENT}} - {description}\n'
    print(s)


def quit_game(game_state):
    game_state['game_over'] = True
    print('Выход из игры.')

