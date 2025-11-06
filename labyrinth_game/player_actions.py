def show_inventory(game_state):
    items = game_state['player_inventory']
    if items:
        print(f'Инвентарь: {items}')
    else:
        print('Инвентарь пуст')

def get_input(prompt="> "):
    try:
        print('тут ваш код')
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
