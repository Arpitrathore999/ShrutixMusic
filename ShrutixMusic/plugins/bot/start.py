# --------------------------------------------------------------------------------
#  ShrutixMusic — start.py (Outlaw-style /start)
# --------------------------------------------------------------------------------

import html as _html
import random
import time

from pyrogram import enums, filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
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
from ShrutixMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

# ── Rich UI (Outlaw-style) ────────────────────────────────────────────────────
try:
    from ShrutixMusic.utils.rich_ui import (
        RICH_AVAILABLE,
        rich_send,
        rich_img,
        rich_note,
        rich_table,
        rich_details,
        rich_esc,
        rich_caption,
        sanitize_display_name,
    )
    HAS_RICH_UI = True
except ImportError:
    HAS_RICH_UI = False
    RICH_AVAILABLE = False

    def rich_esc(v):
        return _html.escape(str(v or ""), quote=False)

    def sanitize_display_name(v, max_len=64):
        return str(v or "User")[:max_len]

    def rich_caption(t):
        return t

    def rich_img(s):
        return ""

    def rich_note(t, expandable=False):
        return f"<blockquote>{t}</blockquote>"

    def rich_table(h, r, border=1):
        return ""

    def rich_details(s, b, open=False):
        return b

    async def rich_send(*a, **k):
        return None


# ── Button helper (silently drops `style=` if fork doesn't support it) ────────
def _make_btn(text, **kwargs):
    try:
        return InlineKeyboardButton(text, **kwargs)
    except TypeError:
        kwargs.pop("style", None)
        return InlineKeyboardButton(text, **kwargs)


_BTN_PRIMARY = "primary"
_BTN_SUCCESS = "success"
_BTN_DANGER  = "danger"
_BTN_DEFAULT = "default"


MESSAGE_EFFECTS = [
    5107584321108051014,
    5159385139981059251,
    5104841245755180586,
    5046509860389126442,
]


# ══════════════════════════════════════════════════════════════════════════════
#  /start (private)
# ══════════════════════════════════════════════════════════════════════════════

