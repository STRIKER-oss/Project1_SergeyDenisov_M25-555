"""Вспомогательные функции игры."""
import math

from .constants import ROOMS

SIN_MULTIPLIER = 12.9898
RANDOM_MULTIPLIER = 43758.5453


EVENT_PROBABILITY = 10
EVENT_TYPES = 3
DAMAGE_THRESHOLD = 3


TRAP_DAMAGE_CHANCE = 10


def pseudo_random(seed, modulo):
    """Псевдослучайный генератор на основе синуса."""
    sin_value = math.sin(seed * SIN_MULTIPLIER)
    multiplied_value = sin_value * RANDOM_MULTIPLIER
    fractional_part = multiplied_value - math.floor(multiplied_value)
    result = fractional_part * modulo
    return math.floor(result)


def trigger_trap(game_state):
    """Активировать ловушку."""
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]

    if inventory:
        item_index = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory[item_index]
        inventory.pop(item_index)
        print(f"Из ваших рук выпал {lost_item} и потерялся в темноте!")
    else:
        damage_chance = pseudo_random(game_state["steps_taken"], TRAP_DAMAGE_CHANCE)
        if damage_chance < DAMAGE_THRESHOLD:
            print("Вас настигает ловушка! Игра окончена.")
            game_state["game_over"] = True
        else:
            print("Вам удалось увернуться от ловушки!")


def random_event(game_state):
    """Случайное событие при перемещении."""
    event_chance = pseudo_random(game_state["steps_taken"], EVENT_PROBABILITY)

    if event_chance == 0:
        event_type = pseudo_random(game_state["steps_taken"] + 1, EVENT_TYPES)

        if event_type == 0:
            print("Вы заметили что-то блестящее на полу...")
            current_room = ROOMS[game_state["current_room"]]
            if "coin" not in current_room["items"]:
                current_room["items"].append("coin")
                print("Вы нашли монетку!")
            else:
                print("Но это оказалась всего лишь пыль.")

        elif event_type == 1:
            print("Вы слышите странный шорох в темноте...")
            if "sword" in game_state["player_inventory"]:
                print("Вы размахиваете мечом и отпугиваете существо!")
            else:
                print("Шорох стихает, но чувство тревоги остаётся.")

        elif event_type == 2:
            current_room = game_state["current_room"]
            has_torch = "torch" in game_state["player_inventory"]
            if current_room == "trap_room" and not has_torch:
                print("Вы не заметили ловушку в темноте!")
                trigger_trap(game_state)
            else:
                print(
                    "Вы чувствуете, что могли наступить на ловушку, "
                    "но вовремя отпрыгнули."
                )


def describe_current_room(game_state):
    """Описать текущую комнату."""
    room_name = game_state["current_room"]
    room_data = ROOMS[room_name]

    print(f"== {room_name.upper()} ==")
    print(room_data["description"])

    if room_data["items"]:
        print("Заметные предметы:", ", ".join(room_data["items"]))

    print("Выходы:", ", ".join(room_data["exits"].keys()))

    if room_data["puzzle"]:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """Решить загадку в текущей комнате."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    if not room["puzzle"]:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room["puzzle"]
    print(f"\nЗагадка: {question}")

    user_answer = input("Ваш ответ: ").strip().lower()

    correct_answers = [correct_answer.lower()]
    if correct_answer == "10":
        correct_answers.extend(["десять", "10"])

    if user_answer in correct_answers:
        print("Правильно! Загадка решена.")
        room["puzzle"] = None

        if room_name == "hall":
            game_state["player_inventory"].append("treasure_key")
            print("Вы получили treasure key!")
        elif room_name == "library":
            game_state["player_inventory"].append("ancient_scroll")
            print("Вы получили ancient scroll!")
        elif room_name == "trap_room":
            print("Ловушка деактивирована! Теперь можно безопасно перемещаться.")
        else:
            print("Вы чувствуете себя умнее!")

    else:
        print("Неверно. Попробуйте снова.")
        if room_name == "trap_room":
            print("Ловушка срабатывает из-за неправильного ответа!")
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """Попытаться открыть сундук с сокровищами."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    if "treasure chest" not in room["items"]:
        print("Сундук уже открыт или отсутствует.")
        return False

    inventory = game_state["player_inventory"]

    if "treasure_key" in inventory or "rusty_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room["items"].remove("treasure chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return True

    print("Сундук заперт. У вас нет подходящего ключа.")
    try_code = input("Ввести код? (да/нет): ").strip().lower()

    if try_code == "да":
        code = input("Введите код: ").strip()
        if code == "10":
            print("Код принят! Сундук открыт!")
            room["items"].remove("treasure chest")
            print("В сундуке сокровище! Вы победили!")
            game_state["game_over"] = True
            return True
        else:
            print("Неверный код.")
    else:
        print("Вы отступаете от сундука.")

    return False


def show_help():
    """Показать справку по командам."""
    from .constants import COMMANDS

    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f"  {command:<16} - {description}")
