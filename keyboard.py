from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="🎁 Open Boxes", callback_data="menu_boxes"),
            InlineKeyboardButton(text="🎰 Play Slots", callback_data="play_slots"),
        ],
        [
            InlineKeyboardButton(text="🎒 My Inventory", callback_data="show_inventory"),
            InlineKeyboardButton(text="💰 My Coins", callback_data="show_coins"),
        ],
        [
            InlineKeyboardButton(text="⚙️ Settings", callback_data="menu_settings")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_boxes_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="📦 Wooden Box (120 coins)", callback_data="buy_wooden box"),
            InlineKeyboardButton(text="🧱 Brick Box (200 coins)", callback_data="buy_brick box"),
        ],
        [
            InlineKeyboardButton(text="🛡️ Steel Box (320 coins)", callback_data="buy_steel box"),
            InlineKeyboardButton(text="✨ Australium Box (600 coins)", callback_data="buy_australium box"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Back to Menu", callback_data="back_to_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Back to Menu", callback_data="back_to_menu")]
        ]
    )


def get_settings_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="⚠️ Delete Account", callback_data="confirm_delete"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Back to Menu", callback_data="back_to_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_delete_confirm_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Yes, Delete My Account", callback_data="execute_delete"),
            InlineKeyboardButton(text="❌ Cancel", callback_data="back_to_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)