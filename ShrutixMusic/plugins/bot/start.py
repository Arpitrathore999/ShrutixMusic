import random
import time

from pyrogram import enums, filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from py_yt import VideosSearch

import config
from ShrutixMusic import nand
from ShrutixMusic.misc import _boot_
from ShrutixMusic.plugins.sudo.sudoers import sudoers_list
from ShrutixMusic.utils.database import add_served_chat, add_served_user, blacklisted_chats, get_lang, is_banned_user, is_on_off
from ShrutixMusic.utils.decorators.language import LanguageStart
from ShrutixMusic.utils.formatters import get_readable_time
from ShrutixMusic.utils.rich_ui import rich_details, rich_esc, rich_heading, rich_img, rich_kv_table, rich_note, rich_send, rich_table, sanitize_display_name
from ShrutixMusic.utils.inline import start_panel
from config import BANNED_USERS
from strings import get_string

MESSAGE_EFFECTS = [5107584321108051014, 5159385139981059251, 5104841245755180586, 5046509860389126442]


def _buttons(group=False):
    bot_link = getattr(config, "BOT_LINK", f"https://t.me/{getattr(config, 'BOT_USERNAME', '')}")
    support = getattr(config, "SUPPORT_CHAT", "")
    updates = getattr(config, "SUPPORT_CHANNEL", support)
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⛩️ ᴧᴅᴅ ᴍᴇ ⛩️", url=f"{bot_link}?startgroup=true", style=enums.ButtonStyle.PRIMARY)],
        [InlineKeyboardButton("🍬 sᴜᴘᴘᴏʀᴛ", url=support, style=enums.ButtonStyle.SUCCESS), InlineKeyboardButton("🍹 ᴜᴘᴅᴀᴛᴇs", url=updates, style=enums.ButtonStyle.SUCCESS)],
        [InlineKeyboardButton("🏩 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="rich_help", style=enums.ButtonStyle.PRIMARY)],
        [InlineKeyboardButton("🫧 ᴏᴡɴᴇʀ", url=f"tg://user?id={config.OWNER_ID}"), InlineKeyboardButton("🍡 ʜᴇʟᴘ", callback_data="rich_help")],
    ])


def _caption(uid, name, group=False, title=""):
    if group:
        return (rich_img(config.START_IMG_URL) + rich_heading(f"❍ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {rich_esc(title)}", 2)
                + rich_note(f"ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ <b>{rich_esc(config.BOT_NAME)}</b>. ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ ʏᴏᴜʀ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs ᴡɪᴛʜ ᴇᴀsᴇ.")
                + rich_details("✦ ᴋᴇʏ ғᴇᴀᴛᴜʀᴇs ✦", rich_table(["ғᴇᴀᴛᴜʀᴇ", "ᴅᴇᴛᴀɪʟs"], [("🎵 sᴛʀᴇᴀᴍɪɴɢ", "ᴀᴜᴅɪᴏ & ᴠɪᴅᴇᴏ"), ("🔁 ᴀᴜᴛᴏᴘʟᴀʏ", "ǫᴜᴇᴜᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ"), ("🎚️ ᴇғғᴇᴄᴛs", "sᴘᴇᴇᴅ & ᴘʟᴀʏᴍᴏᴅᴇ")]), True))
    return (rich_img(config.START_IMG_URL) + rich_note(f"❍ ʜᴇʏ <a href='tg://user?id={uid}'>{rich_esc(name)}</a>, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ <b>{rich_esc(config.BOT_NAME)}</b> 🎶")
            + rich_details("✦ ᴋᴇʏ ғᴇᴀᴛᴜʀᴇs ✦", rich_table(["ғᴇᴀᴛᴜʀᴇ", "ᴅᴇᴛᴀɪʟs"], [("🎵 sᴛʀᴇᴀᴍɪɴɢ", "ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs"), ("🔁 ᴀᴜᴛᴏᴘʟᴀʏ", "ᴋᴇᴇᴘ ᴛʜᴇ ǫᴜᴇᴜᴇ ɢᴏɪɴɢ"), ("🛡️ ᴍᴏᴅᴇʀᴀᴛɪᴏɴ", "ᴀᴅᴍɪɴ & ʙᴏᴛ ᴛᴏᴏʟs")]), True))


