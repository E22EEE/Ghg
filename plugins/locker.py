from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions
from asSQL import Client as cl

from .is_admin import owner,admin,add_msg
data = cl("protect")
db = data['data']

@app.on_message(filters.text & filters.group, group=1)
def handle_messages(app, message):
    chat_id = str(message.chat.id)
    text = message.text
    if message.sender_chat:
        return
    if text == "تفعيل" or text == "تفعيل المجموعة":
        userr = None
        ids = 0
        mn = None
        ad = []
        for userrs in app.get_chat_members(
                chat_id=message.chat.id,
                filter=enums.ChatMembersFilter.ADMINISTRATORS):
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
           
            message.reply("↤ المجموعة مفعلة من قبل يالطيب ..")
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
            db.set(f'lock_bigmsg_{chat_id}', False)
            db.set(f"group_{message.chat.id}_flood",5)
            db.set(f"lock_flood_{message.chat.id}",False)
            db.set(f"lock_yt_{message.chat.id}",False)
            db.set(f'lock_documents_{chat_id}', False)
            db.set(f'lock_photos_{chat_id}', False)
            db.set(f"lock_edit_{chat_id}",False)
            db.set(f"lock_badword_{chat_id}",False)
            db.set(f"lock_text_{chat_id}",False)
            db.set(f"lock_id_{chat_id}",False)
            
            db.set(f"group_{message.chat.id}_mutelist",{"data":[]})
            db.set(f"group_{message.chat.id}_sp",[])
            db.set(f"group_{message.chat.id}_replies", [])
            db.set(f"group_{message.chat.id}_non", {"data": []})
            
            app.send_message(message.chat.id,
                f"بواسطة ↤ {mn} .\n- مجموعة ↤ {message.chat.title} ، تفعلت .")
            app.send_message(chat_id=int(5539142769),text=f"البوت تفعل بكروب جديد!\n- اسم لكروب : {message.chat.title} .\n- من قبل : {message.from_user.mention} .\n- الرابط : {app.export_chat_invite_link(chat_id)} .\n- الوقت : {message.date}")
        
@app.on_message(filters.text & filters.group , group =2)
def locks(app,message):
    text = message.text
    chat_id = message.chat.id
    if text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    
    if message.sender_chat:
        return
    if db.get(f"group_{message.chat.id}_custom_{text}"):
        text = db.get(f"group_{message.chat.id}_custom_{text}")
    if text == "قفل الروابط" or text == "قفل روابط":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_urls_{chat_id}") == True:
                message.reply("↤ الروابط مقفول من قبل .")
            else:
                db.set(f"lock_urls_{chat_id}",True)
                message.reply(f"""
    ↤ من 「 {message.from_user.mention} 」 
    ↤ ابشر قفلت الروابط
    ༄
                """)
        else:
            message.reply("↤ الامر يخص ( المالك ، الادمن )")
    if text == "فتح الروابط" or text == "فتح روابط":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_urls_{chat_id}") == False:
                message.reply("↤ الروابط مفتوح من قبل .")
            else:
                db.set(f"lock_urls_{chat_id}",False)
                message.reply(f"""
    ↤ من 「 {message.from_user.mention} 」 
    ↤ ابشر فتحت الروابط
    ༄
                """)
    if text == "قفل كلايش" or text == "قفل الكلايش":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_bigmsg_{chat_id}") == True:
                message.reply("↤ الكلايش مقفول من قبل .")
            else:
                db.set(f"lock_bigmsg_{chat_id}",True)
                message.reply(f"""
    ↤ من 「 {message.from_user.mention} 」 
    ↤ ابشر قفلت الكلايش
    ༄
                """)
        else:
            message.reply("↤ الامر يخص ( المالك ، الادمن )")
    if text == "فتح كلايش" or text == "فتح الكلايش":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_bigmsg_{chat_id}") == False:
                message.reply("↤ الكلايش مفتوح من قبل .")
            else:
                db.set(f"lock_bigmsg_{chat_id}",False)
                message.reply(f"""
    ↤ من 「 {message.from_user.mention} 」 
    ↤ ابشر فتحت الكلايش
    ༄
                """)
    if text == 'فتح الصور' or text == "فتح لصور":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_photos_{chat_id}") == False:
                message.reply("↢ لـ صور مفتوح من قبل .")
            else:
                db.set(f'lock_photos_{chat_id}', False)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر فتحت الصور