@nand.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    effect_id = random.choice(MESSAGE_EFFECTS)
    parts = message.text.split(None, 1)
    name = parts[1] if len(parts) > 1 else ""

    # ── /start help ──────────────────────────────────────────────────────────
    if name[0:4] == "help":
        keyboard = help_pannel(_)
        return await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["help_1"].format(config.SUPPORT_CHAT),
            reply_markup=keyboard,
            effect_id=effect_id,
        )

    # ── /start sud ───────────────────────────────────────────────────────────
    if name[0:3] == "sud":
        await sudoers_list(client=client, message=message, _=_)
        if await is_on_off(2):
            return await nand.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ "
                    f"<b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"
                    f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                    f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
                ),
            )
        return

    # ── /start info_<video_id> ───────────────────────────────────────────────
    if name[0:3] == "inf":
        m = await message.reply_text("🔎")
        query = (str(name)).replace("info_", "", 1)
        query = f"https://www.youtube.com/watch?v={query}"
        results = VideosSearch(query, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration = result["duration"]
            views = result["viewCount"]["short"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            channellink = result["channel"]["link"]
            channel = result["channel"]["name"]
            link = result["link"]
            published = result["publishedTime"]
        searched_text = _["start_6"].format(
            title, duration, views, published, channellink, channel, nand.mention
        )
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text=_["S_B_8"], url=link),
                    InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                ],
            ]
        )
        await m.delete()
        await nand.send_photo(
            chat_id=message.chat.id,
            photo=thumbnail,
            caption=searched_text,
            reply_markup=key,
        )
        if await is_on_off(2):
            await nand.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ "
                    f"<b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n"
                    f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                    f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
                ),
            )
        return

    # ══════════════════════════════════════════════════════════════════════════
    #  ✨ OUTLAW-STYLE DEFAULT /start ✨
    # ══════════════════════════════════════════════════════════════════════════

    uid       = message.from_user.id
    user_name = sanitize_display_name(message.from_user.first_name)
    bot_name  = getattr(config, "BOT_NAME", "Shrutix Music")
    support   = getattr(config, "SUPPORT_CHAT", "https://t.me/ShrutiBots")
    updates   = getattr(config, "UPDATES_CHANNEL", support)
    owner_id  = getattr(config, "OWNER_ID", 0)
    photo_url = getattr(config, "START_IMG_URL", None)

    # ── Support/Updates pills (Outlaw style) ─────────────────────────────────
    pills = (
        "<p>"
        f'<tg-button type="url" style="primary" url="{support}">'
        "🍬 sᴜᴘᴘᴏʀᴛ</tg-button> "
        f'<tg-button type="url" style="success" url="{updates}">'
        "🍹 ᴜᴘᴅᴀᴛᴇs</tg-button>"
        "</p>"
    )

    # ── Full rich caption ────────────────────────────────────────────────────
    caption = (
        (rich_img(photo_url) if photo_url else "")
        + rich_note(
            f"<p>❍ ʜᴇʏ <a href='tg://user?id={uid}'>{rich_esc(user_name)}</a>, "
            "ᴡᴇʟᴄᴏᴍᴇ ᴀʙᴏᴀʀᴅ! 🎶</p>"
            f"<p>ɪ ᴀᴍ <b>{rich_esc(bot_name)}</b> — ᴀ ғᴀsᴛ &amp; "
            "ᴘᴏᴡᴇʀғᴜʟ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ "
            "ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs.</p>"
        )
        + rich_details(
            "✦ ᴋᴇʏ ғᴇᴀᴛᴜʀᴇs ✦",
            rich_table(
                ["ғᴇᴀᴛᴜʀᴇ", "ᴅᴇᴛᴀɪʟs"],
                [
                    ("🎵 sᴛʀᴇᴀᴍɪɴɢ",   "ᴘʟᴀʏ ᴀᴜᴅɪᴏ &amp; ᴠɪᴅᴇᴏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs"),
                    ("🔁 ᴀᴜᴛᴏᴘʟᴀʏ",    "ᴋᴇᴇᴘs ᴛʜᴇ ǫᴜᴇᴜᴇ ɢᴏɪɴɢ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ"),
                    ("🎚️ ᴇғғᴇᴄᴛs",     "sᴘᴇᴇᴅ ᴄᴏɴᴛʀᴏʟ &amp; ʙᴀss ʙᴏᴏsᴛ"),
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
            "ᴘᴏᴡᴇʀᴇᴅ ʙʏ » "
            "<a href='https://t.me/YuniteCrew'>ᴏᴜᴛʟᴀᴡ 〄 ᴍᴜsɪᴄ</a>"
        )
        + pills
    )

    # ── Inline keyboard ──────────────────────────────────────────────────────
    kb = InlineKeyboardMarkup([
        [
            _make_btn(
                "⛩️ ᴧᴅᴅ мᴇ ʙᴧʙʏ ⛩️",
                url=f"https://t.me/{nand.username}?startgroup=true",
                style=_BTN_PRIMARY,
            )
        ],
        [
            _make_btn("🍬 sᴜᴘᴘᴏʀᴛ 🍬", url=support,  style=_BTN_SUCCESS),
            _make_btn("🍹 ᴜᴘᴅᴀᴛᴇs 🍹", url=updates, style=_BTN_SUCCESS),
        ],
        [
            _make_btn(
                "🏩 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs 🏩",
                callback_data="settings_back_helper",
                style=_BTN_PRIMARY,
            )
        ],
        [
            _make_btn(
                "🫧 ᴏᴡɴᴇʀ 🫧",
                url=f"tg://user?id={owner_id}",
                style=_BTN_DEFAULT,
            ),
            _make_btn(
                "🍡 sᴏᴜʀᴄᴇ 🍡",
                url="https://github.com/NoxxOP/ShrutiMusic",
                style=_BTN_DEFAULT,
            ),
        ],
    ])

    # ── Send: rich path first, photo+caption fallback ────────────────────────
    sent_ok = False
    if HAS_RICH_UI and RICH_AVAILABLE:
        try:
            await rich_send(
                nand,
                message.chat.id,
                caption,
                reply_markup=kb,
                effect_id=effect_id,
            )
            sent_ok = True
        except Exception as e:
            print(f"[start_pm] rich_send failed: {e}")

    if not sent_ok:
        fallback = rich_caption(caption) if HAS_RICH_UI else caption
        if len(fallback) > 1000:
            fallback = fallback[:1000].rstrip() + "…"
        await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=fallback,
            reply_markup=kb,
            effect_id=effect_id,
        )

    # ── Logger ───────────────────────────────────────────────────────────────
    if await is_on_off(2):
        return await nand.send_message(
            chat_id=config.LOGGER_ID,
            text=(
                f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"
                f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
            ),
        )


# ══════════════════════════════════════════════════════════════════════════════
#  /start (group)
# ══════════════════════════════════════════════════════════════════════════════

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


# ══════════════════════════════════════════════════════════════════════════════
#  Bot added to a new chat
# ══════════════════════════════════════════════════════════════════════════════

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