@nand.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    name_arg = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else ""
    if name_arg.startswith("help"):
        return await message.reply_photo(config.START_IMG_URL, caption=_["help_1"].format(config.SUPPORT_CHAT), reply_markup=__import__('ShrutixMusic.utils.inline', fromlist=['help_pannel']).help_pannel(_), effect_id=random.choice(MESSAGE_EFFECTS))
    if name_arg.startswith("sud"):
        await sudoers_list(client=client, message=message, _=_)
        if await is_on_off(2):
            await nand.send_message(config.LOGGER_ID, text=f"{message.from_user.mention} started sudo check. ID: <code>{message.from_user.id}</code>")
        return
    if name_arg.startswith("inf"):
        m = await message.reply_text("🔎")
        query = f"https://www.youtube.com/watch?v={name_arg.replace('info_', '', 1)}"
        result = (await VideosSearch(query, limit=1).next())["result"][0]
        key = InlineKeyboardMarkup([[InlineKeyboardButton("▶️ ᴡᴀᴛᴄʜ", url=result["link"]), InlineKeyboardButton("🍬 sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT)]])
        await m.delete()
        return await nand.send_photo(message.chat.id, result["thumbnails"][0]["url"].split("?")[0], caption=_["start_6"].format(result["title"], result["duration"], result["viewCount"]["short"], result["publishedTime"], result["channel"]["link"], result["channel"]["name"], nand.mention), reply_markup=key)
    try:
        await rich_send(nand, message.chat.id, _caption(message.from_user.id, message.from_user.first_name), reply_markup=_buttons())
    except Exception:
        await message.reply_photo(config.START_IMG_URL, caption=_["start_2"].format(message.from_user.mention, nand.mention), reply_markup=InlineKeyboardMarkup(start_panel(_)), effect_id=random.choice(MESSAGE_EFFECTS))


@nand.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    try:
        await rich_send(nand, message.chat.id, _caption(message.from_user.id, message.from_user.first_name, True, message.chat.title or "this chat"), reply_markup=_buttons(True))
    except Exception:
        await message.reply_photo(config.START_IMG_URL, caption=_["start_1"].format(nand.mention, get_readable_time(int(time.time() - _boot_))), reply_markup=InlineKeyboardMarkup(start_panel(_)))
    await add_served_chat(message.chat.id)


@nand.on_callback_query(filters.regex("^rich_help$") & ~BANNED_USERS)
async def rich_help_cb(client, callback):
    from strings import helpers
    rows = []
    for i in range(1, 17):
        rows.append(InlineKeyboardButton(f"❖ ʜᴇʟᴘ {i}", callback_data=f"rich_help_{i}"))
    kb = InlineKeyboardMarkup([rows[i:i+2] for i in range(0, len(rows), 2)] + [[InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="rich_start_back")]])
    text = rich_img(config.START_IMG_URL) + rich_heading("🏩 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", 2) + rich_note("sᴇʟᴇᴄᴛ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ᴛᴏ ᴠɪᴇᴡ ᴄᴏᴍᴍᴀɴᴅs.")
    await callback.answer()
    await rich_send(nand, callback.message.chat.id, text, reply_markup=kb)


@nand.on_callback_query(filters.regex(r"^rich_help_(\d+)$") & ~BANNED_USERS)
async def rich_help_topic(client, callback):
    from strings import helpers
    i = int(callback.matches[0].group(1))
    body = getattr(helpers, f"HELP_{i}", "No commands available.")
    text = rich_heading(f"❖ ʜᴇʟᴘ {i}", 2) + rich_note(str(body))
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="rich_help"), InlineKeyboardButton("✕ ᴄʟᴏsᴇ", callback_data="rich_close")]])
    await callback.answer()
    await callback.message.edit_text(text, reply_markup=kb)


@nand.on_callback_query(filters.regex("^rich_start_back$") & ~BANNED_USERS)
async def rich_start_back(client, callback):
    await callback.answer()
    await callback.message.edit_text(_caption(callback.from_user.id, callback.from_user.first_name), reply_markup=_buttons())


@nand.on_callback_query(filters.regex("^rich_close$") & ~BANNED_USERS)
async def rich_close(client, callback):
    await callback.answer()
    await callback.message.delete()


@nand.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id); _ = get_string(language)
            if await is_banned_user(member.id):
                try: await message.chat.ban_member(member.id)
                except: pass
            if member.id == nand.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"]); return await nand.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(_["start_5"].format(nand.mention, f"https://t.me/{nand.username}?start=sudolist", config.SUPPORT_CHAT)); return await nand.leave_chat(message.chat.id)
                await rich_send(nand, message.chat.id, _caption(message.from_user.id, message.from_user.first_name, True, message.chat.title or "this chat"), reply_markup=_buttons(True))
                await add_served_chat(message.chat.id); await message.stop_propagation()
        except Exception as ex: print(ex)
