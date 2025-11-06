from labyrinth_game.constants import ROOMS

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

# labyrinth_game/utils.py
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
