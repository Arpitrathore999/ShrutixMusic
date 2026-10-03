"""Rich-message attempt with a visible, standard Telegram fallback."""
import logging
log = logging.getLogger(__name__)

async def send_panel(client, message, rich_html, plain_html, keyboard, photo=None):
    sender = getattr(client, "send_rich_message", None)
    if callable(sender):
        try:
            from pyrogram.types import InputRichMessage
            return await sender(chat_id=message.chat.id, rich_message=InputRichMessage(rich_html), reply_markup=keyboard)
        except Exception as exc:
            log.warning("Rich panel unavailable; using styled HTML fallback: %s", exc)
    if photo:
        return await message.reply_photo(photo=photo, caption=plain_html[:1024], reply_markup=keyboard)
    return await message.reply_text(plain_html, reply_markup=keyboard, disable_web_page_preview=True)

START_RICH = """<h2>✦ WELCOME TO SHRUTIX MUSIC ✦</h2><blockquote>🎶 A powerful Telegram voice-chat music player.</blockquote><details open><summary>✦ KEY FEATURES ✦</summary><table><tr><th>FEATURE</th><th>DETAILS</th></tr><tr><td>🎵 STREAMING</td><td>Audio and video</td></tr><tr><td>🔁 AUTOPLAY</td><td>Continuous queue</td></tr><tr><td>🎚️ CONTROLS</td><td>Pause, skip, speed</td></tr></table></details><details><summary>✧ WHY CHOOSE IT? ✧</summary><p>Easy commands and group playback.</p></details><p>✦ SUPPORT • UPDATES • HELP ✦</p>"""
START_PLAIN = """✦ <b>WELCOME TO SHRUTIX MUSIC</b> ✦

🎶 A powerful Telegram voice-chat music player.

<b>✦ KEY FEATURES ✦</b>
┌ 🎵 <b>STREAMING</b> — Audio &amp; video
├ 🔁 <b>AUTOPLAY</b> — Continuous queue
└ 🎚️ <b>CONTROLS</b> — Pause, skip &amp; speed

<b>✧ WHY CHOOSE IT? ✧</b>
Easy commands and group playback.

✦ <b>SUPPORT • UPDATES • HELP</b> ✦"""
HELP_RICH = """<h2>✦ HELP &amp; COMMANDS ✦</h2><blockquote>Choose a category below to explore music and admin commands.</blockquote><details open><summary>✦ QUICK START ✦</summary><table><tr><th>COMMAND</th><th>USE</th></tr><tr><td>/play</td><td>Play a song</td></tr><tr><td>/pause</td><td>Pause music</td></tr><tr><td>/resume</td><td>Resume music</td></tr><tr><td>/skip</td><td>Next track</td></tr></table></details>"""
HELP_PLAIN = """✦ <b>HELP &amp; COMMANDS</b> ✦

Choose a category using the buttons below.

<b>✦ QUICK START ✦</b>
🎵 /play — Play a song
⏸ /pause — Pause music
▶️ /resume — Resume music
⏭ /skip — Next track"""