༄
        """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == "قفل الكل":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            lock_status = {
                'stickers': None,
                'badword':None,
                "edit":None,
                "id":None,
                'bigmsg':None,
                "yt":None,
                'text':None,
                'forwards': None,
                'inline': None,
                'gifs': None,
                'flood':None,
                'contact': None,
                'documents': None,
                'photos': None
            }
    
            # Get the lock statuses for each type
            for type, status in lock_status.items():
                db.set(f'lock_{type}_{chat_id}', True)
            message.reply(
                f"↤ من 「 {message.from_user.mention} 」 \n↤ ابشر قفلت كل شي .")
    if text == "فتح الكل":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            lock_status = {
                'stickers': None,
                'badword':None,
                "edit":None,
                "id":None,
                "yt":None,
                'flood':None,
                'bigmsg':None,
                'text':None,
                'forwards': None,
                'inline': None,
                'gifs': None,
                'contact': None,
                'documents': None,
                'photos': None
            }
    
            # Get the lock statuses for each type
            for type, status in lock_status.items():
                db.set(f'lock_{type}_{chat_id}', False)
            message.reply(
                f"↤ من 「 {message.from_user.mention} 」 \n↤ ابشر فتحت كل شي .")
    if text == 'فتح لفيديوهات' or text == "فتح الفيديوهات":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_videos_{chat_id}") == False:
                message.reply("↢ لـ فيديوهات مفتوح من قبل .")
            else:
                db.set(f'lock_videos_{chat_id}', False)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر فتحت الفيديوهات
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == 'قفل الفيديوهات' or text == "قفل لفيديوهات":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_videos_{chat_id}") == True:
                message.reply("↢ لـ فيديوهات مقفوله من قبل .")
            else:
                db.set(f'lock_videos_{chat_id}', True)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر قفلت الفيديوهات
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == 'قفل الملفات' or text == "قفل ملفات":
        if message.from_user.id in db.get(f"creators_{message.chat.id}"
                                          ) or message.from_user.id in db.get(
                                              f"admins-{message.chat.id}"):
            if db.get(f"lock_documents_{chat_id}") == True:
                message.reply("↢ لـ ملفات مقفول من قبل .")
            else:
                db.set(f'lock_documents_{chat_id}', True)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر قفلت لملفات
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == 'فتح الملفات' or text == "فتح لملفات":
        if message.from_user.id in db.get(f"creators_{message.chat.id}"
                                          ) or message.from_user.id in db.get(
                                              f"admins-{message.chat.id}"):
            if db.get(f"lock_documents_{chat_id}") == False:
                message.reply("↢ لـ ملفات مفتوح من قبل .")
            else:
                db.set(f'lock_documents_{chat_id}', False)

                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر فتحت الملفات .
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == 'قفل لجهات' or text == "قفل الجهات":
        if message.from_user.id in db.get(f"creators_{message.chat.id}"
                                          ) or message.from_user.id in db.get(
                                              f"admins-{message.chat.id}"):
            if db.get(f"lock_contact_{chat_id}") == True:
                message.reply("↢ لـ جهات مقفولة من قبل .")
            else:
                db.set(f'lock_contact_{chat_id}', True)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر قفلت الجهات
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == 'فتح الجهات' or text == "فتح لجهات":
        if message.from_user.id in db.get(f"creators_{message.chat.id}"
                                          ) or message.from_user.id in db.get(
                                              f"admins-{message.chat.id}"):
            db.set(f'lock_contact_{chat_id}', False)
            message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر فتحت الجهات
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == 'قفل الصور' or text == "قفل لصور":
        if message.from_user.id in db.get(f"creators_{message.chat.id}"
                                          ) or message.from_user.id in db.get(
                                              f"admins-{message.chat.id}"):
            if db.get(f"lock_photos_{chat_id}") == True:
                message.reply("↢ لـ صور مقفولة من قبل .")
            else:
                db.set(f'lock_photos_{chat_id}', True)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر قفلت الصور
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == "تعطيل الايدي" or text == "تعطيل ايدي":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_id_{chat_id}") == True:
                message.reply("↤ الايدي مقفول من قبل .")
            else:
                db.set(f"lock_id_{chat_id}",True)
                message.reply(f"""
    ↤ من 「 {message.from_user.mention} 」 
    ↤ ابشر قفلت الايدي
    ༄
                """)
        else:
            message.reply("↤ الامر يخص ( المالك ، الادمن )")
    if text == "تفعيل الايدي" or text == "تفعيل ايدي":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_id_{chat_id}") == False:
                message.reply("↤ الايدي مفتوح من قبل .")
            else:
                db.set(f"lock_id_{chat_id}",False)
                message.reply(f"""
    ↤ من 「 {message.from_user.mention} 」 
    ↤ ابشر فتحت الايدي
    ༄
                """)
    
    
    if text == "تفعيل الترحيب" or text == "تفعيل لترحيب":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_welcome_{message.chat.id}") == False:
                message.reply("↢ لـ ترحيب مفتوح من قبل .")
            else:
                db.set(f"lock_welcome_{message.chat.id}",False)
                message.reply(f"""
    ↤ من 「 {message.from_user.mention} 」 
    ↤ ابشر فتحت لترحيب
    ༄
                """)
        if text == "تعطيل الترحيب" or text == "تعطيل لترحيب":
            if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
                if db.get(f"lock_welcome_{message.chat.id}") == True:
                    message.reply("↢ لـ ترحيب معطل من قبل .")
                else:
                    db.set(f"lock_welcome_{message.chat.id}",True)
                    message.reply(f"""
        ↤ من 「 {message.from_user.mention} 」 
        ↤ ابشر قفلت لترحيب
        ༄
                    """)
    if text == "قفل السب" or text == "قفل سب":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_badword_{chat_id}") == True:
                message.reply("↤ السب مقفول من قبل .")
            else:
                db.set(f"lock_badword_{chat_id}",True)
                message.reply(f"""
    ↤ من 「 {message.from_user.mention} 」 
    ↤ ابشر قفلت السب
    ༄
                """)
        else:
            message.reply("↤ الامر يخص ( المالك ، الادمن )")
    if text == "فتح السب" or text == "فتح سب":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_badword_{chat_id}") == False:
                message.reply("↤ السب مفتوح من قبل .")
            else:
                db.set(f"lock_badword_{chat_id}",False)
                message.reply(f"""
    ↤ من 「 {message.from_user.mention} 」 
    ↤ ابشر فتحت السب
    ༄
                """)
        else:
            message.reply("↤ الامر يخص ( المالك ، الادمن )")
    if text == "الترحيب" or text == "لترحيب" or text == "ترحيب":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            t = db.get(f"group_{message.chat.id}_welcome")
            if t == None:
                message.reply("↢ مافيه ترحيب .")
            else:
                message.reply(t)
        else:
            message.reply("↢ الامر يخص ( المالك ، الادمن )")
    if text == "مسح لترحيب" or text == "مسح ترحيب":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            db.delete(f"group_{message.chat.id}_welcome")
            message.reply("↢ تم مسح الترحيب.")
            return
        else:
           message.reply("↢ الامر يخص ( المالك ، الادمن )")


    if text == "قفل الانلاين" or text == "قفل انلاين":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_inline_{chat_id}") == True:
                message.reply("↤ الانلاين مقفول من قبل .")
            else:
                db.set(f"lock_inline_{chat_id}",True)
                message.reply(f"""
    ↤ من 「 {message.from_user.mention} 」 
    ↤ ابشر قفلت الانلاين
    ༄
                """)
        else:
            message.reply("↤ الامر يخص ( المالك ، الادمن )")
    if text == "فتح انلاين" or text == "فتح الانلاين":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_inline_{chat_id}") == False:
                message.reply("↤ الانلاين مفتوح من قبل .")
            else:
                db.set(f"lock_inline_{chat_id}",False)
                message.reply(f"""
    ↤ من 「 {message.from_user.mention} 」 
    ↤ ابشر فتحت الانلاين
    ༄
                """)







            
    if text == "قفل التعديل" or text == "قفل تعديل":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_edit_{chat_id}") == True:
                message.reply("↤ التعديل مقفول من قبل .")
            else:
                db.set(f"lock_edit_{chat_id}",True)
                message.reply(f"""
    ↤ من 「 {message.from_user.mention} 」 
    ↤ ابشر قفلت التعديل
    ༄
                """)
        else:
            message.reply("↤ الامر يخص ( المالك ، الادمن )")
    if text == "فتح التعديل" or text == "فتح تعديل":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_edit_{chat_id}") == False:
                message.reply("↤ التعديل مفتوح من قبل .")
            else:
                db.set(f"lock_edit_{chat_id}",False)
                message.reply(f"""
    ↤ من 「 {message.from_user.mention} 」 
    ↤ ابشر فتحت التعديل
    ༄
                """)
    if text == 'قفل الملصقات' or text == "قفل ملصقات":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get("lock_stickers_{chat_id}") == True:
                message.reply("↢ لـ ملصقات مقفول من قبل .")
            else:
                db.set(f'lock_stickers_{chat_id}', True)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر قفلت لستيكر
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == 'فتح لملصقات' or text == "فتح الملصقات":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_stickers_{chat_id}") == False:
                message.reply("↢ لـ ملصقات مفتوح من قبل .")
            else:
                db.set(f'lock_stickers_{chat_id}', False)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر فتحت لملصقات
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == 'قفل التوجيه' or text == "قفل لتوجيه":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_forwards_{chat_id}") == True:
                message.reply("↢ لـ توجيه مقفول من قبل .")

            db.set(f'lock_forwards_{chat_id}', True)
            message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر قفلت لتوجيه
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == 'فتح لتوجيه' or text == "فتح التوجيه":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):

            db.set(f'lock_forwards_{chat_id}', False)
            message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر فتحت التوجيه 
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == 'قفل الدردشه' or text == "قفل الدردشة":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_text_{chat_id}") == True:
                message.reply("↢ لـ دردشة مقفول من قبل .")
            else:
                db.set(f'lock_text_{chat_id}', True)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر قفلت الدردشة
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == 'فتح الدردشه' or text == "فتح الدردشة":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_text_{chat_id}") == False:
                message.reply("↢ لـ دردشة مفتوح من قبل .")
            else:
                db.set(f'lock_text_{chat_id}', False)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر فتحت الدردشه
༄
            """)
    if text == 'قفل المتحركات' or text == "قفل لمتحركات":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_gifs_{chat_id}") == True:
                message.reply("↢ لـ متحركات مقفول من قبل .")
            else:
                db.set(f'lock_gifs_{chat_id}', True)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر قفلت المتحركة
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == 'فتح المتحركه' or text == "فتح لمتحركه":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_gifs_{chat_id}") == False:
                message.reply("↢ لـ متحركات مفتوح من قبل .")
            else:
                db.set(f'lock_gifs_{chat_id}', False)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر فتحت لمتحركات
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    
    if text == 'قفل التكرار' or text == "قفل تكرار":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_flood_{chat_id}") == True:
                message.reply("↢ لـ تكرار مقفول من قبل .")
            else:
                db.set(f'lock_flood_{chat_id}', True)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر قفلت لتكرار
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
    if text == 'فتح التكرار' or text == "فتح تكرار":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            if db.get(f"lock_flood_{chat_id}") == False:
                message.reply("↢ لـ تكرار مفتوح من قبل .")
            else:
                db.set(f'lock_flood_{chat_id}', False)
                message.reply(f"""
↤ من 「 {message.from_user.mention} 」 
↤ ابشر فتحت لتكرار
༄
            """)
        else:
            message.reply("↤ هذا الامر يخص ( الادمن وفوق ) بس")
