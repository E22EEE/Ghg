from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions
import time,getids 
from asSQL import Client as cl
from .is_admin import admin,add_msg,owner
data = cl("protect")
db = data['data']

from getids import get_date_as_string
 
 
 
def get_creation_date(id: int) -> str:
    if str(id)[0] == '5' and str(id)[1] == '9':
        return '01/2023'
    if len(str(id)) == 10:
        if str(id)[0] == '5':
            if not str(id)[1] == '0':
                return '0{}/2022'.format(str(id).replace("0","")[2])
            else:
                return '0{}/2022'.format(str(id)[2])
        elif str(id)[0] == '1' and str(id)[1] == '0':
            if '11' in str(id):
                return '11/2020'
            if '12' in str(id):
                return '12/2020'
            else:
                return '0{}/2020'.format(str(id).replace("0","")[2])
        else:
            if '11' in str(id):
                return '11/2021'
            if '12' in str(id):
                return '12/2021'
            if '10' in str(id):
                return '10/2021'
            else:
                return '0{}/2021'.format(str(id).replace("0","")[1])
    if len(str(id)) == 9:
        if str(id)[0] == '9':
            return '0{}/2020'.format(str(id).replace("0","")[0])
        else:
            return get_date_as_string(id)[1]
    else:
        return get_date_as_string(id)[1]
def rank_is(user_id,chat_id):
    if user_id in db.get(f"admins-{chat_id}"):
        return "الادمن"
    if user_id in db.get(f"creators_{chat_id}"):
        return "المالك"
    
    else:
        return "عضو"
