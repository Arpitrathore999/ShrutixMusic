import asyncio
import random

from pyrogram import enums, filters
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from py_yt import VideosSearch

import config
from ShrutixMusic import nand
from ShrutixMusic.misc import _boot_
from ShrutixMusic.plugins.sudo.sudoers import sudoers_list
from ShrutixMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from ShrutixMusic.utils.decorators.language import LanguageStart
from ShrutixMusic.utils.formatters import get_readable_time
from ShrutixMusic.utils.rich_ui import (
    rich_esc,
    rich_heading,
    rich_img,
    rich_kv_table,
    rich_note,
    rich_send,
    rich_table,
    rich_details,
    sanitize_display_name,
)
from config import BANNED_USERS
from strings import get_string

MESSAGE_EFFECTS = [
    5107584321108051014,
    5159385139981059251,
    5104841245755180586,
    5046509860389126442,
]


def _bot_link() -> str:
    username = getattr(nand, "username", None) or ""
    return f"https://t.me/{username}" if username else "https://t.me/"


def _start_photo() -> str:
    return getattr(config, "START_IMG_URL", "")


def _support_pills() -> str:
    support = getattr(config, "SUPPORT_CHAT", "")
    updates = getattr(config, "SUPPORT_CHANNEL", "")
    return (
        "<p>"
        + (f'<tg-button type="url" style="primary" url="{rich_esc(support)}">🍬 sᴜᴘᴘᴏʀᴛ ↗</tg-button> ' if support else "")
        + (f'<tg-button type="url" style="success" url="{rich_esc(updates)}">🍹 ᴜᴘᴅᴀᴛᴇs ↗</tg-button>' if updates else "")
        + "</p>"
    )


def _start_rich(uid: int, name: str) -> str:
    bot_name = rich_esc(getattr(nand, "name", "ShrutixMusic"))
    photo = _start_photo()
    return (
        rich_img(photo)
        + rich_note(
            f"<p>❍ ʜᴇʏ <a href=\"tg://user?id={uid}\">{rich_esc(name)}</a>, ᴡᴇʟᴄᴏᴍᴇ ᴀʙᴏᴀʀᴅ! 🎶</p>"
            f"<p>ɪ ᴀᴍ <b>{bot_name}</b> — ᴀ ғᴀsᴛ &amp; ᴘᴏᴡᴇʀғᴜʟ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs.</p>"
        )
        + rich_details(
            "✦ ᴋᴇʏ ғᴇᴀᴛᴜʀᴇs ✦",
            rich_table(
                ["ғᴇᴀᴛᴜʀᴇ", "ᴅᴇᴛᴀɪʟs"],
                [
                    ("🎵 sᴛʀᴇᴀᴍɪɴɢ", "ᴘʟᴀʏ ᴀᴜᴅɪᴏ &amp; ᴠɪᴅᴇᴏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs"),
                    ("🔁 ᴀᴜᴛᴏᴘʟᴀʏ", "ᴋᴇᴇᴘs ᴛʜᴇ ǫᴜᴇᴜᴇ ɢᴏɪɴɢ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ"),
                    ("🎚️ ᴇғғᴇᴄᴛs", "sᴘᴇᴇᴅ ᴄᴏɴᴛʀᴏʟ &amp; ʙᴀss ʙᴏᴏsᴛ"),
                    ("🛡️ ᴍᴏᴅᴇʀᴀᴛɪᴏɴ", "ᴄʜᴀᴛ ᴀɴᴅ ᴜsᴇʀ ᴄᴏɴᴛʀᴏʟs"),
                ],
            ),
            open=True,
        )
        + rich_details(
            "✧ ᴡʜʏ ᴄʜᴏᴏsᴇ ɪᴛ? ✧",
            "<p>⭐ sɪᴍᴘʟᴇ sʟᴀsʜ ᴄᴏᴍᴍᴀɴᴅs, ɴᴏ sᴇᴛᴜᴘ ɴᴇᴇᴅᴇᴅ.</p>"
            "<p>🎧 ᴄʟᴇᴀɴ, ʟᴏᴡ-ʟᴀɢ sᴛʀᴇᴀᴍɪɴɢ.</p>"
            "<p>❍ ᴄʟɪᴄᴋ ʜᴇʟᴘ ʙᴇʟᴏᴡ ғᴏʀ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs.</p>",
            open=True,
        )
        + rich_note(f"ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <b>{bot_name}</b>")
        + _support_pills()
    )


