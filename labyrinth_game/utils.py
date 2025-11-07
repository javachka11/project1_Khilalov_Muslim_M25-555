from labyrinth_game.constants import ROOMS
import math

def describe_current_room(game_state):
    cur_room = ROOMS[game_state['current_room']]

    print(f'== {game_state["current_room"].upper()} ==')
    print(f'Описание комнаты: {cur_room["description"]}')
    print(f'Заметные предметы: {cur_room["items"]}')
    print(f'Выходы: {list(cur_room["exits"].keys())}')
    if cur_room["puzzle"] is not None:
        print(f'Кажется, здесь есть загадка (используйте команду solve).')

def get_award(room):
    match room:
        case 'hall':
            print('Сундукт открылся и вы получаете rusty_key.')
            return 'rusty_key'
        case 'trap_room':
            print('Вы проскользнули через плиты и миновали ловушку.')
            return None
        case 'library':
            print('Свиток указывает вам на ключ от сокровищницы.')
            return 'treasure_key'
        case 'treasure_room':
            print('Код открывает сундук.')
            return 'treasure'
        case 'skeleton_room':
            print('Скелет рассыпается и роняет ключ от сокровищницы.')
            return 'treasure_key'
        case _:
            return None


def solve_puzzle(game_state):
    cur_room = ROOMS[game_state['current_room']]
    if cur_room['puzzle'] is None:
        print('Загадок здесь нет.')
    else:
        print(f'Загадка. {cur_room["puzzle"][0]}')
        puzzle_answer = input('Ваш ответ: ')
        if puzzle_answer == cur_room['puzzle'][1]:
            print('Ответ правильный.')
            cur_room['puzzle'] = None
            award = get_award(game_state['current_room'])
            if award is not None:
                game_state['player_inventory'].append(award)
        else:
            print('Неверно. Попробуйте снова.')


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
    print('Ловушка активирована! Пол стал дрожать...')

    inventory = game_state['player_inventory']
    if inventory:
        damage = pseudo_random(game_state['steps_taken'], 10)
        if damage < 3:
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
    not_event = pseudo_random(game_state['steps_taken'], 6)
    if not not_event:
        event = pseudo_random(game_state['steps_taken'], 3)
        if event == 0:
            print('Вы увидели на полу монетку.')
            ROOMS[game_state['current_room']]['items'].append('coin')
        elif event == 1:
            print('Вы слышите шорох.')
            if 'sword' in game_state['player_inventory']:
                print('Вы отпугнули существо.')
        else:
            if (game_state['current_room'] == 'trap_room' and
                'torch' not in game_state['player_inventory']):
                print('Опасность!')
                trigger_trap(game_state)







def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")


def quit_game(game_state):
    game_state['game_over'] = True
    print('Выход из игры.')

