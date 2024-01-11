from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions
import time,random
from asSQL import Client as cl
from .is_admin import admin,add_msg,owner
data = cl("protect")
db = data['data']
def rd(chat_id,text):
    rdodd = (db.get(f"group_{chat_id}_replies"))
    found = None
    info = None
    for i in rdodd:
        if f"{text}" in i:
            found = True
            info = i
        else:
            continue
    if found:
        return info
    else:
        return None
@app.on_message(filters.all & filters.group , group = 33)
def handle_messages(app, message):
    chat_id = str(message.chat.id)
    text = message.text
    t = ((time.time()))
    if message.text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            if db.key_exists(f"user_{chat_id}_{message.from_user.id}_msgs") ==1:
                pass
            else:
                db.set(f"user_{chat_id}_{message.from_user.id}_msgs",[t])
        else:
            return
    if message.sender_chat:
        return
    add_msg(chat_id,message.from_user.id,1)
    if (rd(message.chat.id,message.text)) != None:
        info = rd(message.chat.id,message.text)
        
        if info:
            if info[message.text]['type'] == "text":
                return message.reply(f"{info[message.text]['reply']}")
            else:
                file = info[message.text]['file']
                caption = info[message.text]['caption'] if info[message.text]['caption'] else "،"
                if caption and file:
                    app.send_cached_media(message.chat.id,file,caption=caption,reply_to_message_id=message.id)
    
    if db.get(f"running_rolet_{message.chat.id}"):
        info = db.get(f"running_rolet_info_{message.chat.id}")
        current_time = time.time()
        elapsed_time = current_time - float(info)
    
        if elapsed_time >= 300:
            db.delete(f"running_rolet_{message.chat.id}")
            db.delete(f"running_rolet_players_{message.chat.id}")
            db.delete(f"running_rolet_admin_{message.chat.id}")
            db.delete(f"running_rolet_info_{message.chat.id}")
            return app.send_message(chat_id=chat_id,text="يبدو ان هناك روليت مشتغلة صارلها اكثر من 5 دقايق .. مسحتها :) ")
    name = "".join(random.choice(db.get('botname') ))
    name2 = "شهد"
    bot_r = [
f"اسمي {name}","انطم","مو بوته!","اذلف","تراها زاقه","الله يعين","ياصبر الارض","هاه",name2,"؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟","تراك ازعجتنا","الله يصبرني",]
    bot_name = [
"عيونها","هلا",
"نعم","امرني ياعيوني","لبيه","قول شعندك","سم","امرني",
"هلا والله","ها يعمري",
"نييم","روحها","هاه",
"زفت",
f"الله ياخذ {name}","لبيه","ها ",f"الله يرزقك حياة غير {name} ",
"تواصل مع مدير اعمالي","سم لبيه امر",
"عيوني","؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟",]
    sb = [
"عييييييييب","عيب","ياكلب عيب","يا قليل التربيه","يا قليل الادب","؟؟؟؟؟؟","ياليت تتأدب","بقص لسانك","حاضر","ياخي عيب","؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟","استغفر الله",
   ]
    lovem = [
"يلبيييه",
"اكثر",
"يعمري",
"اعشقك",
"بدينا كذب",
"احلى من يحبني",
"يحظي والله",
"اكثر اكثر اكثرر",
"يروحي",
"اموت فيك",]
    zg = [
"عييييييييب","عيب","زق بوجهك","يا قليل التربيه","يا قليل الادب","؟؟؟؟؟؟","ياليت تتأدب","بقص لسانك","حاضر","ياخي عيب","؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟",]
    mm = [
"ابركها من ساعة","احبك","اكثر","ترا ازعجتنا","انقلع","طيب","مو اكثر مني","وبعدين ؟","جت من الله","توكل بس"]
    if text in db.get('bad_words'):
        return message.reply(random.choice(sb))
    if text == 'بوت':
       message.reply(random.choice(bot_r))
   
    if text == name2:
      message.reply(random.choice(bot_name))
   
    
    if text == 'احبك' or text == "احبج":
       message.reply(random.choice(lovem))
   
    if text == 'اكرهك':
      message.reply(random.choice(mm))
   
    if text == 'كليزق' or text == 'كلزق':
      message.reply(random.choice(zg))
   