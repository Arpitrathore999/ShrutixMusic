import random
from typing import Union

from pyrogram import filters, types
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from ShrutixMusic import nand
from ShrutixMusic.utils import help_pannel
from ShrutixMusic.utils.database import get_lang
from ShrutixMusic.utils.decorators.language import LanguageStart, languageCB
from ShrutixMusic.utils.inline.help import private_help_panel
from ShrutixMusic.utils.rich_ui import (
    rich_details,
    rich_edit,
    rich_esc,
    rich_img,
    rich_note,
    rich_send,
    rich_table,
    sanitize_display_name,
)
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers

MESSAGE_EFFECTS = [
    5107584321108051014,
    5159385139981059251,
    5104841245755180586,
    5046509860389126442,
]

HELP_TOPICS = {f"hb{i}": getattr(helpers, f"HELP_{i}") for i in range(1, 17)}
PAGE_ONE = [f"hb{i}" for i in range(1, 10)]
PAGE_TWO = [f"hb{i}" for i in range(10, 17)]


def _chunk(items, size):
    return [items[i : i + size] for i in range(0, len(items), size)]


def _help_markup(page=1, start=False):
    items = PAGE_ONE if page == 1 else PAGE_TWO
    rows = []
    for chunk in _chunk(items, 3):
        rows.append(
            [
                InlineKeyboardButton(
                    text={
                        "hb1": "🎛️ ᴀᴅᴍɪɴ",
                        "hb2": "🔐 ᴀᴜᴛʜ",
                        "hb3": "📢 ɢᴄᴀsᴛ",
                        "hb4": "🚫 ʙʟ-ᴄʜᴀᴛ",
                        "hb5": "⛔ ʙʟ-ᴜsᴇʀs",
                        "hb6": "📡 ᴄʜᴀɴɴᴇʟ",
                        "hb7": "🔨 ɢʙᴀɴ",
                        "hb8": "🔁 ʟᴏᴏᴘ",
                        "hb9": "🛠️ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ",
                        "hb10": "🏓 ᴘɪɴɢ & sᴛᴀᴛs",
                        "hb11": "🎵 ᴘʟᴀʏ",
                        "hb12": "📥 sᴇᴇᴋ",
                        "hb13": "⚡ sᴘᴇᴇᴅ",
                        "hb14": "🧰 ᴛᴏᴏʟs",
                        "hb15": "👑 sᴜᴅᴏ",
                        "hb16": "⚙️ sᴇᴛᴛɪɴɢs",
                    }[key],
                    callback_data=f"help_callback {key} {'1' if start else '0'}",
                    style=ButtonStyle.PRIMARY,
                )
                for key in chunk
            ]
        )
    if page == 1:
        rows.append(
            [
                InlineKeyboardButton("✕ ᴄʟᴏsᴇ", callback_data="close", style=ButtonStyle.DEFAULT),
                InlineKeyboardButton("ɴᴇxᴛ ➜", callback_data=f"help_page 2 {'1' if start else '0'}", style=ButtonStyle.SUCCESS),
            ]
        )
    else:
        rows.append(
            [
                InlineKeyboardButton("← ᴘʀᴇᴠ", callback_data=f"help_page 1 {'1' if start else '0'}", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton("✕ ᴄʟᴏsᴇ", callback_data="close", style=ButtonStyle.DEFAULT),
            ]
        )
    return InlineKeyboardMarkup(rows)


def _help_html(user=None, page=1):
    name = sanitize_display_name(user.first_name) if user else "User"
    uid = user.id if user else 0
    return (
        rich_img(START_IMG_URL)
        + rich_note(
            f"<p>❍ ʜᴇʏ <a href=\"tg://user?id={uid}\">{rich_esc(name)}</a>, "
            "ʜᴇʀᴇ ᴀʀᴇ ᴀʟʟ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ʏᴏᴜ ᴄᴀɴ ᴜsᴇ.</p>"
            "<p>ᴛᴀᴘ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ ᴛᴏ ᴠɪᴇᴡ ɪᴛs ᴄᴏᴍᴍᴀɴᴅs.</p>"
        )
        + rich_details(
            "✦ ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs ✦",
            rich_table(
                ["ᴄᴀᴛᴇɢᴏʀʏ", "ᴜsᴇ"],
                [
                    ("🎵 ᴘʟᴀʏ", "ᴍᴜsɪᴄ & ᴠᴏɪᴄᴇ ᴄʜᴀᴛ"),
                    ("🎛️ ᴀᴅᴍɪɴ", "ᴘʟᴀʏᴇʀ ᴄᴏɴᴛʀᴏʟs"),
                    ("🛠️ ᴛᴏᴏʟs", "ᴜᴛɪʟɪᴛɪᴇs & sᴛᴀᴛs"),
                    ("👑 sᴜᴅᴏ", "ᴏᴡɴᴇʀ/ᴅᴇᴠ ᴄᴏᴍᴍᴀɴᴅs"),
                ],
            ),
            open=True,
        )
        + rich_note(f"<p>ᴘᴀɢᴇ <b>{page}</b> • sᴇʟᴇᴄᴛ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ.</p>")
    )


def _topic_html(key):
    # Existing help strings already use Telegram-compatible HTML. Wrap them in a rich block.
    return rich_img(START_IMG_URL) + rich_details("✦ ᴄᴏᴍᴍᴀɴᴅ ᴅᴇᴛᴀɪʟs ✦", HELP_TOPICS[key], open=True)


async def send_help_message(message: Message, effect_id=None):
    try:
        await message.delete()
    except Exception:
        pass
    await rich_send(
        nand,
        message.chat.id,
        _help_html(message.from_user, 1),
        reply_markup=_help_markup(1, False),
        effect_id=effect_id or random.choice(MESSAGE_EFFECTS),
    )


@nand.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@nand.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client, update: Union[types.Message, types.CallbackQuery]):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except Exception:
            pass
        chat_id = update.message.chat.id
        user = update.from_user
        await rich_edit(update, _help_html(user, 1), reply_markup=_help_markup(1, True), client=client)
    else:
        await send_help_message(update)


@nand.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


@nand.on_callback_query(filters.regex("help_page") & ~BANNED_USERS)
@languageCB
async def help_page_cb(client, CallbackQuery, _):
    parts = CallbackQuery.data.split()
    page = int(parts[1])
    start = len(parts) > 2 and parts[2] == "1"
    try:
        await CallbackQuery.answer()
    except Exception:
        pass
    await rich_edit(
        CallbackQuery,
        _help_html(CallbackQuery.from_user, page),
        reply_markup=_help_markup(page, start),
        client=client,
    )


@nand.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    parts = CallbackQuery.data.strip().split()
    cb = parts[1]
    start = len(parts) > 2 and parts[2] == "1"
    page = 1 if int(cb[2:]) <= 9 else 2
    try:
        await CallbackQuery.answer()
    except Exception:
        pass
    await rich_edit(
        CallbackQuery,
        _topic_html(cb),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "← ʙᴀᴄᴋ",
                        callback_data=f"help_page {page} {'1' if start else '0'}",
                        style=ButtonStyle.PRIMARY,
                    )
                ]
            ]
        ),
        client=client,
    )
