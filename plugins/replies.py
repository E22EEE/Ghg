from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions

from asSQL import Client as cl
from .is_admin import admin,add_msg,owner
data = cl("protect")
db = data['data']
@app.on_message(filters.text & filters.group , group = 8)
def handle_messages(app, message):
    
    chat_id = str(message.chat.id)
    text = message.text
    if text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    
    if message.sender_chat:
        return
    if text  == "تعطيل":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            db.delete(f'group_{message.chat.id}')
            message.reply(f"""
    ↤من 「 {message.from_user.mention} 」 
    ↤ابشر عطلت المجموعة
    ༄
                """)
@app.on_message(filters.text & filters.group , group = 9)
def r(app,message):
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text
    if text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    
    
    if db.get(f"group_{message.chat.id}_custom_{text}"):
        text = db.get(f"group_{message.chat.id}_custom_{text}")
    