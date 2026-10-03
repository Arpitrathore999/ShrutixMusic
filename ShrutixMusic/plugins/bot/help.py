from typing import Union
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from ShrutixMusic import nand
from ShrutixMusic.utils.database import get_lang
from ShrutixMusic.utils.rich_ui import rich_heading, rich_note, rich_send
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers

TOPICS = {f"hb{i}": getattr(helpers, f"HELP_{i}", "No commands available.") for i in range(1, 17)}

def menu():
    buttons = [InlineKeyboardButton(f"❖ ʜᴇʟᴘ {i}", callback_data=f"rh_{i}") for i in range(1,17)]
    return InlineKeyboardMarkup([buttons[i:i+2] for i in range(0,16,2)] + [[InlineKeyboardButton("✕ ᴄʟᴏsᴇ", callback_data="rh_close")]])

@nand.on_message(filters.command(["help"]) & ~BANNED_USERS)
async def help_handler(client, message: Message):
    try: await message.delete()
    except: pass
    text = rich_heading("🏩 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", 2) + rich_note("sᴇʟᴇᴄᴛ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ ᴛᴏ ᴠɪᴇᴡ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs.")
    await rich_send(nand, message.chat.id, text, reply_markup=menu())

@nand.on_callback_query(filters.regex(r"^rh_(\d+)$") & ~BANNED_USERS)
async def help_topic(client, callback):
    n = int(callback.matches[0].group(1)); body = TOPICS.get(f"hb{n}", "No commands available.")
    await callback.answer()
    text = rich_heading(f"❖ ʜᴇʟᴘ {n}", 2) + rich_note(str(body))
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="rh_menu"), InlineKeyboardButton("✕ ᴄʟᴏsᴇ", callback_data="rh_close")]])
    await callback.message.edit_text(text, reply_markup=kb)

@nand.on_callback_query(filters.regex("^rh_menu$") & ~BANNED_USERS)
async def help_menu(client, callback):
    await callback.answer()
    text = rich_heading("🏩 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", 2) + rich_note("sᴇʟᴇᴄᴛ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ ᴛᴏ ᴠɪᴇᴡ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs.")
    await callback.message.edit_text(text, reply_markup=menu())

@nand.on_callback_query(filters.regex("^rh_close$") & ~BANNED_USERS)
async def help_close(client, callback):
    await callback.answer(); await callback.message.delete()
