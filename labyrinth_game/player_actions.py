"""Действия игрока."""


def get_input(prompt="> "):
    """Получить ввод от пользователя."""
    try:
        user_input = input(prompt)
        return user_input.strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state):
    """Показать инвентарь игрока."""
    inventory = game_state["player_inventory"]
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")


def move_player(game_state, direction):
    """Переместить игрока в указанном направлении."""
    from .constants import ROOMS
    from .utils import describe_current_room, random_event

    current_room = game_state["current_room"]
    exits = ROOMS[current_room]["exits"]

    if direction in exits:
        next_room = exits[direction]

        if next_room == "treasure_room":
            if "rusty key" in game_state["player_inventory"]:
                print("Вы используете ключ, чтобы открыть путь в сокровищницу.")
                game_state["current_room"] = next_room
                game_state["steps_taken"] += 1
                describe_current_room(game_state)
                random_event(game_state)
                return True
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return False

        game_state["current_room"] = next_room
        game_state["steps_taken"] += 1
        describe_current_room(game_state)
        random_event(game_state)
        return True
    else:
        print("Нельзя пойти в этом направлении.")
        return False


def take_item(game_state, item_name):
    """Взять предмет из комнаты."""
    from .constants import ROOMS

    current_room = game_state["current_room"]
    room_items = ROOMS[current_room]["items"]

    if item_name in room_items:
        game_state["player_inventory"].append(item_name)
        room_items.remove(item_name)
        print(f"Вы подняли: {item_name}")
        return True

    for room_item in room_items:
        if item_name.lower() in room_item.lower():
            game_state["player_inventory"].append(room_item)
            room_items.remove(room_item)
            print(f"Вы подняли: {room_item}")
            return True

    print("Такого предмета здесь нет.")
    return False


def use_item(game_state, item_name):
    """Использовать предмет из инвентаря."""
    inventory = game_state["player_inventory"]

    if item_name in inventory:
        if item_name == "torch":
            print("Вы зажигаете факел. Стало светлее!")
        elif item_name == "sword":
            print("Вы размахиваете мечом. Чувствуете себя увереннее!")
        elif item_name == "bronze box":
            if "rusty key" not in inventory:
                print("Вы открываете бронзовую шкатулку и находите внутри rusty key!")
                inventory.append("rusty key")
            else:
                print("Шкатулка уже пуста.")
        else:
            print(f"Вы не знаете, как использовать {item_name}.")
        return

    for inv_item in inventory:
        if item_name.lower() in inv_item.lower():
            if "torch" in inv_item.lower():
                print("Вы зажигаете факел. Стало светлее!")
            elif "sword" in inv_item.lower():
                print("Вы размахиваете мечом. Чувствуете себя увереннее!")
            elif "bronze" in inv_item.lower() and "box" in inv_item.lower():
                if "rusty key" not in inventory:
                    print("Вы открываете шкатулку и находите внутри rusty key!")
                    inventory.append("rusty key")
                else:
                    print("Шкатулка уже пуста.")
            else:
                print(f"Вы не знаете, как использовать {inv_item}.")
            return

    print("У вас нет такого предмета.")
