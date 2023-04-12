""" speech to text """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram.errors import BadRequest

from userge import userge, Message

from . import transcribe_message

@userge.on_cmd(
    "totext",
    about={
        "header": "transcribe a file (speech to text)",
        "usage": "{tr}stt [reply to telegram video/audio note]",
    },
)
async def transcriber(msg: Message):
    """Speech to text using Telegram premium."""
    reply_msg = msg.reply_to_message
    await msg.edit("processing...")
    if not reply_msg:
        return await msg.edit_text("`Please reply to video or voice note!`")
    if not userge.me.is_premium:
        return await msg.edit_text("`This feature only for Telegram premium user..!`")
    if reply_msg.video_note is None and reply_msg.voice is None:
        return await msg.edit_text("`No voice or video note found.`")

    result = await transcribe_message(reply_msg)
    if result is None or result == "":
        return await msg.edit_text(
            "<i>Transcription failed, maybe the message has no recognizable voice?</i>"
        )
    return await msg.edit_text(f"<b>Transcribed text:</b>\n{resul}")
