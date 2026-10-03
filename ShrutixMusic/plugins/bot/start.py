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
    rich_edit,
    rich_esc,
    rich_heading,
    rich_img,
    rich_kv_table,
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


def _support_url():
    return getattr(config, "SUPPORT_CHAT", "")


def _updates_url():
    return getattr(config, "SUPPORT_CHANNEL", _support_url())


def _bot_username():
    username = getattr(nand, "username", None)
    return username or getattr(config, "BOT_USERNAME", "ShrutixMusic")


def _start_keyboard():
    bot_url = f"https://t.me/{_bot_username()}?startgroup=true"
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⛩️ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ⛩️",
                    url=bot_url,
                    style=enums.ButtonStyle.PRIMARY,
                )
            ],
            [
                InlineKeyboardButton(
                    "🍬 sᴜᴘᴘᴏʀᴛ 🍬",
                    url=_support_url(),
                    style=enums.ButtonStyle.SUCCESS,
                ),
                InlineKeyboardButton(
                    "🍹 ᴜᴘᴅᴀᴛᴇs 🍹",
                    url=_updates_url(),
                    style=enums.ButtonStyle.SUCCESS,
                ),
            ],
            [
                InlineKeyboardButton(
                    "🏩 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs 🏩",
                    callback_data="rich_help_menu",
                    style=enums.ButtonStyle.PRIMARY,
                )
            ],
            [
                InlineKeyboardButton(
                    "🫧 ᴏᴡɴᴇʀ 🫧",
                    user_id=config.OWNER_ID,
                    style=enums.ButtonStyle.DEFAULT,
                ),
                InlineKeyboardButton(
                    "🍡 sᴏᴜʀᴄᴇ 🍡",
                    url=getattr(config, "UPSTREAM_REPO", "https://github.com/NoxxOP/ShrutixMusic"),
                    style=enums.ButtonStyle.DEFAULT,
                ),
            ],
        ]
    )


def _rich_start(uid: int, name: str):
    name = sanitize_display_name(name)
    bot_name = getattr(config, "BOT_NAME", None) or "ShrutixMusic"

    return (
        # Screenshot-style order: image -> welcome note -> expandable feature table
        rich_img(config.START_IMG_URL)
        + rich_note(
            f"<p>❍ ʜᴇʏ <a href='tg://user?id={uid}'>{rich_esc(name)}</a>, ᴡᴇʟᴄᴏᴍᴇ ᴀʙᴏᴀʀᴅ! 🎶</p>"
            f"<p>ɪ ᴀᴍ <b>{rich_esc(bot_name)}</b> — ᴀ ғᴀsᴛ &amp; ᴘᴏᴡᴇʀғᴜʟ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs.</p>"
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
            f"ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='{_updates_url()}'>sʜʀᴜᴛɪx ꭙ ᴍᴜsɪᴄ</a>"
        )
        + f"<p>{_support_url() and f'<a href=\"{_support_url()}\">🍬 sᴜᴘᴘᴏʀᴛ</a>' or ''}"
        + f" {_updates_url() and f'<a href=\"{_updates_url()}\">🍹 ᴜᴘᴅᴀᴛᴇs</a>' or ''}</p>"
    )


@nand.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    argument = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else ""

    # Keep the original deep-link features working.
    if argument.startswith("help"):
        keyboard = __import__(
            "ShrutixMusic.utils.inline", fromlist=["help_pannel"]
        ).help_pannel(_)
        return await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["help_1"].format(config.SUPPORT_CHAT),
            reply_markup=keyboard,
            effect_id=random.choice(MESSAGE_EFFECTS),
        )

    if argument.startswith("sud"):
        await sudoers_list(client=client, message=message, _=_)
        if await is_on_off(2):
            await nand.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ "
                    f"<b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>"
                    f"\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
                ),
            )
        return

    if argument.startswith("inf"):
        m = await message.reply_text("🔎")
        query = argument.replace("info_", "", 1)
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
        key = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text=_["S_B_8"], url=link),
                InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
            ]]
        )
        await m.delete()
        return await nand.send_photo(
            chat_id=message.chat.id,
            photo=thumbnail,
            caption=_["start_6"].format(
                title, duration, views, published, channellink, channel, nand.mention
            ),
            reply_markup=key,
        )

    await rich_send(
        nand,
        message.chat.id,
        _rich_start(message.from_user.id, message.from_user.first_name),
        reply_markup=_start_keyboard(),
        effect_id=random.choice(MESSAGE_EFFECTS),
    )

    if await is_on_off(2):
        await nand.send_message(
            chat_id=config.LOGGER_ID,
            text=(
                f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"
                f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
            ),
        )


@nand.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    try:
        await rich_send(
            nand,
            message.chat.id,
            rich_img(config.START_IMG_URL)
            + rich_note(
                f"❍ ʜᴇʏ <a href='tg://user?id={message.from_user.id}'>{rich_esc(sanitize_display_name(message.from_user.first_name))}</a>, "
                f"ᴛʜɪs ɪs <b>{rich_esc(getattr(config, 'BOT_NAME', 'ShrutixMusic'))}</b> 🎶<br/>"
                f"ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ <b>{rich_esc(message.chat.title or 'this chat')}</b>."
            ),
            reply_markup=_start_keyboard(),
        )
    except Exception:
        await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["start_1"].format(
                nand.mention, get_readable_time(int(time.time() - _boot_))
            ),
            reply_markup=InlineKeyboardMarkup(start_panel(_)),
        )
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
                    await message.reply_text(
                        _["start_5"].format(
                            nand.mention,
                            f"https://t.me/{nand.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await nand.leave_chat(message.chat.id)

                await rich_send(
                    nand,
                    message.chat.id,
                    rich_img(config.START_IMG_URL)
                    + rich_note(
                        f"❍ ʜᴇʏ <a href='tg://user?id={message.from_user.id}'>{rich_esc(sanitize_display_name(message.from_user.first_name))}</a>, "
                        f"ᴛʜɪs ɪs <b>{rich_esc(getattr(config, 'BOT_NAME', 'ShrutixMusic'))}</b> 🎶<br/>"
                        f"ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ <b>{rich_esc(message.chat.title or 'this chat')}</b>.",
                    ),
                    reply_markup=_start_keyboard(),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