def _start_keyboard() -> InlineKeyboardMarkup:
    owner = getattr(config, "OWNER_ID", 0)
    support = getattr(config, "SUPPORT_CHAT", "")
    updates = getattr(config, "SUPPORT_CHANNEL", "")
    buttons = [
        [InlineKeyboardButton("⛩️ ᴧᴅᴅ мᴇ ʙᴧʙʏ ⛩️", url=f"{_bot_link()}?startgroup=true", style=enums.ButtonStyle.PRIMARY)],
    ]
    row = []
    if support:
        row.append(InlineKeyboardButton("🍬 sᴜᴘᴘᴏʀᴛ 🍬", url=support, style=enums.ButtonStyle.SUCCESS))
    if updates:
        row.append(InlineKeyboardButton("🍹 ᴜᴘᴅᴀᴛᴇs 🍹", url=updates, style=enums.ButtonStyle.SUCCESS))
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("🏩 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs 🏩", callback_data="show_help", style=enums.ButtonStyle.PRIMARY)])
    buttons.append([
        InlineKeyboardButton("🫧 ᴏᴡɴᴇʀ 🫧", user_id=owner, style=enums.ButtonStyle.DEFAULT),
        InlineKeyboardButton("🍡 sᴏᴜʀᴄᴇ 🍡", url=getattr(config, "UPSTREAM_REPO", "https://github.com/NoxxOP/ShrutixMusic"), style=enums.ButtonStyle.DEFAULT),
    ])
    return InlineKeyboardMarkup(buttons)


@nand.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    name_arg = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else ""
    if name_arg.startswith("help"):
        from ShrutixMusic.plugins.bot.help import send_help_menu
        return await send_help_menu(message, delete_command=False)
    if name_arg.startswith("sud"):
        await sudoers_list(client=client, message=message, _=_)
        if await is_on_off(2):
            await nand.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>",
            )
        return
    if name_arg.startswith("inf"):
        m = await message.reply_text("🔎")
        query = name_arg.replace("info_", "", 1)
        results = VideosSearch(f"https://www.youtube.com/watch?v={query}", limit=1)
        result = (await results.next())["result"]
        if not result:
            return await m.edit_text("❌ No result found.")
        item = result[0]
        key = InlineKeyboardMarkup([[InlineKeyboardButton("ʏᴏᴜᴛᴜʙᴇ 🎄", url=item["link"]), InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT)]])
        await m.delete()
        return await nand.send_photo(chat_id=message.chat.id, photo=item["thumbnails"][0]["url"].split("?")[0], caption=_['start_6'].format(item['title'], item['duration'], item['viewCount']['short'], item['publishedTime'], item['channel']['link'], item['channel']['name'], nand.mention), reply_markup=key)

    name = sanitize_display_name(message.from_user.first_name)
    try:
        await message.delete()
    except Exception:
        pass
    try:
        await rich_send(nand, message.chat.id, _start_rich(message.from_user.id, name), reply_markup=_start_keyboard(), effect_id=random.choice(MESSAGE_EFFECTS))
    except FloodWait as fw:
        await asyncio.sleep(fw.value + 1)
        await rich_send(nand, message.chat.id, _start_rich(message.from_user.id, name), reply_markup=_start_keyboard())

    if await is_on_off(2):
        await nand.send_message(chat_id=config.LOGGER_ID, text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>")


@nand.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    name = sanitize_display_name(message.from_user.first_name)
    chat_title = rich_esc(message.chat.title or "this chat")
    caption = (
        rich_img(_start_photo())
        + rich_note(f"❍ ʜᴇʏ <a href=\"tg://user?id={message.from_user.id}\">{rich_esc(name)}</a>, ᴛʜɪs ɪs <b>{rich_esc(nand.name)}</b>.")
        + rich_note(f"ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ {chat_title}. ʏᴏᴜ ᴄᴀɴ ɴᴏᴡ ᴘʟᴀʏ sᴏɴɢs ʜᴇʀᴇ.")
        + _support_pills()
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("⛩️ ᴧᴅᴅ мᴇ ʙᴧʙʏ ⛩️", url=f"{_bot_link()}?startgroup=true", style=enums.ButtonStyle.PRIMARY)],
        [InlineKeyboardButton("🏩 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs 🏩", callback_data="show_help", style=enums.ButtonStyle.PRIMARY)],
    ])
    await rich_send(nand, message.chat.id, caption, reply_markup=kb)
    await add_served_chat(message.chat.id)


@nand.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except Exception:
                    pass
            if member.id == nand.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await nand.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(_["start_5"].format(nand.mention, f"https://t.me/{nand.username}?start=sudolist", config.SUPPORT_CHAT), disable_web_page_preview=True)
                    return await nand.leave_chat(message.chat.id)
                caption = rich_img(_start_photo()) + rich_note(f"❍ ʜᴇʏ {rich_esc(message.from_user.first_name)}, ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴀᴅᴅɪɴɢ <b>{rich_esc(nand.name)}</b> ᴛᴏ <b>{rich_esc(message.chat.title)}</b>.") + _support_pills()
                kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏩 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs 🏩", callback_data="show_help", style=enums.ButtonStyle.PRIMARY)]])
                await rich_send(nand, message.chat.id, caption, reply_markup=kb)
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
