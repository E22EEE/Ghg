from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.types import ChatPermissions
import time

from .is_admin import owner,admin,add_msg

button1 = InlineKeyboardButton('- م1', callback_data='bc1')
button2 = InlineKeyboardButton('- م2', callback_data='bc2')
button3 = InlineKeyboardButton('- م3', callback_data='bc3')
button4 = InlineKeyboardButton('- اليوتيوب', callback_data='bc4')
button5 = InlineKeyboardButton('- الالعاب', callback_data='bc5')
button6 = InlineKeyboardButton("- التسلية", callback_data="bc6")

raw1 = [button1, button2]
raw2 = [button3]
raw3 = [button4, button5]
raw4 = [button6]

keyboard = [raw1, raw2, raw3, raw4]
board = InlineKeyboardMarkup(keyboard)

@app.on_message(filters.text & filters.group , group =72)
def v(app,message):
    if (message.text == "cmds" or message.text == "الاوامر"):
      if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            message.reply('''
- اهلين فيك باوامر البوت .

 - للاستفسار : @Tepthon .
''', parse_mode=enums.ParseMode.MARKDOWN, reply_markup=board)
      else:
        return message.reply("⇜ الامر يخص ( المالك او الادمن وفوق وبس )")
        
@app.on_callback_query()
async def callback_query(app, query):
    chat_id = query.message.chat.id
    message_id = query.message.id
    if query.data == 'bc1':
      if owner(query.message.from_user.id,query.message.chat.id) or admin(query.message.from_user.id,query.message.chat.id):

        await app.edit_message_text(chat_id, message_id, '''
 - للاستفسار : @Tepthon .

- (اوامر الرفع والتنزيل) .

- رفع - تنزيل مشرف .
- تنزيل الكل - بدون رد - لتنزيل جميع الادمنية .

- (اوامر المسح) .

- مسح محظورين .
- مسح مقيدين .
- مسح - بالرد - مسح رسالة .
- تنظيف - تنظيف الرسائل .
- مسح ترحيب .

- (اوامر الطرد الحظر الكتم) .

- حظر - بالرد .
- طرد - بالرد .
- كتم - بالرد .
- تقييد - بالرد .

- فك حظر - بالرد .
- فك كتم - بالرد .
- فك تقييد - بالرد .
- كشف البوتات .

- (اوامر النطق) .

- انطق - النص .
- وش يقول؟ - قريبا .

- (اوامر اخرى) .

- الرابط .
- ايدي .
- افتاري .
- ايدي - بالرد .
- انشاء رابط .
''', parse_mode=enums.ParseMode.MARKDOWN, reply_markup=board)
      else:
        return await query.message.reply("⇜ الامر يخص ( المالك او الادمن وفوق وبس )")

    elif query.data == 'bc2':
      if owner(query.message.from_user.id,query.message.chat.id) or admin(query.message.from_user.id,query.message.chat.id):
        await app.edit_message_text(chat_id, message_id, '''
 - للاستفسار : @Tepthon .

- (اوامر الوضع) .

- اضف ترحيب .
- اضف امر .

- (اوامر رؤية الاعدادات) .

- الادمنية .
- المالكين .
- المكتومين .
- المحظورين .
- الاعدادات .
- 

''', parse_mode=enums.ParseMode.MARKDOWN, reply_markup=board)
      else:
        return await query.message.reply("⇜ الامر يخص ( المالك او الادمن وفوق وبس )")
    elif query.data == 'bc3':
      if owner(query.message.from_user.id,query.message.chat.id) or admin(query.message.from_user.id,query.message.chat.id):
        await app.edit_message_text(chat_id, message_id, '''
 - للاستفسار : @Tepthon .

- (اوامر الردود) .

- الردود - تشوف كل الردود المضافة .
- اضف رد - عشان تضيف رد .
- حذف رد - عشان تحذف رد .
- مسح الردود - لمسح جميع الردود المضافه .

- (اوامر القفل والفتح) .

- قفل - فتح التعديل .
- قفل - فتح الفيديوهات .
- قفل - فتح الصور .
- قفل - فتح الملصقات .
- قفل - فتح الملفات .
- ثقل - فتح المتحركات .
- قفل - فتح الدردشة .
- قفل - فتح الروابط .
- قفل - فتح الاشعارات .
- قفل - فتح التكرار .
- قفل - فتح التوجيه .
- قفل - فتح الانلاين .
- قفل - فتح الجهات .
- قفل - فتح السب .

- (اوامر التفعيل والتعطيل) .

- تفعيل - تعطيل الترحيب .
- تفعيل - تعطيل الايدي .

''', parse_mode=enums.ParseMode.MARKDOWN, reply_markup=board)
      else:
        return await query.message.reply("⇜ الامر يخص ( المالك او الادمن وفوق وبس )")
    elif query.data == 'bc5':
        pass
    elif query.data == 'bc4':
     if owner(query.message.from_user.id,query.message.chat.id) or admin(query.message.from_user.id,query.message.chat.id):
        await app.edit_message_text(chat_id, message_id, '''
 - للاستفسار : @Tepthon .

- (اليوتيوب) .

- تفعيل اليوتيوب .
- تعطيل اليوتيوب .

- (البحث والتحميل) .

- يوت اسم الاغنية .
- بحث اسم الاغنية او الفيديو .

''', parse_mode=enums.ParseMode.MARKDOWN, reply_markup=board)
    else:
        return await query.message.reply("⇜ الامر يخص ( المالك او الادمن وفوق وبس )")
    if query.data == "bc6":
      if owner(query.message.from_user.id,query.message.chat.id) or admin(query.message.from_user.id,query.message.chat.id):
        await app.edit_message_text(chat_id, message_id, '''
 - للاستفسار : @Tepthon .

- (اوامر الزواج) .

- زواج - بالرد - عشان تتزوج  
- طلاق - بالرد - عشان تطلقها 
- خلع - بالرد - عشان تطلقك  
''', parse_mode=enums.ParseMode.MARKDOWN, reply_markup=board)
      else:
        return await query.message.reply("⇜ الامر يخص ( المالك او الادمن وفوق وبس )")
    else:
        pass
