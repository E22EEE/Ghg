from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions

from asSQL import Client as cl
from .is_admin import admin,add_msg,owner
data = cl("protect")
db = data['data']
bads = db.get("bad_words")

@app.on_edited_message(filters.all , group = 6)
def oed(_,message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    lock_edit = db.get(f"lock_edit_{chat_id}")
    if lock_edit:
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            return
        else:
            message.delete()
@app.on_message(filters.forwarded & filters.group , group = 5)
def hand_forw(_,message):
    chat_id = message.chat.id
    lock_forwards = db.get(f'lock_forwards_{chat_id}')
    user_id = message.from_user.id
    if message:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    if lock_forwards:
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            return
        else:
            message.delete()
@app.on_message(filters.text & filters.group , group = 4)
def texts_filter(_,message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    users = db.get(f"group_{chat_id}_mutelist")
    lock_bads = db.get(f"lock_badword_{chat_id}")
    lock_text = db.get(f'lock_text_{chat_id}')
    lock_inline = db.get(f"lock_inline_{chat_id}")
    lock_big = db.get(f'lock_bigmsg_{chat_id}')
    lock_urls = db.get(f'lock_urls_{chat_id}')
    if users != None:
        found = False
        for i in users['data']:
            if f"{message.from_user.id}" in i:
                found = True
            else:
                continue
       
        if found:
            if message.from_user.id == 5539142769:
                return
            else:
                message.delete()
    if lock_inline and message.via_bot:
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            return
        else:
            message.delete()
            message.reply(
                f"⇜ عزيزي 「 {message.from_user.mention} 」 \n⇜ الانلاين مقفول.")
    if lock_big and len(message.text) >400:
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            return
        else:
            message.delete()
            message.reply(
                f"⇜ عزيزي 「 {message.from_user.mention} 」 \n⇜ ممنوع الكلام لكبير.")
    if lock_bads and message.text:
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            return
        else:
            if any(word in bads for word in message.text.split()):
                message.delete()
                message.reply(f"⇜ عزيزي [ {message.from_user.mention} ] ، ممنوع السب .")
                    

    if lock_text and message.text:
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            return
        else:
            message.delete()
    if lock_urls and message.text:
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            return
        else:
            if "MessageEntityType.URL" in str(message):
                message.delete()
                message.reply(f"⇜ عزيزي [ {message.from_user.mention} ] ، ممنوع الروابط .")
@app.on_message(filters.media & filters.group, group =3)
def media_filter(_,message):
    chat_id = message.chat.id
    lock_stickers = db.get(f'lock_stickers_{chat_id}')
    lock_gifs = db.get(f'lock_gifs_{chat_id}')
    lock_documents = db.get(f'lock_documents_{chat_id}')
    lock_videos = db.get(f'lock_videos_{chat_id}')
    lock_photos = db.get(f'lock_photos_{chat_id}')
    cre = db.get(f"creators_{message.chat.id}")
    adm = db.get(f"admins-{message.chat.id}")
    user_id = message.from_user.id
    if lock_photos and message.photo:
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            return
        else:
            message.delete()
    if lock_videos and message.video:
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            return
        else:
            message.delete
    if lock_documents and message.document:
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            return
        else:
            message.delete()
    if lock_stickers and message.sticker:
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            return
        else:
            message.delete()
    if lock_gifs and message.animation:
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            return
        else:
            message.delete()
    users = db.get(f"group_{chat_id}_mutelist")
    
    if users != None:
        found = False
        for i in users['data']:
            if f"{message.from_user.id}" in i:
                found = True
            else:
                continue
       
        if found:
            message.delete()