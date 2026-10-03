import random
import time

from pyrogram import filters
from pyrogram.enums import ButtonStyle, ChatType
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
from ShrutixMusic.utils.inline import start_panel
from ShrutixMusic.utils.rich_ui import (
    rich_details,
    rich_esc,
    rich_img,
    rich_note,
    rich_send,
    rich_table,
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


def _buttons():
    bot_link = f"https://t.me/{nand.username}"
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⛩️ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ⛩️",
                    url=f"{bot_link}?startgroup=true",
                    style=ButtonStyle.PRIMARY,
                )
            ],
            [
                InlineKeyboardButton(
                    "🍬 sᴜᴘᴘᴏʀᴛ 🍬", url=config.SUPPORT_CHAT, style=ButtonStyle.SUCCESS
                ),
                InlineKeyboardButton(
                    "🍹 ᴜᴘᴅᴀᴛᴇs 🍹", url=config.SUPPORT_CHANNEL, style=ButtonStyle.SUCCESS
                ),
            ],
            [
                InlineKeyboardButton(
                    "🏩 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs 🏩",
                    callback_data="settings_back_helper",
                    style=ButtonStyle.PRIMARY,
                )
            ],
            [
                InlineKeyboardButton(
                    "🫧 ᴏᴡɴᴇʀ 🫧",
                    user_id=config.OWNER_ID,
                    style=ButtonStyle.DEFAULT,
                ),
                InlineKeyboardButton(
                    "🍡 sᴏᴜʀᴄᴇ 🍡",
                    url=config.UPSTREAM_REPO,
                    style=ButtonStyle.DEFAULT,
                ),
            ],
        ]
    )


def _rich_start(user, photo):
    name = sanitize_display_name(user.first_name)
    uid = user.id
    return (
        rich_img(photo)
        + rich_note(
            f"<p>❍ ʜᴇʏ <a href=\"tg://user?id={uid}\">{rich_esc(name)}</a>, "
            "ᴡᴇʟᴄᴏᴍᴇ ᴀʙᴏᴀʀᴅ! 🎶</p>"
            f"<p>ɪ ᴀᴍ <b>{rich_esc(nand.mention)}</b> — ᴀ ғᴀsᴛ &amp; ᴘᴏᴡᴇʀғᴜʟ "
            "ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs.</p>"
        )
        + rich_details(
            "✦ ᴋᴇʏ ғᴇᴀᴛᴜʀᴇs ✦",
            rich_table(
                ["ғᴇᴀᴛᴜʀᴇ", "ᴅᴇᴛᴀɪʟs"],
                [
                    ("🎵 sᴛʀᴇᴀᴍɪɴɢ", "ᴘʟᴀʏ ᴀᴜᴅɪᴏ &amp; ᴠɪᴅᴇᴏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs"),
                    ("🔁 ᴀᴜᴛᴏᴘʟᴀʏ", "ᴋᴇᴇᴘs ᴛʜᴇ ǫᴜᴇᴜᴇ ɢᴏɪɴɢ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ"),
                    ("🎚️ ᴇғғᴇᴄᴛs", "sᴘᴇᴇᴅ ᴄᴏɴᴛʀᴏʟ &amp; ʙᴀss ʙᴏᴏsᴛ"),
                    ("🛡️ ᴍᴏᴅᴇʀᴀᴛɪᴏɴ", "ʙʟᴏᴄᴋ/ᴜɴʙʟᴏᴄᴋ ᴄʜᴀᴛs &amp; ᴜsᴇʀs"),
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
        + rich_note(
            f'ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href="{rich_esc(config.UPSTREAM_REPO)}">sʜʀᴜᴛɪx ꭙ ᴍᴜsɪᴄ</a>'
        )
        + "<p>"
        + f'<tg-button url="{rich_esc(config.SUPPORT_CHAT)}" style="primary">🍬 sᴜᴘᴘᴏʀᴛ ↗</tg-button> '
        + f'<tg-button url="{rich_esc(config.SUPPORT_CHANNEL)}" style="success">🍹 ᴜᴘᴅᴀᴛᴇs ↗</tg-button>'
        + "</p>"
    )


@nand.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    effect_id = random.choice(MESSAGE_EFFECTS)
    name = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else ""

    if name.startswith("help"):
        # Let the real help handler render the Rich UI.
        from ShrutixMusic.plugins.bot.help import send_help_message
        return await send_help_message(message, effect_id=effect_id)

    if name.startswith("sud"):
        await sudoers_list(client=client, message=message, _=_)
        if await is_on_off(2):
            return await nand.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )
        return

    if name.startswith("inf"):
        m = await message.reply_text("🔎")
        query = str(name).replace("info_", "", 1)
        results = VideosSearch(f"https://www.youtube.com/watch?v={query}", limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration = result["duration"]
            views = result["viewCount"]["short"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            channellink = result["channel"]["link"]
            channel = result["channel"]["name"]
            link = result["link"]
            published = result["publishedTime"]
        searched_text = _["start_6"].format(title, duration, views, published, channellink, channel, nand.mention)
        key = InlineKeyboardMarkup([[InlineKeyboardButton(text=_["S_B_8"], url=link), InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT)]])
        await m.delete()
        await nand.send_photo(chat_id=message.chat.id, photo=thumbnail, caption=searched_text, reply_markup=key)
        return

    await rich_send(client, message.chat.id, _rich_start(message.from_user, config.START_IMG_URL), reply_markup=_buttons(), effect_id=effect_id)
    if await is_on_off(2):
        await nand.send_message(
            chat_id=config.LOGGER_ID,
            text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
        )


@nand.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(nand.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


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
                    await message.reply_text(
                        _["start_5"].format(
                            nand.mention,
                            f"https://t.me/{nand.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await nand.leave_chat(message.chat.id)
                out = start_panel(_)
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        nand.mention,
                        message.chat.title,
                        nand.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
