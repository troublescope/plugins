from pyrogram.errors import PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import enums

from userge import userge, Message, filters, get_collection

class MentionsDB:
    def __init__(self):
        self.db = get_collection("CONFIGS")
        data = self.db.find_one({"_id": "MENTION_TOGGLE"})
        self.toggle = bool(data.get("data")) if data else False

    def update_toggle(self):
        self.toggle = not self.toggle
        self.db.update_one(
            {"_id": "MENTION_TOGGLE"}, {"$set": {"data": self.toggle}}, upsert=True
        )

    async def save_mention(self, msg: Message):
        if not self.toggle:
            return
        if not msg.from_user or msg.from_user.is_verified:
            return
        if msg.chat.type == enums.ChatType.PRIVATE:
            link = f"tg://openmessage?user_id={msg.chat.id}&message_id={msg.id}"
            text = f"{msg.from_user.mention} 💻 sent you a **Private message.**"
        else:
            link = msg.link
            text = f"{msg.from_user.mention} 💻 tagged you in **{msg.chat.title}.**"
        text += f"\n\n[Message]({link}):" if not userge.has_bot else "\n\n**Message:**"
        if msg.text:
            text += f"\n`{msg.text}`"
        button = InlineKeyboardButton(text="📃 Message Link", url=link)
        client = userge.bot if userge.has_bot else userge
        try:
            await client.send_message(
                chat_id=userge.id if userge.has_bot else config.LOG_CHANNEL_ID,
                text=text,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[button]])
            )
            if not msg.text:
                await client.copy_message(
                    userge.id if userge.has_bot else config.LOG_CHANNEL_ID,
                    msg.chat.id,
                    msg.id
                )
        except PeerIdInvalid:
            if userge.dual_mode:
                await userge.send_message(userge.id, "/start")
                await client.send_message(
                    chat_id=userge.id if userge.has_bot else config.LOG_CHANNEL_ID,
                    text=text,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([[button]])
                )
                if not msg.text:
                    await client.copy_message(
                        userge.id if userge.has_bot else config.LOG_CHANNEL_ID,
                        msg.chat.id,
                        msg.id
                    )
            else:
                raise

    async def get_toggle_text(self):
        return f"Mentions Alerter **{'enabled' if self.toggle else 'disabled'}** Successfully."


MENTIONS_DB = MentionsDB()

@userge.on_cmd(
    "mentions",
    about="Toggles Mentions, "
          "if enabled Bot will send Message if anyone mention you."
)
async def toggle_mentions(msg: Message):
    """ toggle mentions """
    await MENTIONS_DB.update_toggle()
    toggle_text = await MENTIONS_DB.get_toggle_text()
    await msg.edit(toggle_text)


@userge.on_filters(
    ~filters.me & ~filters.bot & ~filters.service
    & (filters.mentioned | filters.private), group=1, allow_via_bot=False)
async def handle_mentions(msg: Message):
    await MENTIONS_DB.save_mention(msg)
