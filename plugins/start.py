from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.types import ChatPermissions
import time

button1 = InlineKeyboardButton('ضيفني لـ مجموعتك 🧚🏻‍♀️', url='t.me/raadsecurity_bot?startgroup=Commands&admin=ban_users+restrict_members+delete_messages+add_admins+change_info+invite_users+pin_messages+manage_call+manage_chat+manage_video_chats+promote_members')
button2 = InlineKeyboardButton('تحديثاتي 🍹', url='t.me/Raad_Updates')

raw1 = [button1, button2]

keyboard = [raw1]
board = InlineKeyboardMarkup(keyboard)

@app.on_message(filters.text & filters.private)
def v(app,message):
    if (message.text == "/start"):
            message.reply('''
⇜ أهلين فيك ياحلو انا بوت اسمي شهد

⇜ اختصاصي إدارة المجموعات وحمايتها من التفليش والخ....
⇜ كت تويت ، ساوند ، بحث ، وأشياء كثير
⇜عشان تفعلني ارفعني مشرف وأرسل تفعيل
''', parse_mode=enums.ParseMode.MARKDOWN, reply_markup=board)

