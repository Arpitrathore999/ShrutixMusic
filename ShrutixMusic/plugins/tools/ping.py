import random
from datetime import datetime

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from ShrutixMusic import nand
from ShrutixMusic.core.call import Shruti
from ShrutixMusic.utils import bot_sys_stats
from ShrutixMusic.utils.decorators.language import language
from ShrutixMusic.utils.rich_ui import (
    rich_esc,
    rich_heading,
    rich_img,
    rich_kv_table,
    rich_send,
)
from config import BANNED_USERS, PING_IMG_URL, SUPPORT_CHAT

MESSAGE_EFFECTS = [
    5107584321108051014,
    5159385139981059251,
    5104841245755180586,
    5046509860389126442,
]


def supp_markup():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="🍬 sᴜᴘᴘᴏʀᴛ 🍬", url=SUPPORT_CHAT)]]
    )


@nand.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    chat_id = message.chat.id
    start = datetime.now()
    is_private = message.chat.type == ChatType.PRIVATE
    effect_id = random.choice(MESSAGE_EFFECTS) if is_private else None

    # Rich temporary ping message, matching the Outlaw-style flow.
    response = await rich_send(
        client,
        chat_id,
        rich_heading(
            f"❍ {rich_esc(client.me.first_name)} ɪs ᴘɪɴɢɪɴɢ...",
            level=3,
        ),
        effect_id=effect_id,
    )

    pytgping = await Shruti.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000

    try:
        await response.delete()
    except Exception:
        pass

    caption = (
        rich_heading(f"🏓 ᴘᴏɴɢ : {resp:.0f}ms", level=3)
        + rich_img(PING_IMG_URL)
        + rich_kv_table(
            [
                ("ᴜᴘᴛɪᴍᴇ", f"<code>{rich_esc(UP)}</code>"),
                ("ʀᴀᴍ", f"<code>{rich_esc(RAM)}</code>"),
                ("ᴄᴘᴜ", f"<code>{rich_esc(CPU)}</code>"),
                ("ᴅɪsᴋ", f"<code>{rich_esc(DISK)}</code>"),
                ("ᴘʏᴛɢᴄ", f"<code>{rich_esc(pytgping)}ms</code>"),
            ],
            headers=["sʏsᴛᴇᴍ sᴛᴀᴛs", ""],
        )
        + f'<p>❍ ʙʏ » <a href="{SUPPORT_CHAT}">sʜʀᴜᴛɪx ꭙ ᴍᴜsɪᴄ</a></p>'
    )

    await rich_send(
        client,
        chat_id,
        caption,
        reply_markup=supp_markup(),
        effect_id=effect_id,
    )
