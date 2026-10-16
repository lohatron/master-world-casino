import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

from database import (
    init_db,
    new_user,
    find_user,
    add_toy,
    show_items,
    show_coins,
    trade_items,
    delete_account,
    update_coins
)
from drop import (
    box_prices,
    wooden_box,
    brick_box,
    steel_box,
    australium_box,
    play
)
from keyboard import (
    get_main_menu_keyboard,
    get_boxes_keyboard,
    get_back_keyboard,
    get_settings_keyboard,
    get_delete_confirm_keyboard
)

load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("env load failure")

dp = Dispatcher()
bot = Bot(token=TOKEN)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.full_name

    if not find_user(user_id):
        new_user(user_id, username)

    await message.answer(
        f"Welcome, {username}! 🎉\nChoose an option below to manage your inventory, play slots, or open boxes:",
        reply_markup=get_main_menu_keyboard()
    )


@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Main Menu:",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "show_coins")
async def cb_show_coins(callback: CallbackQuery):
    user_id = callback.from_user.id
    coins = show_coins(user_id) or 0
    await callback.message.edit_text(
        f"💰 You currently have **{coins}** coins.",
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@dp.callback_query(F.data == "show_inventory")
async def cb_show_inventory(callback: CallbackQuery):
    user_id = callback.from_user.id
    items = show_items(user_id)
    
    if not items:
        text = "🎒 Your inventory is empty!"
    else:
        text = "🎒 **Your Inventory:**\n" + "\n".join(f"- {item}" for item in items)

    await callback.message.edit_text(
        text,
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@dp.callback_query(F.data == "menu_boxes")
async def cb_menu_boxes(callback: CallbackQuery):
    await callback.message.edit_text(
        "📦 Choose a box to open:",
        reply_markup=get_boxes_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("buy_"))
async def cb_buy_box(callback: CallbackQuery):
    user_id = callback.from_user.id
    box_name = callback.data.split("_", 1)[1]
    cost = box_prices.get(box_name, 0)
    
    user_coins = show_coins(user_id) or 0
    if user_coins < cost:
        await callback.answer(f"❌ You need {cost} coins, but you only have {user_coins}!", show_alert=True)
        return

    # Deduct coins & open box
    update_coins(user_id, -cost)

    item = None
    if box_name == "wooden box":
        item = wooden_box()
    elif box_name == "brick box":
        item = brick_box()
    elif box_name == "steel box":
        item = steel_box()
    elif box_name == "australium box":
        item = australium_box()

    if item:
        add_toy(item, user_id)
        await callback.message.edit_text(
            f"🎉 You opened a **{box_name}** for {cost} coins and got:\n\n✨ **{item}** ✨",
            reply_markup=get_boxes_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await callback.answer("Error opening box.", show_alert=True)


@dp.callback_query(F.data == "play_slots")
async def cb_play_slots(callback: CallbackQuery):
    user_id = callback.from_user.id
    result = play(user_id)

    if result is False:
        await callback.answer("❌ You need at least 15 coins to play the slots!", show_alert=True)
        return

    slots, delta = result
    user_coins = show_coins(user_id) or 0

    if delta > 0:
        msg = f"🎰 Slots: `{slots}`\n🎉 JACKPOT! You won **+{delta}** coins!\n💰 Total coins: {user_coins}"
    else:
        msg = f"🎰 Slots: `{slots}`\n😢 You lost **{abs(delta)}** coins.\n💰 Total coins: {user_coins}"

    await callback.message.edit_text(
        msg,
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


# --- SETTINGS & ACCOUNT DELETION ---

@dp.callback_query(F.data == "menu_settings")
async def cb_settings(callback: CallbackQuery):
    await callback.message.edit_text(
        "⚙️ **Account Settings:**\nDeleting your account will erase all your items and coins permanently.",
        reply_markup=get_settings_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@dp.callback_query(F.data == "confirm_delete")
async def cb_confirm_delete(callback: CallbackQuery):
    await callback.message.edit_text(
        "⚠️ **Are you absolutely sure?** This action cannot be undone!",
        reply_markup=get_delete_confirm_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@dp.callback_query(F.data == "execute_delete")
async def cb_execute_delete(callback: CallbackQuery):
    user_id = callback.from_user.id
    success = delete_account(user_id)
    
    if success:
        await callback.message.edit_text(
            "😢 Your account and all associated data have been deleted. Send /start if you ever want to return!"
        )
    else:
        await callback.answer("❌ Error: Account not found.", show_alert=True)
    await callback.answer()


# --- TRADING ITEMS ---
# Command format: /trade <other_user_id> "your item" "their item"

@dp.message(Command("trade"))
async def cmd_trade(message: Message):
    args = message.text.split(maxsplit=3)
    
    if len(args) < 4:
        await message.reply(
            "❌ **Usage:** `/trade <user_id> \"your item\" \"their item\"`\n"
            "Example: `/trade 123456789 frog rocket`",
            parse_mode="Markdown"
        )
        return
    
    try:
        user1_id = message.from_user.id
        user2_id = int(args[1])
        item1 = args[2].strip('"')
        item2 = args[3].strip('"')
        
        success = trade_items(user1_id, item1, user2_id, item2)
        
        if success:
            await message.reply(f"✅ Successfully traded **{item1}** for user `{user2_id}`'s **{item2}**!")
        else:
            await message.reply("❌ Trade failed. Check if both users exist, you own item1, and they own item2.")
            
    except ValueError:
        await message.reply("❌ Invalid User ID format. Make sure it's a number.")


async def main():
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())