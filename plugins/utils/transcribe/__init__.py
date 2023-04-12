# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

""" speech to text """

from pyrogram import Client
from pyrogram.errors import BadRequest
from pyrogram.types import Message 
from pyrogram.raw import functions, types


async def transcribe_message(message: Message) -> str | None:
    """Transcribes a voice message or a video note.
    Returns `None` if the message cannot be transcribed, `transcription_id` as an integer
    if the transcription is pending, or the transcribed text as a string if it's ready.
    """
    try:
        transcribed: types.messages.TranscribedAudio = await userge.invoke(
            functions.messages.TranscribeAudio(
                peer=await userge.resolve_peer(message.chat.id),
                msg_id=message.id,
            )
        )
    except BadRequest as e:
        if isinstance(e.value, str) and "TRANSCRIPTION_FAILED" in e.value:
            return None
        raise
    return transcribed.text