
from pyrogram import Client
from pyrogram import  filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions

from asSQL import Client as cl

data = cl("protect")
db = data['data']
db.create_table()
db.set("botname",['شهد','بوت'])
db.set("bad_words",['fuck','عير','طيز','زب','كسمك','كسختك','طيزك','مص', "عاهرة", "قحبه", "شرموطه", "قحبة", "شرموطة", "فك",'كسمك','كسعمتك','كسختك','عيري','اير','عير','زب','زوب','كسي','طيز','امك','خالتك','مص','كسك','مصلي','موطه','موطة','موطلي','انيج امك','كسختك','عير باختك','عير بامك','عير بيك','بلاع','نيج','نيجني','انيجك','امك الكحبه','اختك الكحبه','تيل بيك','تيل','اه','سكسي','سكس','sex','+18','نيجه','مصه','كحبه','كحبه','امك تنيج','اختك تنيج','خالتك الشكرا','خالتك الشكره','خالتك الشكرة','وردي','ما اتحمل','كله لو بس الراس','مصيلي','ااه','اهه','🍑'])

plugins = dict(root="plugins")

Client("raad",
api_id=1263966,
api_hash="6ae148a39b2074da28fa7e98c7f7e094",
bot_token="5939440211:AAF4l2owVIORseALk8E_t23oFqPmOqIfpfU", plugins=plugins).run()