@app.on_message(filters.text & filters.group , group = 10)
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
    if text == "رسائلي":
        msgs_count = db.get(f"group_{message.chat.id}_{message.from_user.id}_info")['msgs']
        message.reply(f"رسائلك ⇜  {msgs_count}")
    if text == "ايدي":
        if db.get(f"lock_id_{chat_id}") == True:
            message.reply("الايدي معطل من قبل الادمنية او المالكين .")
        else:
            if message.reply_to_message:
                chat_member = app.get_chat_member(message.chat.id,
                                                  message.reply_to_message.from_user.id)
                rank = chat_member.status
                msgs_count = db.get(
                    f"group_{message.chat.id}_{message.reply_to_message.from_user.id}_info")['msgs']
                infos = f"""
⇜ الاسم ↢ {message.reply_to_message.from_user.first_name} 
⇜ بالمنشن ↢ {message.reply_to_message.from_user.mention}
⇜ الايدي ↢ {message.reply_to_message.from_user.id} 
⇜ اليوزر ↢ (  {message.reply_to_message.from_user.username} )
⇜ الرتبه ↢  ( {rank_is(message.reply_to_message.from_user.id,message.chat.id)} )
⇜ رتبتك بالمجموعة ↢  (  {rank} )
⇜  رسائلك ↢ {msgs_count} 
༄ 
        """.replace("ChatMemberStatus.MEMBER",
                    'عضو').replace("ChatMemberStatus.ADMINISTRATOR", 'ادمن').replace(
                        "ChatMemberStatus.OWNER",
                        "المالك").replace("None", "مافيه يوزر").replace("ChatMemberStatus.RESTRICTED",'عضو')
                message.reply(infos)
            else:
                chat_member = app.get_chat_member(message.chat.id,
                                              message.from_user.id)
                rank = chat_member.status
                msgs_count = db.get(
                    f"group_{message.chat.id}_{message.from_user.id}_info")['msgs']
                infos = f"""
⇜ الاسم ↢ {message.from_user.first_name} 
⇜ بالمنشن ↢ {message.from_user.mention}
⇜ الايدي ↢ {message.from_user.id} 
⇜ اليوزر ↢ (  {message.from_user.username} )
⇜ الرتبه ↢  ( {rank_is(message.from_user.id,message.chat.id)} )
⇜ رتبتك بالمجموعة ↢  (  {rank} )
⇜  رسائلك ↢ {msgs_count} 
༄ 
        """.replace("ChatMemberStatus.MEMBER",
                    'عضو').replace("ChatMemberStatus.ADMINISTRATOR", 'ادمن').replace(
                        "ChatMemberStatus.OWNER",
                        "المالك").replace("None", "مافيه يوزر").replace("ChatMemberStatus.RESTRICTED",'عضو')
                message.reply(infos)
    if text == "الرابط":
        if db.key_exists(f"group_{message.chat.id}_link") == 0:
            x = app.export_chat_invite_link(message.chat.id)
            db.set(f"group_{message.chat.id}_link",x)
            message.reply(f"الرابط ⇜ {x}")
        else:
            message.reply(f"الرابط : {db.get(f'group_{message.chat.id}_link')}")
    if text == 'افتار' and message.reply_to_message and message.reply_to_message.from_user:
        m = message
        if not m.reply_to_message.from_user.photo:
            return m.reply(f' مقدر اجيب افتاره يمكن حاظرني')
        else:
            if m.reply_to_message.from_user.username:
                photo = f'http://t.me/{m.reply_to_message.from_user.username}'
            else:
                for p in app.get_chat_photos(m.reply_to_message.from_user.id,
                                             limit=1):
                    photo = p.file_id
            get_bio = app.get_chat(m.reply_to_message.from_user.id).bio
            if not get_bio:
                caption = None
            else:
                caption = f'`{get_bio}`'
            return m.reply_photo(photo, caption=caption)
    if text == 'افتاري':
        m = message
        if not m.from_user.photo:
            return m.reply(f' ماقدر اجيب افتارك ارسل نقطه خاص وارجع جرب')
        else:
            if m.from_user.username:
                photo = f'http://t.me/{m.from_user.username}'
            else:
                for p in app.get_chat_photos(m.from_user.id, limit=1):
                    photo = p.file_id
            get_bio = app.get_chat(m.from_user.id).bio
            if not get_bio:
                caption = None
            else:
                caption = f'`{get_bio}`'
            return m.reply_photo(photo, caption=caption)
    if text == "روليت":
        db.delete(f"running_rolet_{message.chat.id}")
        if db.get(f"running_rolet_{message.chat.id}"):
                return message.reply("⇜ فيه روليت شغالة .")
        else:
            db.set(f"running_rolet_players_{message.chat.id}", [])
            current_time = time.time()
            db.set(f"running_rolet_info_{message.chat.id}", current_time)
            db.set(f"running_rolet_{message.chat.id}", True)
            db.set(f"running_rolet_admin_{chat_id}",message.from_user.id)
            
            return message.reply(f"⇜ من {message.from_user.mention} بديت روليت جديد ..\n\n⇜ اذا تبي تفوت للعبة ارسل انا .\n\nعشان ننهي اللعبة ارسل تم (للي بدء اللعبة .)\n\n⇜ 5 دقايق وينمسح هذا الروليت ..")
    if text == "انا":
        if db.get(f"running_rolet_{message.chat.id}"):
            found = None
            players = db.get(f"running_rolet_players_{message.chat.id}")
            admin = db.get(f"running_rolet_admin_{message.chat.id}")
            if len(players) == 10:
                return message.reply("الروليت قفلت فيها 10 !")
            if message.from_user.id == admin:
                return message.reply("انت مشارك !")
            for p in players:
                if p['id'] == message.from_user.id:
                    found = True
                else:
                    continue
            if found:
                return message.reply("انت مشارك !")
            else:
                d = {"id": message.from_user.id, "name": message.from_user.mention}
                db.push(f"running_rolet_players_{message.chat.id}", d)
                return message.reply("ضفتك بلروليت")
        else:
            return message.reply("مافيه روليت")
    if text == "تم":
        import random
        admin = db.get(f"running_rolet_admin_{message.chat.id}")
        if message.from_user.id == admin:
            if db.get(f"running_rolet_{message.chat.id}"):
                players = db.get(f"running_rolet_players_{message.chat.id}")
                if len(players) == 2 or len(players) >2:
                    player = random.choice(players)
                    name = player['name']
                    db.delete(f"running_rolet_players_{message.chat.id}")
                    db.delete(f"running_rolet_{message.chat.id}")
                    db.delete(f"running_rolet_info_{message.chat.id}")
                    db.delete(f"running_rolet_admin_{message.chat.id}")
                    return message.reply(f"اختاريت : {name}")
                    
                else:
                    return message.reply("مافيه ناس ..")
            else:
                return message.reply("مافيه روليت")
        return
    command = text
    if command.startswith("كشف"):
        command = text.split()
        if message.reply_to_message:
            user = message.reply_to_message.from_user
            rank = None
            type_of_get_info = "بالرد"
            chat_member = app.get_chat_member(message.chat.id, user.id)
            rank = chat_member.status
            infos = f"""
⇜ الاسم ↢ {user.first_name} 
⇜ الايدي ↢ {user.id} 
⇜ اليوزر ↢ (  {user.username} )
⇜ الرتبه ↢  ( {rank_is(user.id,message.chat.id)} )
⇜ بالمجموعة ↢  (  {rank} )
⇜ نوع الكشف ↢ {type_of_get_info} 
༄ 
""".replace("ChatMemberStatus.MEMBER",
            'عضو').replace("ChatMemberStatus.ADMINISTRATOR", 'ادمن').replace(
            "ChatMemberStatus.OWNER",
            "المالك").replace("None", "مافيه يوزر").replace("ChatMemeberStatus.RESTRICTED","عضو").replace(
            "ChatMemberStatus.BANNED",'محظور')
            return message.reply(infos)
        if len(command) == 2:
            try:
                
                if command[1].startswith("@"):
                    user = app.get_users(command[1][1:])
                    rank = None
                    type_of_get_info = "باليوزر"
                else:
                    user = app.get_users(int(command[1]))
                    rank = None
                    type_of_get_info = "بالايدي"
                chat_member = app.get_chat_member(message.chat.id, user.id)
                rank = chat_member.status
                infos = f"""
⇜ الاسم ↢ {user.first_name} 
⇜ الايدي ↢ {user.id} 
⇜ اليوزر ↢ (  {user.username} )
⇜ الرتبه ↢  ( {rank_is(user.id,message.chat.id)} )
⇜ بالمجموعة ↢  (  {rank} )
⇜ نوع الكشف ↢ {type_of_get_info} 
༄ 
""".replace("ChatMemberStatus.MEMBER",
                'عضو').replace("ChatMemberStatus.ADMINISTRATOR", 'ادمن').replace(
                "ChatMemberStatus.OWNER",
                "المالك").replace("None", "مافيه يوزر")
                message.reply(infos)
            except Exception as e:
                #print(e)
                message.reply("ما لقيت احد")
    if text == "بايو":
        if message.reply_to_message:
            id = message.reply_to_message.from_user.id
            get_bio = app.get_chat(id).bio
            if get_bio:
                return message.reply(f"``{get_bio}``",parse_mode=enums.ParseMode.MARKDOWN)
            else:
                return message.reply("- ما عنده بايو .")
        else:
            id = message.from_user.id
            get_bio = app.get_chat(id).bio
            if get_bio:
                return message.reply(f"``{get_bio}``")
                
            else:
                return message.reply("- ما في بايو.")
    if (text == "الانشاء" or text == "انشاء"):
        if message.reply_to_message:
            id = message.reply_to_message.from_user.id
            date = get_creation_date(id)
            message.reply(f"الانشاء : {date}")
        else:
            id = message.from_user.id
            date = get_creation_date(id)
            message.reply(f"الانشاء : {date}")
    