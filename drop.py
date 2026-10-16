import random
import database


common = [
    "frog",
    "rocket",
    "recycle bin",
    "trash",
    "hard hat"
]

rare = [
    "big trash",
    "iron hard hat",
    "crital frog",
    "ninja recycle bin"
]

epic = [
    "slot machine",
    "monochrome frog",
    "wild card",
    "diamond plate hard hat"
]

legendary = [
    "deal maker",
    "australium hard hat",
    "demon card"
]

miracle = [
    "MASTER WORLD CASINO",
    "MASTER AUSTRALIUM FROG"
]


def epic_drop():
    return random.choice(epic)


def common_drop():
    return random.choice(common)


def rare_drop():
    return random.choice(rare)


def legen_drop():
    return random.choice(legendary)


def miracle_drop():
    return random.choice(miracle)


def wooden_box():
    drop = random.randint(1, 100)

    if drop <= 70:
        return common_drop()
    elif drop <= 95:
        return rare_drop()
    else:
        return epic_drop()


def brick_box():
    drop = random.randint(1, 100)

    if drop <= 55:
        return common_drop()
    elif drop <= 75:
        return rare_drop()
    elif drop <= 99:
        return epic_drop()
    else:
        return legen_drop()


def steel_box():
    drop = random.randint(1, 100)

    if drop <= 75:
        return rare_drop()
    elif drop <= 85:
        return epic_drop()
    else:
        return legen_drop()


def australium_box():
    drop = random.randint(1, 100)

    if drop <= 55:
        return epic_drop()
    elif drop <= 99:
        return legen_drop()
    else:
        return miracle_drop()


box_prices = {
    "wooden box": 120,
    "brick box": 200,
    "steel box": 320,
    "australium box": 600
}


def play(user_id):
    coins = database.show_coins(user_id)
    
    # Check if user exists and has enough coins
    if coins is not None and coins >= 15:
        slots = []

        for _ in range(3):
            slots.append(random.choice([1, 2, 3, 4, 5, 6, 7]))

        if slots[0] == slots[1] == slots[2]:
            database.update_coins(user_id, 50)
            return slots, 50

        database.update_coins(user_id, -15)
        return slots, -15
    else:
        return False