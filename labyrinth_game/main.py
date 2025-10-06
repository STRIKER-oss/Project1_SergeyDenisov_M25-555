#!/usr/bin/env python3
"""Основной модуль игры 'Лабиринт сокровищ'."""

from .player_actions import get_input, move_player, show_inventory, take_item, use_item
from .utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle


def process_command(game_state, command):
    """Обработать команду игрока."""
    parts = command.split()
    if not parts:
        return

    action = parts[0]

    match action:
        case "look":
            describe_current_room(game_state)
        case "inventory":
            show_inventory(game_state)
        case "go":
            if len(parts) > 1:
                direction = parts[1]
                move_player(game_state, direction)
            else:
                print("Укажите направление: go north/south/east/west")
        case "north" | "south" | "east" | "west":
            move_player(game_state, action)
        case "take":
            if len(parts) > 1:
                item_name = " ".join(parts[1:])
                take_item(game_state, item_name)
            else:
                print("Укажите предмет: take <item>")
        case "use":
            if len(parts) > 1:
                item_name = " ".join(parts[1:])
                use_item(game_state, item_name)
                if (
                    item_name == "treasure chest"
                    and game_state["current_room"] == "treasure_room"
                ):
                    attempt_open_treasure(game_state)
        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "help":
            show_help()
        case "quit" | "exit":
            print("До свидания!")
            game_state["game_over"] = True
        case _:
            print("Неизвестная команда. Введите 'help' для справки.")


def main():
    """Главная функция игры."""
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    print("Введите 'help' для списка команд.")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input("\nВведите команду: ")
        process_command(game_state, command)

    print(f"\nИгра завершена. Сделано шагов: {game_state['steps_taken']}")


if __name__ == "__main__":
    main()
