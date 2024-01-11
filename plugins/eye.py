from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions

from asSQL import Client as cl
from .is_admin import owner,admin,add_msg
data = cl("protect")
db = data['data']
@app.on_message(filters.left_chat_member)
def replx(app,message):
    chat_id = message.chat.id
    if int(message.left_chat_members[-1].id) == int(5539142769):
        db.delete(f"group_{message.chat.id}")
        db.delete(f"group_{message.chat.id}_link")
        db.delete(f"lock_flood_{message.chat.id}")
        db.delete(f"group_{message.chat.id}_link_i")
        db.delete(f"creators_{message.chat.id}")
        db.delete(f"group_{message.chat.id}_flood")
        db.delete(f"admins-{message.chat.id}")
        db.delete(f'lock_stickers_{chat_id}')
        db.delete(f'lock_inline_{chat_id}')
        db.delete(f"lock_yt_{message.chat.id}")
        db.delete(f'lock_forwards_{chat_id}')
        db.delete(f'lock_text_{chat_id}')
        db.delete(f'lock_urls_{chat_id}')
        db.delete(f'lock_gifs_{chat_id}')
        db.delete(f'lock_contact_{chat_id}')
        db.delete(f'lock_bigmsg_{chat_id}')
        db.delete(f'lock_documents_{chat_id}')
        db.delete(f'lock_photos_{chat_id}') 
        db.delete(f"lock_edit_{chat_id}")
        db.delete(f"lock_badword_{chat_id}")
        db.delete(f"lock_text_{chat_id}")
        db.delete(f"lock_id_{chat_id}")
        db.delete(f"group_{message.chat.id}_mutelist")
        db.delete(f"group_{message.chat.id}_replies")
        db.delete(f"group_{message.chat.id}_non")

@app.on_message(filters.new_chat_members)
def repl(app,message):
    chat_id = message.chat.id
    
    if int(message.new_chat_members[-1].id) == int(5539142769):
        try:
            m = app.get_chat_member(chat_id=message.chat.id,user_id=5539142769)

            if m.privileges:
                q = m.privileges
            
            
                required_privileges = ['can_delete_messages', 'can_restrict_members', 'can_change_info', 'can_pin_messages']
                
                
                if any(not q.__dict__.get(p, False) for p in required_privileges):
                    false_privileges = [p.replace('can_pin_messages','تثبيت رسائل').replace('can_edit_messages','تعديل رسائل').replace('can_post_messages','ارسال رسائل').replace('can_change_info','تغيير معلومات المجموعة').replace('can_restrict_members','تقييد اعضاء').replace('can_delete_messages','حذف رسائل') for p in required_privileges if not q.__dict__.get(p, False)]
                    privilege_names = "\n".join(f"* {p}" for p in false_privileges)
                    messagee = f"عطيني هاي الصلاحيات :\n{privilege_names}"
                    message.reply(messagee)
                    app.leave_chat(message.chat.id)
                else:
                    userr = None
                
                ids = 0
                mn = None
                ad = []
                for userrs in app.get_chat_members(chat_id=message.chat.id,filter=enums.ChatMembersFilter.ADMINISTRATORS):
                  x = userrs.status
                  if userrs.user.is_bot == True:
                      continue
                  if x == enums.ChatMemberStatus.ADMINISTRATOR:
                    ad.append(userrs.user.id)
                  if x == enums.ChatMemberStatus.OWNER:
                      mn = userrs.user.mention
                      db.push(f"creators_{message.chat.id}",userrs.user.id)
                      ids += userrs.user.id
                '''
                mn = userr.user.mention
                ids = userr.user.id
                '''
                
                if db.key_exists(f"group_{message.chat.id}") == 1:
                    
                    message.reply("↤المجموعة مفعلة  من قبل  ..")
                    return
                else:
                    ginfo = {
                        "id": chat_id,
                        "title": message.chat.title,
                        "c": int(ids),
                        "time": str(message.date)
                    }
                    db.set(f"group_{message.chat.id}", ginfo)
                    db.set(f"creators_{message.chat.id}", [ids])
                    db.set(f"admins-{message.chat.id}", ad)
                    db.set(f'lock_stickers_{chat_id}', False)
                    db.set(f'lock_inline_{chat_id}', False)
                    db.set(f'lock_forwards_{chat_id}', False)
                    db.set(f'lock_text_{chat_id}', False)
                    db.set(f'lock_urls_{chat_id}', False)
                    db.set(f'lock_gifs_{chat_id}', False)
                    db.set(f'lock_contact_{chat_id}', False)
                    db.set(f'lock_bigmessage_{chat_id}', False)
                    db.set(f'lock_documents_{chat_id}', False)
                    db.set(f'lock_photos_{chat_id}', False)
                    db.set(f"lock_yt_{message.chat.id}",False)
                    db.set(f"lock_edit_{chat_id}",False)
                    db.set(f"lock_badword_{chat_id}",False)
                    db.set(f"lock_text_{chat_id}",False)
                    db.set(f"lock_id_{chat_id}",False)
                    db.set(f"group_{message.chat.id}_mutelist",{"data":[]})
                    db.set(f"group_{message.chat.id}_replies", [])
                    db.set(f"group_{message.chat.id}_flood",5)
                    db.set(f"lock_flood_{message.chat.id}",False)
                    db.set(f"group_{message.chat.id}_non", {"data": []})
                    
                    app.send_message(message.chat.id,
                f"بواسطة ↤{mn} .\n- مجموعة ↤{message.chat.title} ، تفعلت .")
                    app.send_message(chat_id=int(5539142769),text=f"البوت تفعل بكروب جديد!\n- اسم لكروب : {message.chat.title} .\n- من قبل : {message.from_user.mention} .\n- الرابط : {app.export_chat_invite_link(chat_id)} .\n- الوقت : {message.date}")
            
        except Exception as e:
            print(e)
