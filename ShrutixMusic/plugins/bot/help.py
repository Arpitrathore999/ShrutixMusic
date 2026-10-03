import random
from typing import Union

from pyrogram import enums, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from ShrutixMusic import nand
from ShrutixMusic.utils.rich_ui import rich_edit, rich_esc, rich_heading, rich_img, rich_note, rich_send, rich_table, rich_details, sanitize_display_name
from ShrutixMusic.utils.database import get_lang
from ShrutixMusic.utils.decorators.language import languageCB
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT, SUPPORT_CHANNEL
from strings import get_string, helpers

TOPICS = {f"hb{i}": getattr(helpers, f"HELP_{i}") for i in range(1, 17)}
PAGE_ONE = [f"hb{i}" for i in range(1, 10)]
PAGE_TWO = [f"hb{i}" for i in range(10, 17)]
LABELS = {f"hb{i}": f"H_B_{i}" for i in range(1, 17)}


def _topic_page(key):
    return 1 if int(key[2:]) <= 9 else 2


def _menu_keyboard():
    rows = []
    for page in (PAGE_ONE, PAGE_TWO):
        rows.extend([
            [InlineKeyboardButton(get_string("en")[LABELS[a]], callback_data=f"richhelp:{a}", style=enums.ButtonStyle.PRIMARY) for a in page[i:i+3]]
            for i in range(0, len(page), 3)
        ])
        if page is PAGE_ONE:
            rows.append([InlineKeyboardButton("▷ ɴᴇxᴛ", callback_data="richhelp:page:2", style=enums.ButtonStyle.SUCCESS)])
    rows.append([InlineKeyboardButton("⌯ ᴄʟᴏsᴇ ⌯", callback_data="richhelp:close", style=enums.ButtonStyle.DANGER)])
    return InlineKeyboardMarkup(rows)


def _page_keyboard(page=1):
    items = PAGE_ONE if page == 1 else PAGE_TWO
    rows = []
    language = get_string("en")
    for i in range(0, len(items), 3):
        rows.append([InlineKeyboardButton(language[LABELS[k]], callback_data=f"richhelp:{k}", style=enums.ButtonStyle.PRIMARY) for k in items[i:i+3]])
    nav = []
    if page == 1:
        nav.append(InlineKeyboardButton("▷ ɴᴇxᴛ", callback_data="richhelp:page:2", style=enums.ButtonStyle.SUCCESS))
    else:
        nav.append(InlineKeyboardButton("◁ ᴘʀᴇᴠ", callback_data="richhelp:page:1", style=enums.ButtonStyle.SUCCESS))
    nav.append(InlineKeyboardButton("⌯ ᴄʟᴏsᴇ ⌯", callback_data="richhelp:close", style=enums.ButtonStyle.DANGER))
    rows.append(nav)
    return InlineKeyboardMarkup(rows)


def _menu_caption(uid, name, page=1):
    bot_name = rich_esc(getattr(nand, "name", "ShrutixMusic"))
    return (
        rich_img(START_IMG_URL)
        + rich_note(f"<p>❍ ʜᴇʏ <a href=\"tg://user?id={uid}\">{rich_esc(name)}</a>, ᴘɪᴄᴋ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ ᴛᴏ sᴇᴇ ɪᴛs ᴄᴏᴍᴍᴀɴᴅs.</p>")
        + rich_details("✦ ʜᴇʟᴘ &amp; ᴄᴏᴍᴍᴀɴᴅs ✦", rich_table(["ғᴇᴀᴛᴜʀᴇ", "ᴅᴇᴛᴀɪʟs"], [("✉️ ʜᴇʟᴘ ᴍᴇɴᴜ", "ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴀʀᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ʜᴇʀᴇ"), ("📄 ᴘᴀɢᴇ", f"{page} / 2")]), open=True)
        + rich_note(f"ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <b>{bot_name}</b>")
        + (f'<p><tg-button type="url" style="primary" url="{rich_esc(SUPPORT_CHAT)}">🍬 sᴜᴘᴘᴏʀᴛ ↗</tg-button> <tg-button type="url" style="success" url="{rich_esc(SUPPORT_CHANNEL)}">🍹 ᴜᴘᴅᴀᴛᴇs ↗</tg-button></p>' if SUPPORT_CHAT or SUPPORT_CHANNEL else "")
    )


def _topic_caption(uid, key):
    title = get_string("en")[LABELS[key]]
    return (
        rich_img(START_IMG_URL)
        + rich_heading(f"📜 {rich_esc(title)}", level=3)
        + rich_note(TOPICS[key])
        + rich_details("✧ ɴᴏᴛᴇ ✧", "<p>ᴜsᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ʀᴇᴛᴜʀɴ ᴛᴏ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ.</p>", open=True)
    )


async def send_help_menu(message: Message, delete_command=True):
    if delete_command:
        try:
            await message.delete()
        except Exception:
            pass
    name = sanitize_display_name(message.from_user.first_name)
    return await rich_send(nand, message.chat.id, _menu_caption(message.from_user.id, name, 1), reply_markup=_page_keyboard(1), effect_id=random.choice([5107584321108051014, 5159385139981059251, 5104841245755180586, 5046509860389126442]))


@nand.on_message(filters.command(["help"]) & ~BANNED_USERS)
async def helper(message_client, message: Message):
    await send_help_menu(message)


@nand.on_callback_query(filters.regex(r"^show_help$") & ~BANNED_USERS)
async def show_help_cb(client, callback: types.CallbackQuery):
    await callback.answer()
    uid = callback.from_user.id
    name = sanitize_display_name(callback.from_user.first_name)
    await rich_edit(callback, _menu_caption(uid, name, 1), reply_markup=_page_keyboard(1), client=nand)


@nand.on_callback_query(filters.regex(r"^richhelp:") & ~BANNED_USERS)
async def rich_help_cb(client, callback: types.CallbackQuery):
    await callback.answer()
    parts = callback.data.split(":")
    if parts[1] == "close":
        try:
            await callback.message.delete()
        except Exception:
            pass
        return
    if parts[1] == "page":
        page = int(parts[2])
        await rich_edit(callback, _menu_caption(callback.from_user.id, sanitize_display_name(callback.from_user.first_name), page), reply_markup=_page_keyboard(page), client=nand)
        return
    key = parts[1]
    if key not in TOPICS:
        return
    page = _topic_page(key)
    back = InlineKeyboardMarkup([[InlineKeyboardButton("◁ ʙᴀᴄᴋ", callback_data=f"richhelp:page:{page}", style=enums.ButtonStyle.PRIMARY), InlineKeyboardButton("⌯ ᴄʟᴏsᴇ ⌯", callback_data="richhelp:close", style=enums.ButtonStyle.DANGER)]])
    await rich_edit(callback, _topic_caption(callback.from_user.id, key), reply_markup=back, client=nand)


@nand.on_callback_query(filters.regex(r"^settings_back_helper$") & ~BANNED_USERS)
async def legacy_help_back(client, callback: types.CallbackQuery):
    await callback.answer()
    await rich_edit(callback, _menu_caption(callback.from_user.id, sanitize_display_name(callback.from_user.first_name), 1), reply_markup=_page_keyboard(1), client=nand)
