"""Вспомогательные функции игры."""
from .constants import ROOMS
# Убираем импорт get_input из player_actions, будем использовать встроенный input


def describe_current_room(game_state):
    """Описать текущую комнату."""
    # Получаем название текущей комнаты
    room_name = game_state['current_room']
    
    # Получаем данные о комнате из ROOMS
    room_data = ROOMS[room_name]
    
    # Выводим название комнаты в верхнем регистре
    print(f"== {room_name.upper()} ==")
    
    # Выводим описание комнаты
    print(room_data['description'])
    
    # Проверяем есть ли предметы в комнате
    if room_data['items']:
        # Если есть предметы, показываем их
        print("Заметные предметы:", ", ".join(room_data['items']))
    
    # Показываем доступные выходы
    print("Выходы:", ", ".join(room_data['exits'].keys()))
    
    # Проверяем есть ли загадка
    if room_data['puzzle']:
        # Если есть загадка, сообщаем об этом
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """Решить загадку в текущей комнате."""
    # Получаем текущую комнату
    room_name = game_state['current_room']
    room = ROOMS[room_name]
    
    # Проверяем, есть ли загадка в комнате
    if not room['puzzle']:
        print("Загадок здесь нет.")
        return
    
    # Получаем вопрос и правильный ответ
    question, correct_answer = room['puzzle']
    
    # Выводим вопрос
    print(f"\nЗагадка: {question}")
    
    # Получаем ответ от пользователя (используем встроенный input)
    user_answer = input("Ваш ответ: ").strip().lower()
    
    # Сравниваем ответ пользователя с правильным
    if user_answer == correct_answer.lower():
        print("Правильно! Загадка решена.")
        
        # Убираем загадку из комнаты
        room['puzzle'] = None
        
        # Добавляем награду игроку
        game_state['player_inventory'].append('treasure_key')
        print("Вы получили treasure key!")
        
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    """Попытаться открыть сундук с сокровищами."""
    # Получаем текущую комнату
    room_name = game_state['current_room']
    room = ROOMS[room_name]
    
    # Проверяем наличие сундука
    if 'treasure_chest' not in room['items']:
        print("Сундук уже открыт или отсутствует.")
        return False
    
    # Получаем инвентарь игрока
    inventory = game_state['player_inventory']
    
    # Проверяем ключи у игрока
    if 'treasure_key' in inventory or 'rusty_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        
        # Удаляем сундук из комнаты
        room['items'].remove('treasure_chest')
        
        # Сообщаем о победе
        print("В сундуке сокровище! Вы победили!")
        
        # Завершаем игру
        game_state['game_over'] = True
        return True
    
    # Если ключей нет, предлагаем ввести код
    print("Сундук заперт. У вас нет подходящего ключа.")
    
    # Спрашиваем, хочет ли игрок ввести код (используем встроенный input)
    try_code = input("Ввести код? (да/нет): ").strip().lower()
    
    if try_code == 'да':
        # Запрашиваем код
        code = input("Введите код: ").strip()
        
        # Проверяем код (правильный код из загадки treasure_room)
        if code == '10':
            print("Код принят! Сундук открыт!")
            
            # Удаляем сундук из комнаты
            room['items'].remove('treasure_chest')
            
            # Сообщаем о победе
            print("В сундуке сокровище! Вы победили!")
            
            # Завершаем игру
            game_state['game_over'] = True
            return True
        else:
            print("Неверный код.")
    else:
        print("Вы отступаете от сундука.")
    
    return False


def show_help():
    """Показать справку по командам."""
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")