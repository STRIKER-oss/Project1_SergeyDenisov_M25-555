#!/usr/bin/env python3
"""Основной модуль игры 'Лабиринт сокровищ'."""
from .constants import ROOMS
from .player_actions import get_input, show_inventory, move_player, take_item, use_item
from .utils import describe_current_room, solve_puzzle, attempt_open_treasure, show_help


def process_command(game_state, command):
    """Обработать команду игрока."""
    # Разделяем строку на части
    parts = command.split()
    
    # Если команда пустая, ничего не делаем
    if not parts:
        return
    
    # Берем первую часть как команду
    action = parts[0]
    
    # Используем match/case для определения команды
    match action:
        case "look":
            describe_current_room(game_state)
        
        case "inventory":
            show_inventory(game_state)
        
        case "go":
            # Проверяем есть ли направление
            if len(parts) > 1:
                direction = parts[1]
                move_player(game_state, direction)
            else:
                print("Укажите направление: go north/south/east/west")
        
        case "take":
            # Проверяем есть ли название предмета
            if len(parts) > 1:
                item_name = parts[1]
                take_item(game_state, item_name)
            else:
                print("Укажите предмет: take <item>")
        
        case "use":
            # Проверяем есть ли название предмета
            if len(parts) > 1:
                item_name = parts[1]
                use_item(game_state, item_name)
                
                # Особый случай: использование treasure_chest в treasure_room
                if (item_name == 'treasure_chest' and 
                    game_state['current_room'] == 'treasure_room'):
                    attempt_open_treasure(game_state)
        
        case "solve":
            solve_puzzle(game_state)
            
            # Если решили загадку в treasure_room, пробуем открыть сундук
            if (game_state['current_room'] == 'treasure_room' and 
                ROOMS['treasure_room']['puzzle'] is None):
                attempt_open_treasure(game_state)
        
        case "help":
            show_help()
        
        case "quit" | "exit":
            print("До свидания!")
            game_state['game_over'] = True
        
        case _:
            print("Неизвестная команда. Введите 'help' для справки.")


def main():
    """Главная функция игры."""
    # Создаем состояние игры
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance', 
        'game_over': False,
        'steps_taken': 0
    }
    
    # Приветственное сообщение
    print("Добро пожаловать в Лабиринт сокровищ!")
    print("Введите 'help' для списка команд.")
    
    # Показываем стартовую комнату
    describe_current_room(game_state)
    
    # Цикл игры
    while not game_state['game_over']:
        # Считываем команду от пользователя
        command = get_input("\nВведите команду: ")
        
        # Обрабатываем команду
        process_command(game_state, command)
    
    print(f"\nИгра завершена. Сделано шагов: {game_state['steps_taken']}")


# Стандартная конструкция для запуска
if __name__ == "__main__":
    main()