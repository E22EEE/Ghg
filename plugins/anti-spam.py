from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions
import time,random
import pyrogram
from asSQL import Client as cl
from .is_admin import admin,add_msg,owner
data = cl("protect")
db = data['data']
@app.on_message(filters.all & filters.group , group = 30)
def handle_messages(app, message):
    chat_id = str(message.chat.id)
    
    
    if message:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            if db.get(f"group_{message.chat.id}_flood"):
                pass
            else:
                db.set(f"group_{message.chat.id}_flood",5)
        
        else:
            return
    if message.sender_chat:
        return   
    t = ((time.time()))
    much_of = db.get(f"group_{message.chat.id}_flood")
    times = db.get(f"user_{chat_id}_{message.from_user.id}_msgs")
    db.push(f"user_{chat_id}_{message.from_user.id}_msgs",t)
    if db.get(f"lock_flood_{chat_id}"):
        if not owner(message.from_user.id,message.chat.id) and not admin(message.from_user.id,message.chat.id):
            if len(times)>=int(much_of):
                if times[-1] - times[0] <= 4:
                    c = 5*2
                    for i in range(message.id,message.id-int(much_of)*3,-1):
                        try:
                            m = app.get_messages(chat_id,i)
                            if m:
                                if m.from_user.id == message.from_user.id:
                                    app.restrict_chat_member(chat_id,m.from_user.id,ChatPermissions())
                                    app.delete_messages(chat_id,i)
                                else:
                                    pass
                            else:
                                pass
                        except:
                            continue
                    db.delete(f"user_{chat_id}_{message.from_user.id}_msgs")
                    db.set(f"user_{chat_id}_{message.from_user.id}_msgs",[t])
                    return message.reply(f"سبام ها {message.from_user.mention} ?")
                    
                else:
                    db.delete(f"user_{chat_id}_{message.from_user.id}_msgs")
                    db.set(f"user_{chat_id}_{message.from_user.id}_msgs",[t])
    else:
        pass