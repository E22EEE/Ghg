from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Client("5939440211:AAF4l2owVIORseALk8E_t23oFqPmOqIfpfU") 

@app.on_message(filters.text("السورس"))
def send_source(message):
    url = 'https://t.me/telebote/52'
    chat_id = message.chat.id
    app.send_photo(chat_id=chat_id, photo=url, caption="")

    keyboard = InlineKeyboardMarkup(row_width=1)
    channel_button = InlineKeyboardButton("قناة السورس", url="http://t.me/Tepthon")
    developer_button = InlineKeyboardButton("مطور السورس", url="http://t.me/PPF22")
  
    keyboard.add(channel_button, developer_button)
                                                      
    app.send_message(chat_id, """اسم المطور - ꪔ᥆ɦᥲꪔꪔᥲძ <\>
يوزر المطور - @PPF22
ايدي المطور - 1260465030""", reply_markup=keyboard) 


@app.on_message(filters.text("سورس"))
def send_source(message):

    keyboard = InlineKeyboardMarkup(row_width=1)
    channel_button = InlineKeyboardButton("قناة السورس", url="http://t.me/Tepthon")
    developer_button = InlineKeyboardButton("مطور السورس", url="http://t.me/PPF22")
  
    keyboard.add(channel_button, developer_button)
                                                      
    app.send_message(chat_id, """𝑾𝒆𝒍𝒄𝒐𝒎𝒆 𝑻𝒐 𝑺𝒐𝒖𝒓𝒄𝒆 𝑺𝒉𝒂𝒉𝒂𝒅  ❤️.
 
- Dev @PPF22""", reply_markup=keyboard) 


app.run()