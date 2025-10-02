"""Действия игрока."""
# Убираем импорт из utils здесь, будем импортировать внутри функций когда нужно


def get_input(prompt="> "):
    """Получить ввод от пользователя."""
    try:
        # Просим пользователя ввести команду
        user_input = input(prompt)
        # Убираем лишние пробелы и делаем маленькими буквами
        return user_input.strip().lower()
    except (KeyboardInterrupt, EOFError):
        # Если пользователь нажал Ctrl+C или Ctrl+D
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state):
    """Показать инвентарь игрока."""
    # Получаем инвентарь из game_state
    inventory = game_state['player_inventory']
    
    # Проверяем, есть ли предметы
    if inventory:
        # Если есть предметы, показываем их
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        # Если нет предметов, сообщаем что пусто
        print("Ваш инвентарь пуст.")


def move_player(game_state, direction):
    """Переместить игрока в указанном направлении."""
    # Импортируем внутри функции чтобы избежать циклического импорта
    from .constants import ROOMS
    from .utils import describe_current_room
    
    # Получаем текущую комнату
    current_room = game_state['current_room']
    
    # Получаем выходы из текущей комнаты
    exits = ROOMS[current_room]['exits']
    
    # Проверяем, существует ли выход в этом направлении
    if direction in exits:
        # Если выход есть, обновляем текущую комнату
        game_state['current_room'] = exits[direction]
        
        # Увеличиваем шаг на единицу
        game_state['steps_taken'] += 1
        
        # Выводим описание новой комнаты
        describe_current_room(game_state)
        
        return True
    else:
        # Если выхода нет, выводим сообщение
        print("Нельзя пойти в этом направлении.")
        return False


def take_item(game_state, item_name):
    """Взять предмет из комнаты."""
    # Импортируем внутри функции чтобы избежать циклического импорта
    from .constants import ROOMS
    
    # Получаем текущую комнату
    current_room = game_state['current_room']
    
    # Получаем предметы в текущей комнате
    room_items = ROOMS[current_room]['items']
    
    # Проверяем, есть ли предмет в комнате
    if item_name in room_items:
        # Если предмет есть, добавляем его в инвентарь игрока
        game_state['player_inventory'].append(item_name)
        
        # Удаляем предмет из списка предметов комнаты
        room_items.remove(item_name)
        
        # Печатаем сообщение о том, что игрок подобрал предмет
        print(f"Вы подняли: {item_name}")
        
        return True
    else:
        # Если такого предмета нет, выводим сообщение
        print("Такого предмета здесь нет.")
        return False


def use_item(game_state, item_name):
    """Использовать предмет из инвентаря."""
    # Получаем инвентарь игрока
    inventory = game_state['player_inventory']
    
    # Проверяем, есть ли предмет в инвентаре
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return
    
    # Проверяем какой предмет используется
    if item_name == "torch":
        print("Вы зажигаете факел. Стало светлее!")
    
    elif item_name == "sword":
        print("Вы размахиваете мечом. Чувствуете себя увереннее!")
    
    elif item_name == "bronze box":
        # Проверяем, есть ли уже rusty key в инвентаре
        if "rusty_key" not in inventory:
            print("Вы открываете бронзовую шкатулку и находите внутри rusty key!")
            inventory.append("rusty_key")
        else:
            print("Шкатулка уже пуста.")
    
    else:
        # Для остальных предметов
        print(f"Вы не знаете, как использовать {item_name}.")