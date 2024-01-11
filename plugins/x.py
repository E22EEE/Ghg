from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions

from asSQL import Client as cl
from .is_admin import admin,add_msg,owner
data = cl("protect")
db = data['data']
@app.on_message(filters.media  & filters.group, group = 92)
def handle_messages(app, message):
    
    if db.get(f"new_reply_{message.chat.id}_{message.from_user.id}"):
        if message.video :
            
            old = db.get(f"group_{message.chat.id}_replies")
            rd = db.get(f"new_reply_{message.chat.id}_{message.from_user.id}")
            caption = None
            if message.caption:
                caption = message.caption
                d = {f"{rd}":{"by":message.from_user.id,"date":f"{message.date}","file":message.video.file_id,"caption":caption,"type":"video"}}
                old.append(d)
                db.set(f"group_{message.chat.id}_replies",old)
                db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
                return message.reply(f"الرد {rd} نضاف.")
            else:
                d = {f"{rd}":{"by":message.from_user.id,"date":f"{message.date}","file":message.video.file_id,"caption":caption,"type":"video"}}
                old.append(d)
                db.set(f"group_{message.chat.id}_replies",old)
                db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
                return message.reply(f"الرد {rd} نضاف.")
        if message.photo:
            old = db.get(f"group_{message.chat.id}_replies")
            rd = db.get(f"new_reply_{message.chat.id}_{message.from_user.id}")
            caption = None
            if message.caption:
                caption = message.caption
                d = {f"{rd}":{"by":message.from_user.id,"date":f"{message.date}","file":message.photo.file_id,"caption":caption,"type":"photo"}}
                old.append(d)
                db.set(f"group_{message.chat.id}_replies",old)
                db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
                return message.reply(f"الرد {rd} نضاف.")
            else:
                d = {f"{rd}":{"by":message.from_user.id,"date":f"{message.date}","file":message.photo.file_id,"caption":None,"type":"photo"}}
                old.append(d)
                db.set(f"group_{message.chat.id}_replies",old)
                db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
                return message.reply(f"الرد {rd} نضاف.")
        if message.audio:
            old = db.get(f"group_{message.chat.id}_replies")
            rd = db.get(f"new_reply_{message.chat.id}_{message.from_user.id}")
            caption = None
            if message.caption:
                caption = message.caption
                d = {f"{rd}":{"by":message.from_user.id,"date":f"{message.date}","file":message.audio.file_id,"caption":caption,"type":"audio"}}
                old.append(d)
                db.set(f"group_{message.chat.id}_replies",old)
            
                db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
                return message.reply(f"الرد {rd} نضاف.")
            else:
                d = {f"{rd}":{"by":message.from_user.id,"date":f"{message.date}","file":message.audio.file_id,"caption":caption,"type":"audio"}}
                old.append(d)
                db.set(f"group_{message.chat.id}_replies",old)
                db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
                return message.reply(f"الرد {rd} نضاف.")
        if message.document:
            old = db.get(f"group_{message.chat.id}_replies")
            rd = db.get(f"new_reply_{message.chat.id}_{message.from_user.id}")
            caption = None
            if message.caption:
                caption = message.caption
                d = {f"{rd}":{"by":message.from_user.id,"date":f"{message.date}","file":message.document.file_id,"caption":caption,"type":"document"}}
                old.append(d)
                db.set(f"group_{message.chat.id}_replies",old)
                db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
                return message.reply(f"الرد {rd} نضاف.")
            else:
                d = {f"{rd}":{"by":message.from_user.id,"date":f"{message.date}","file":message.document.file_id,"caption":caption,"type":"document"}}
                old.append(d)
                db.set(f"group_{message.chat.id}_replies",old)
                db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
                return message.reply(f"الرد {rd} نضاف.")
        
        
        if message.voice:
            old = db.get(f"group_{message.chat.id}_replies")
            rd = db.get(f"new_reply_{message.chat.id}_{message.from_user.id}")
            caption = None
            if message.caption:
                caption = message.caption
                d = {f"{rd}":{"by":message.from_user.id,"date":f"{message.date}","file":message.voice.file_id,"caption":caption,"type":"voice"}}
                old.append(d)
                db.set(f"group_{message.chat.id}_replies",old)
                db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
                return message.reply(f"الرد {rd} نضاف.")
            else:
                d = {f"{rd}":{"by":message.from_user.id,"date":f"{message.date}","file":message.voice.file_id,"caption":None,"type":"voice"}}
                old.append(d)
                db.set(f"group_{message.chat.id}_replies",old)
                db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
                return message.reply(f"الرد {rd} نضاف.")
        if message.animation:
            old = db.get(f"group_{message.chat.id}_replies")
            rd = db.get(f"new_reply_{message.chat.id}_{message.from_user.id}")
            caption = None
            if message.caption:
                caption = message.caption
                d = {f"{rd}":{"by":message.from_user.id,"date":f"{message.date}","file":message.animation.file_id,"caption":caption,"type":"animation"}}
                old.append(d)
                db.set(f"group_{message.chat.id}_replies",old)
                db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
                return message.reply(f"الرد {rd} نضاف.")
            else:
                d = {f"{rd}":{"by":message.from_user.id,"date":f"{message.date}","file":message.animation.file_id,"caption":None,"type":"animation"}}
                old.append(d)
                db.set(f"group_{message.chat.id}_replies",old)
                db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
                return message.reply(f"الرد {rd} نضاف.")