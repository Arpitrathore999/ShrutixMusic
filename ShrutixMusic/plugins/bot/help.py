import random
from typing import Union

from pyrogram import enums, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from ShrutixMusic import nand
from ShrutixMusic.utils.database import get_lang
from ShrutixMusic.utils.decorators.language import LanguageStart, languageCB
from ShrutixMusic.utils.rich_ui import (
    rich_edit,
    rich_esc,
    rich_heading,
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

HELP_TOPICS = {
    f"hb{i}": getattr(helpers, f"HELP_{i}", "No commands available.")
    for i in range(1, 17)
}

# Names are intentionally short so the keyboard looks like the Outlaw screenshot.
TOPIC_NAMES = {
    "hb1": "ᴧᴅᴍɪɴ",
    "hb2": "ᴧ-ᴘʟᴀʏ",
    "hb3": "ɢ-ᴄᴧsᴛ",
    "hb4": "ʙʟ-ᴄʜᴧᴛ",
    "hb5": "ʙʟ-ᴜsᴇʀs",
    "hb6": "ᴘɪɴɢ",
    "hb7": "ᴘʟᴀʏ",
    "hb8": "sᴘᴇᴇᴅ",
    "hb9": "ɪɴғᴏ",
    "hb10": "ᴍɪsᴄ",
    "hb11": "sᴇᴛᴛɪɴɢs",
    "hb12": "sᴜᴅᴏ",
    "hb13": "ᴛᴏᴏʟs",
    "hb14": "ʟᴀɴɢ",
    "hb15": "ʙʀᴏᴀᴅᴄᴀsᴛ",
    "hb16": "ᴅᴇᴠ",
}


def _help_keyboard(page=1):
    keys = list(HELP_TOPICS)
    keys = keys[:9] if page == 1 else keys[9:]
    rows = []
    for i in range(0, len(keys), 3):
        rows.append(
            [
                InlineKeyboardButton(
                    TOPIC_NAMES.get(key, key),
                    callback_data=f"rich_help_topic {key} {page}",
                    style=enums.ButtonStyle.PRIMARY,
                )
                for key in keys[i : i + 3]
            ]
        )

    nav = []
    if page == 1:
        nav.append(
            InlineKeyboardButton(
                "⌯ ɴᴇxᴛ ⌯",
                callback_data="rich_help_page 2",
                style=enums.ButtonStyle.SUCCESS,
            )
        )
    else:
        nav.append(
            InlineKeyboardButton(
                "⌯ ᴘʀᴇᴠ ⌯",
                callback_data="rich_help_page 1",
                style=enums.ButtonStyle.SUCCESS,
            )
        )
    nav.append(
        InlineKeyboardButton(
            "⌯ ᴄʟᴏsᴇ ⌯",
            callback_data="rich_help_close",
            style=enums.ButtonStyle.DANGER,
        )
    )
    rows.append(nav)
    return InlineKeyboardMarkup(rows)


def _help_text(uid, name, page=1):
    return (
        rich_heading("📜 ᴄʜᴏᴏsᴇ ᴀ ᴄᴀᴛᴇɢᴏʀʏ", level=3)
        + rich_img(START_IMG_URL)
        + rich_note(
            f"<p>❍ ʜᴇʏ <a href='tg://user?id={uid}'>{rich_esc(sanitize_display_name(name))}</a>, "
            "ᴘɪᴄᴋ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ ᴛᴏ sᴇᴇ ɪᴛs ᴄᴏᴍᴍᴀɴᴅs.</p>"
        )
        + rich_note(
            "<b>✦ ʜᴇʟᴘ ғᴇᴀᴛᴜʀᴇs ✦</b>"
            "<br/>✉️ ʜᴇʟᴘ ᴍᴇɴᴜ — ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /"
        )
        + rich_note(
            f"ᴘᴀɢᴇ <b>{page}/2</b> • ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='{SUPPORT_CHAT}'>sʜʀᴜᴛɪx ꭙ ᴍᴜsɪᴄ</a>"
        )
    )


@nand.on_message(filters.command(["help"]) & ~BANNED_USERS)
@LanguageStart
async def helper(client, message: Message, _):
    try:
        await message.delete()
    except Exception:
        pass

    await rich_send(
        nand,
        message.chat.id,
        _help_text(message.from_user.id, message.from_user.first_name),
        reply_markup=_help_keyboard(1),
        effect_id=random.choice(MESSAGE_EFFECTS) if message.chat.type == "private" else None,
    )


@nand.on_callback_query(filters.regex(r"^rich_help_menu$") & ~BANNED_USERS)
async def rich_help_menu(client, callback):
    await callback.answer()
    text = _help_text(
        callback.from_user.id,
        callback.from_user.first_name,
        1,
    )
    await rich_edit(callback, text, reply_markup=_help_keyboard(1), client=nand)


@nand.on_callback_query(filters.regex(r"^rich_help_page (1|2)$") & ~BANNED_USERS)
async def rich_help_page(client, callback):
    page = int(callback.matches[0].group(1))
    await callback.answer()
    text = _help_text(
        callback.from_user.id,
        callback.from_user.first_name,
        page,
    )
    await rich_edit(callback, text, reply_markup=_help_keyboard(page), client=nand)


@nand.on_callback_query(filters.regex(r"^rich_help_topic (hb\d+) \d+$") & ~BANNED_USERS)
async def rich_help_topic(client, callback):
    key = callback.matches[0].group(1)
    page = int(callback.data.rsplit(" ", 1)[1])
    body = HELP_TOPICS.get(key, "No commands available.")
    title = TOPIC_NAMES.get(key, "ʜᴇʟᴘ")

    await callback.answer()
    text = (
        rich_heading(f"📜 {rich_esc(title)}", level=3)
        + rich_img(START_IMG_URL)
        + rich_note(str(body))
        + rich_note(f"ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='{SUPPORT_CHAT}'>sʜʀᴜᴛɪx ꭙ ᴍᴜsɪᴄ</a>")
    )
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                "‹ ʙᴀᴄᴋ",
                callback_data=f"rich_help_page {page}",
                style=enums.ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                "✕ ᴄʟᴏsᴇ",
                callback_data="rich_help_close",
                style=enums.ButtonStyle.DANGER,
            ),
        ]]
    )
    await rich_edit(callback, text, reply_markup=keyboard, client=nand)


@nand.on_callback_query(filters.regex(r"^rich_help_close$") & ~BANNED_USERS)
async def rich_help_close(client, callback):
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass


# Keep the original group-help behavior available for existing translations.
@nand.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_group(client, message: Message, _):
    from ShrutixMusic.utils.inline.help import private_help_panel

    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))
