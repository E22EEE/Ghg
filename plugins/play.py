import pyrogram
from pyrogram import filters,Client as app,enums
import asSQL
from asSQL import Client as c5

data = c5("protect")
db = data['love']
db.create_table()

@app.on_message(filters.group & filters.text , group = 5)
def r1(app,msg):
    if msg.reply_to_message and msg.text == "زواج":
        if msg.reply_to_message.from_user.id == app.get_me().id:
            return
        if msg.reply_to_message.from_user.id == msg.from_user.id:
            return
        if db.get(f"is_user_marriage_{msg.chat.id}_{msg.from_user.id}"):
            from_who = db.get(f"is_user_marriage_{msg.chat.id}_{msg.from_user.id}")['husband']
            wife = db.get(f"is_user_marriage_{msg.chat.id}_{msg.from_user.id}")['wife']
            
            return msg.reply("⇜ هيييييه! ولي منا انت متزوج!")
        if db.get(f"is_user_marriage_{msg.chat.id}_{msg.reply_to_message.from_user.id}"):
            return msg.reply("⇜ متزوجه هذي!")
        else:
            wife = msg.reply_to_message.from_user.id
            wife_name = msg.reply_to_message.from_user.first_name
            husband = msg.from_user.id
            husband_name = msg.from_user.first_name
            d = {"husband": husband,"wife": wife,"wife_name":wife_name,"husband_name":husband_name,"group":msg.chat.id,}
            db.set(f"is_user_marriage_{msg.chat.id}_{msg.from_user.id}",d)
            db.set(f"is_user_marriage_{msg.chat.id}_{wife}",d)
            return msg.reply(f"⇜ مبرووك! عقدت زواجكم!!:\n\n⇜ الزوجه: {msg.reply_to_message.from_user.mention} .\nالزوج: {msg.from_user.mention}\n ..")
    if msg.reply_to_message and msg.text == "طلاق" and db.get(f'is_user_marriage_{msg.chat.id}_{msg.from_user.id}'):
        if msg.reply_to_message.from_user.id == app.get_me().id:
            return
        if msg.reply_to_message.from_user.id == msg.from_user.id:
            return
        if db.get(f"is_user_marriage_{msg.chat.id}_{msg.reply_to_message.from_user.id}"):
            
            from_who = db.get(f"is_user_marriage_{msg.chat.id}_{msg.reply_to_message.from_user.id}")['husband']
            wife = db.get(f"is_user_marriage_{msg.chat.id}_{msg.reply_to_message.from_user.id}")['wife']
            if wife == msg.from_user.id:
                return msg.reply("الطلاق للمتزوج ..")
            if from_who == msg.from_user.id:
                db.delete(f"is_user_marriage_{msg.chat.id}_{msg.reply_to_message.from_user.id}")
                db.delete(f"is_user_marriage_{msg.chat.id}_{msg.from_user.id}")
                return msg.reply(f"⇜ طلقتك من  {msg.reply_to_message.from_user.mention}")
            else:
                pass
        else:

            pass
    if msg.reply_to_message and msg.text == "خلع" and db.get(f'is_user_marriage_{msg.chat.id}_{msg.from_user.id}'):
        if msg.reply_to_message.from_user.id == app.get_me().id:
            return
        if msg.reply_to_message.from_user.id == msg.from_user.id:
            return
        if db.get(f"is_user_marriage_{msg.chat.id}_{msg.reply_to_message.from_user.id}"):
            
            from_who = db.get(f"is_user_marriage_{msg.chat.id}_{msg.reply_to_message.from_user.id}")['wife']
            wife = db.get(f"is_user_marriage_{msg.chat.id}_{msg.from_user.id}")['husband']
            if wife == msg.from_user.id:
                return msg.reply("⇜ الخلع للزوجات فقط ..")
            if from_who == msg.from_user.id:
                db.delete(f"is_user_marriage_{msg.chat.id}_{msg.reply_to_message.from_user.id}")
                db.delete(f"is_user_marriage_{msg.chat.id}_{msg.from_user.id}")
                return msg.reply(f"⇜ خلعتك من  {msg.reply_to_message.from_user.mention}")
            else:
                return msg.reply("للاسف مو زوجتك")
        else:
            pass
    if msg.text == "طلاق":
        c = db.keys()
        for i in c:
            if db.get(i)['husband'] == msg.from_user.id:
                wife = db.get(i)['wife_name']
                db.delete(i)
                return msg.reply(f"طلقتك من زوجتك {wife}")
            else:
                pass
        return
    if msg.text == "خلع":
        c = db.keys()
        for i in c:
            if db.get(i)['wife'] == msg.from_user.id:
                husband = db.get(i)['husband_name']
                db.delete(i)
                return msg.reply(f"خلعتك من زوجتك {husband}" )
            else:
                pass
        return
