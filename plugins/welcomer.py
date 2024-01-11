from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions

from asSQL import Client as cl
from .is_admin import admin,add_msg,owner
data = cl("protect")
db = data['data']
@app.on_chat_member_updated()
@app.on_message(filters.new_chat_members)
def welcome(app,message):
    chat_id = message.chat.id
    m = message.from_user.mention
    km = f"""
لا تُسِئ اللفظ وإن ضَاق عليك الرَّد

ɴᴀᴍᴇ ⌯ ⁪⁬⁪⁬{m}
𝖣𝖺𝗍𝖾 ⌯ {message.date}
"""
    k = db.get(f"group_{message.chat.id}_welcome")
    if db.get(f"lock_welcome_{message.chat.id}") == False:
        if k == None:
            app.send_message(chat_id,km)
        else:
            kc = db.get(f"group_{message.chat.id}_welcome")
            message.reply(chat_id,kc)
