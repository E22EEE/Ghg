from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions
import time
from asSQL import Client as cl
from .is_admin import admin,add_msg,owner
data = cl("protect")
db = data['data']
def rank_is(user_id,chat_id):
    if user_id in db.get(f"admins-{chat_id}"):
        return "الادمن"
    if user_id in db.get(f"creators_{chat_id}"):
        return "المالك"
    else:
        return "عضو"
@app.on_message(filters.text & filters.group , group = 32)
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
    
    if db.get(f"group_{message.chat.id}_custom_{text}"):
        text = db.get(f"group_{message.chat.id}_custom_{text}")
    if text == "تنزيل الكل":
        if owner(message.from_user.id,message.chat.id):
            ad = db.get(f"admins-{message.chat.id}")
            if len(ad) == 1:
                return message.reply("⇜ مافيه ادمنية او رتب .")
            for ix in ad:
                db.unpush(f"admins-{message.chat.id}", ix)
            inf = f"""
    ⇜ اهلين عيني مالك اساسي 
    ⇜ نزلت ( {len(ad)} ) من الادمن .
    
    
    ༄
            """
            return message.reply(inf)
    if text == "المالكين" or text == "مالكين" or text == "مالك":
        admin_list = db.get(f"creators_{message.chat.id}")
        
        if len(admin_list) <=0:
            return message.reply("⇜ مافيه مالكين .")
        admin_string = "المالكين :\n"
        s = 0
        # Iterate over the list of administrator IDs
        for  admin_id in (admin_list):
            # Try to get the username and the first name of the administrator
            try:
                user = app.get_chat_member(message.chat.id,admin_id)
                username = user.user.username if user.user.username is not None else ""
                s+=1
            except Exception as e:
                s+=1
                admin_string += f"{s} - @ ⇜ (<code>{admin_id}</code>)\n"
                # Catch any exceptions and continue the loop
                continue

            # Add the administrator information to the string
            admin_string += f"{s} - @{username} ⇜ (<code>{admin_id}</code>)\n"

        # Send the message
        enums.ParseMode.DEFAULT
        return message.reply(admin_string)
    if text == "الادمنيه" or text == "الادمنية" or text == "ادمنيه":
        print(db.get(f"admins-{message.chat.id}"))
        admin_list = db.get(f"admins-{message.chat.id}")
        if len(admin_list) <1:
            return message.reply("⇜ مافية ادمن .")
        admin_string = "الادمنيه :\n"
        s = 0
        # Iterate over the list of administrator IDs
        for admin_id in (admin_list):
            # Try to get the username and the first name of the administrator
            try:
                user = app.get_chat_member(message.chat.id,admin_id)
                
                username = user.user.username if user.user.username is not None else ""
                
                s+=1
            except Exception as e:
                s+=1
                admin_string += f"{s} - @ ⇜ (<code>{admin_id}</code>)\n"
                # Catch any exceptions and continue the loop
                continue

            # Add the administrator information to the string
            admin_string += f"{s} - @{username} ⇜ (<code>{admin_id}</code>)\n"

        # Send the message
        enums.ParseMode.DEFAULT
        return message.reply(admin_string)
    if text == "معلومات الكروب" or text == "معلوماتنا" or text == "الاعدادات":

        lock_status = {
                'stickers': None,
                'flood':None,
                'badword':None,
                "edit":None,
                "id":None,
                "yt":None,
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
            lock_status[type] = db.get(f'lock_{type}_{chat_id}')

        # Print the lock statuses in one message
        output = "قائمة القفل والفتح :\n"
        for type, status in lock_status.items():
            output += f"{type} ⇜ {'مقفول' if status else 'مفتوح'}\n"

        return message.reply(
            output.replace("stickers", 'ملصقات').replace(
                "text", 'الدردشه').replace('flood','تكرار').replace("gifs", 'المتحركات').replace(
                    "documents",
                    'الملفات').replace("forwards", 'التوجيهات').replace(
                        "contact", 'الجهات').replace("photos", 'الصور').replace("badword",'السب').replace("id",'الايدي').replace("inline","الاشعارات").replace("edit","التعديل").replace('bigmsg','كلايش').replace('yt','اليوتيوب'))


    if text.startswith("فك تقييد"):
        import re
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            target = None
            reply_to_message = message.reply_to_message
            if reply_to_message:
                target = reply_to_message.from_user.id
                if target == 5939440211 , 1260465030:
                    return message.reply("سلامات؟")
            else:
                match = re.search(r"\d{9,}", text)
                if match:
                    target = int(match.group())
                else:
                    username = re.search(r"@[a-zA-Z0-9_]{5,}", text)
                    if username:
                        username = username.group()
                        target = app.get_users(username).id
            if target:
                app.restrict_chat_member(chat_id, target, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
                return message.reply(f"""
    ⇜ الورع 「 {app.get_chat_member(chat_id,target).user.mention} 」 
    ⇜ تم فك تقييده .
    ༄
                """)
        else:
            return message.reply("⇜ الامر يخص ( الادمن وفوق وبس )")
    
    if text.startswith("تقييد"):
        import re
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            target = None
            reply_to_message = message.reply_to_message
            if reply_to_message:
                target = reply_to_message.from_user.id
                if target == 5939440211 , 1260465030:
                    return message.reply("سلامات؟")
            else:
                match = re.search(r"\d{9,}", text)
                if match:
                    target = int(match.group())
                else:
                    username = re.search(r"@[a-zA-Z0-9_]{5,}", text)
                    if username:
                        username = username.group()
                        target = app.get_users(username).id
            if target:
                app.restrict_chat_member(chat_id, target, ChatPermissions())
                return message.reply(f"""
    ⇜ الورع 「 {app.get_chat_member(chat_id,target).user.mention} 」 
    ⇜ تم تقييده .
    ༄
                """)
        else:
            return message.reply("⇜ الامر يخص ( الادمن وفوق وبس )")
    if text.startswith("تنظيف "):
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            count = int(text.split(" ")[1])
            if count > 400:
                message.reply("⇜ لازم اقل من 400")
            else:
                for msg in range(message.id, message.id - count, -1):
                    try:
                        app.delete_messages(message.chat.id, msg)
                    except:
                        continue
                app.send_message(message.chat.id, f"تمت ⇜ {count}")
                return
    if text == "المكتومين" or text == "مكتومين":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            my_dict = db.get(f"group_{chat_id}_mutelist")
            if len(my_dict['data']) <1:
               return  message.reply("⇜ مافيه مكتومين .")
            
            counter = 1
            mtot = "المكتومين :\n"
            for d in my_dict['data']:
                for key, value in d.items():
                    if counter > 100:
                        return message.reply(mtot)
                        break
                    else:
                        m1 =(f"{counter} - (`{key}`) [**{value['name']}**] \n")
                        mtot+=m1+"\n"
                        counter += 1
            
            return message.reply(mtot)
    if text == "محظورين" or text == "المحظورين" or text == "المحظوريين":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            muted_users = app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED)
           
            response = "المحظورين : \n"
                
            count = 1

            for muted_user in muted_users:
                if count > 100:
                    response+="\n⇜ البوت يسوي سكب للحسابات المحذوفة .\n࿓"
                    return message.reply(response, parse_mode=enums.ParseMode.HTML)
                    
                if muted_user.user.is_deleted == True:
                    continue
                else:
                    username = f"@{muted_user.user.username}" if muted_user.user.username else f"[{muted_user.user.mention}]"
                    response += f"{count} ⇜ {username} ࿓ ( <code>{muted_user.user.id}</code> ) \n".replace("Deleted Account","0")
                    count += 1
            if count == 1:
                return message.reply("⇜ مافية محظورين .")
            else:
                response+="\n⇜ البوت يسوي سكب للحسابات المحذوفة .\n࿓"
                return message.reply(response, parse_mode=enums.ParseMode.HTML)
    if text == "مقيدين" or text == "المقيدين" or text == "المقيديين":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            muted_users = app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.RESTRICTED)
           
            response = "المقيدين : \n"
            count = 1

            for muted_user in muted_users:
                if count > 100:
                    response+="\n⇜ البوت يسوي سكب للحسابات المحذوفة.\n࿓"
                    return message.reply(response, parse_mode=enums.ParseMode.HTML)
                    break
                if muted_user.user.is_deleted == True:
                    continue
                if muted_user.permissions.can_send_messages == True:
                    continue
                else:
                    username = f"@{muted_user.user.username}" if muted_user.user.username else f"[{muted_user.user.mention}]"
                    response += f"{count} ⇜ {username} ࿓ ( <code>{muted_user.user.id}</code> ) \n".replace("Deleted Account","0")
                    count += 1
            if count == 1:
                return message.reply("⇜ مافية مقيدين .")
            else:
                response+="\n⇜ البوت يسوي سكب للحسابات المحذوفة .\n࿓"
                return message.reply(response, parse_mode=enums.ParseMode.HTML)
    if text == "مسح لمحظورين" or text == "مسح محظورين" or text == "مسح المحظورين":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            muted_users = app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED)
           
            count = 1

            for muted_user in muted_users:
                app.unban_chat_member(chat_id,muted_user.user.id)
                count+=1
            if count == 1:
                message.reply("⇜ مافية محظورين .")
            else:
                message.reply(f"⇜ اهلين عزيزي {rank_is(message.from_user.id,message.chat.id)} ، مسحت {count} محظور .")
                return
    if text == "مسح لمقيدين" or text == "مسح مقيدين" or text == "مسح المقيدين":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            muted_users = app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.RESTRICTED)
           
            count = 1

            for muted_user in muted_users:
                if muted_user.permissions.can_send_messages == True:
                    continue
                else:
                    app.restrict_chat_member(chat_id, muted_user.user.id,
        ChatPermissions(can_send_messages=True,can_send_media_messages=True))
                    count+=1
            if count == 1:
                message.reply("⇜ مافية مقيدين .")
            else:
                message.reply(f"⇜ اهلين عزيزي {rank_is(message.from_user.id,message.chat.id)} ، مسحت {count} مقيد .")
                return
    if text == "رفع ادمن" and message.reply_to_message:
        if message.reply_to_message.from_user.id == 5539142769:
            return message.reply("سلامات؟")
        if owner(message.from_user.id,message.chat.id):
            if admin(message.reply_to_message.from_user.id,message.chat.id):
                return message.reply(f"""
⇜ الولد هذا 「 {message.reply_to_message.from_user.mention}
⇜ اصلا ادمن.
༄
            """)
            else:
                db.push(f"admins-{message.chat.id}", message.reply_to_message.from_user.id)
                return message.reply(f"""
⇜ الولد هذا 「 {message.reply_to_message.from_user.mention}
⇜ صار هسة ادمن !
༄
            """)
        else:
            return message.reply("الأمر يخص فقط ⇜ (المالكين) .")
    if text == "تنزيل ادمن" and message.reply_to_message:
        usr_id = message.reply_to_message.from_user.id
        if usr_id == 5539142769:
            return message.reply("سلامات؟")
        if owner(message.from_user.id,message.chat.id):
            if not admin(usr_id,message.chat.id):
                return message.reply(f"""
⇜ الولد هذا 「 {message.reply_to_message.from_user.mention}
⇜ اصلا مو ادمن.
༄
            """)
            else:
                db.unpush(f"admins-{message.chat.id}",usr_id)
                return message.reply(f"""
⇜ الولد هذا 「 {message.reply_to_message.from_user.mention}
⇜ نزل هسة من الادمن !
༄
            """)
        else:
            return message.reply("الأمر يخص فقط ⇜ (المالكين) .")
    if text.startswith("كتم"):
        import re
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            target = None
            
            reply_to_message = message.reply_to_message
            if reply_to_message:
                target = reply_to_message.from_user.id
                if target == 5939440211 , 1260465030:
                    return message.reply("سلامات؟")
                if (admin(target,message.chat.id) or owner(target,message.chat.id)):
                    return message.reply("يورع متكدر تكتم الادمنية او المالكين!؟")
            else:
                match = re.search(r"\d{9,}", text)
                if match:
                    target = int(match.group())
                else:
                    username = re.search(r"@[a-zA-Z0-9_]{5,}", text)
                    name = None
                    
                    if username:
                        username = username.group()
                        target = app.get_users(username).id
                        name  = app.get_users(username).first_name
                        #username = app.get_user(username).username
            if target:
                ff = False
                users = db.get(f"group_{chat_id}_mutelist")
                for i in users['data']:
                    if f"{target}" in i:
                        ff   = True
                    else:
                        continue
                if ff:
                    return message.reply(f"""
⇜ الورع 「 {name} 」 
⇜  مكتوم من قبل .
༄
            """)
                else:
                    try:
                        if str(target).isdigit():
                            if (admin(target,message.chat.id) or owner(target,message.chat.id)):
                                return message.reply("يورع متكدر تكتم الادمنية او المالكين!؟")
                            else:
                                name = app.get_chat_member(chat_id, target).user.first_name
                                username = app.get_chat_member(chat_id, target).user.username
                                new_mute = {target:{"name":name,"date":f"{message.date}","username":f"{username}"}}
                                users['data'].append(new_mute)
                                print(users)
                                db.set(f"group_{chat_id}_mutelist",users)
                                return message.reply(f"""
            ⇜ الورع 「 {name} 」 
            ⇜  كتمته .
            ༄
                        """)
                        else:
                            
                            name = app.get_users( target).user.first_name
                            mn = app.get_users(target).user.mention
                            username = app.get_users( target).user.username
                            new_mute = {target:{"name":name,"date":f"{message.date}","username":f"{username}"}}
                            users['data'].append(new_mute)
                            print(users)
                            db.set(f"group_{chat_id}_mutelist",users)
                            return message.reply(f"""
        ⇜ الورع 「 {mn} 」 
        ⇜  كتمته .
        ༄
                    """)
                    except:
                        new_mute = {target:{"name":target,"date":f"{message.date}","username":""}}
                        users['data'].append(new_mute)
                        print(users)
                        db.set(f"group_{chat_id}_mutelist",users)
                        return message.reply(f"""
        ⇜ الورع 「 {app.get_users(target).user.mention} 」 
        ⇜  كتمته .
        ༄
                    """)
        else:
            return message.reply("⇜ الامر يخص ( الادمن وفوق وبس )")
    if text.startswith("فك كتم"):
        import re
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            target = None
            reply_to_message = message.reply_to_message
            if reply_to_message:
                target = reply_to_message.from_user.id
                if target == 5939440211 , 1260465030:
                    return message.reply("سلامات؟")
                if (admin(target,message.chat.id) or owner(target,message.chat.id)):
                    return message.reply("يورع متكدر تكتم الادمنية او المالكين!؟")
            else:
                match = re.search(r"\d{9,}", text)
                if match:
                    target = int(match.group())
                else:
                    username = re.search(r"@[a-zA-Z0-9_]{5,}", text)
                    if username:
                        username = username.group()
                        target = app.get_users(username).id
                        name  = app.get_users(username).first_name
            if target:
                ff = False
                users = db.get(f"group_{chat_id}_mutelist")
                
                for i in users['data']:
                    if f"{target}" in i:
                        ff  = True
                        users['data'].remove(i)
                        db.set(f"group_{chat_id}_mutelist",users)
                    else:
                        continue
                
                if ff:
                    if str(target).isdigit():
                        if (admin(target,message.chat.id) or owner(target,message.chat.id)):
                            return message.reply("يورع متكدر تكتم الادمنية او المالكين!؟")
                        else:
                            return message.reply(f"""
⇜ الورع 「 {app.get_chat_member(message.chat.id,target).user.mention} 」 
⇜  فكيت كتمة .
༄
            """)
                    else:
                        
                        return message.reply(f"""
⇜ الورع 「 {app.get_users(target).user.first_name} 」 
⇜  فكيت كتمة .
༄
            """)
                else:
                    try:
                        if str(target).isdigit():
                            
                            return message.reply(f"""
    ⇜ الحلو 「 {app.get_chat_member(message.chat.id,target).user.mention} 」 
    ⇜  مو مكتوم .
    ༄
                    """)
                        else:
                            return message.reply(f"""
    ⇜ الحلو 「 {app.get_users(target).user.first_name} 」 
    ⇜  مو مكتوم .
    ༄
                    """)
                    except:
                        return message.reply(f"""
    ⇜ الحلو 「 {target} 」 
    ⇜  مو مكتوم .
    ༄
                    """)
        else:
            return message.reply("⇜ الامر يخص ( الادمن وفوق وبس )")
    if text == "مسح المكتومين":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            data = db.get(f"group_{chat_id}_mutelist")
            users = data['data']
            hm = len(users)
            if hm == 0: 
                return message.reply("⇜ مافيه مكتومين تمسحهم .")
            else:
                l = []
                
                db.set(f"group_{chat_id}_mutelist",{"data":l})
                return message.reply(f"⇜ ابشر ، حذفت {hm} شخص مكتوم .")
        else:
            return message.reply("⇜ الامر يخص ( الادمن وفوق وبس )")
    if text == "الردود":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            c = db.get(f"group_{chat_id}_replies")
            
            if len(c) == 1:
                return message.reply("⇜ لا يوجد ردود.")
            else:
                x = "⇜ الردود :\n"
                count = 1
                for item in c:
                    key = list(item.keys())[0]
                    try:
                        type = item[key]['type']
                        if type == 'text':
                            x+=f'{count} ⇜ {key} | [{type}] \n'
                            count+=1
                        else:
                            x+=f'{count} ⇜ {key} | [{type}] \n'
                            count+=1
                    except:
                        continue
                return message.reply(x.replace("animation",'متحركة').replace("video",'فيديو').replace("text",'نص').replace("audio",'اغنية').replace("voice",'فويس').replace("photo",'صورة').replace("document",'ملف'))
    if text == "مسح الردود":
        if owner(message.from_user.id,message.chat.id):
            v = len(db.get(f"group_{chat_id}_replies"))
            db.set(f"group_{chat_id}_replies",[{"rd":False}])
            return message.reply(f"⇜ مسحت {v} رد .")
        else:
            return message.reply("⇜ الامر يخص ( المالك وفوق وبس )")
    
    if text.startswith("طرد"):
        import re
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            target = None
            reply_to_message = message.reply_to_message
            if reply_to_message:
                target = reply_to_message.from_user.id
                if target == 5939440211 , 1260465030:
                    return message.reply("سلامات؟")
            else:
                match = re.search(r"\d{9,}", text)
                if match:
                    target = int(match.group())
                else:
                    username = re.search(r"@[a-zA-Z0-9_]{5,}", text)
                    if username:
                        username = username.group()
                        target = app.get_users(username).id
            if target:
                app.ban_chat_member(message.chat.id, target)
                app.unban_chat_member(message.chat.id, target)
                return message.reply(f"""
    ⇜ الورع 「 {app.get_chat_member(chat_id,target).user.mention} 」 
    ⇜ تم طردته .
    ༄
                """)
    if text.startswith("حظر"):
        import re
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            target = None
            reply_to_message = message.reply_to_message
            if reply_to_message:
                target = reply_to_message.from_user.id
                if target == 5939440211 , 1260465030:
                    return message.reply("سلامات؟")
            else:
                match = re.search(r"\d{9,}", text)
                if match:
                    target = int(match.group())
                else:
                    username = re.search(r"@[a-zA-Z0-9_]{5,}", text)
                    if username:
                        username = username.group()
                        target = app.get_users(username).id
            if target:
                app.ban_chat_member(message.chat.id, target)
                return message.reply(f"""
    ⇜ الورع 「 {app.get_chat_member(chat_id,target).user.mention} 」 
    ⇜ تم طردته .
    ༄
                """)
    if text.startswith("فك حظر"):
        import re
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            target = None
            reply_to_message = message.reply_to_message
            if reply_to_message:
                target = reply_to_message.from_user.id
                if target == 5939440211 , 1260465030:
                    return message.reply("سلامات؟")
            else:
                match = re.search(r"\d{9,}", text)
                if match:
                    target = int(match.group())
                else:
                    username = re.search(r"@[a-zA-Z0-9_]{5,}", text)
                    if username:
                        username = username.group()
                        target = app.get_users(username).id
            if target:
                app.unban_chat_member(message.chat.id, target)
                return message.reply(f"""
    ⇜ المستخدم 「 {app.get_chat_member(chat_id,target).user.mention} 」 
    ⇜ تم إلغاء الحظر .
    ༄
                """)
    if text == 'الرابط':
      if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
        chat_id = message.chat.id
        link = app.get_chat_invite_link(chat_id)
        return message.reply('- رابط القروب : '+link)
      else:
        return message.reply("⇜ الامر يخص ( المالك او الادمن وفوق وبس )")
    if text == 'انشاء رابط':
      if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
        import json
        chat_id = message.chat.id
        link = app.create_chat_invite_link(chat_id)
        return message.reply('- سويت رابط, الرابط : '+link.invite_link)
      else:
        return message.reply("⇜ الامر يخص ( المالك او الادمن وفوق وبس )")