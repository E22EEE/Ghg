from asSQL import Client as cl
data = cl("protect")
db = data['data']
db.create_table()

def admin(id:int,chat_id:str):
    if id in db.get(f"admins-{chat_id}"):
        return True
    else:
        return False
def owner(id:int,chat_id:str):
    if id in db.get(f"creators_{chat_id}"):
        return True
    else:
        return False
def add_msg(chat_id,user_id,count):
    if db.key_exists(f"group_{chat_id}_{user_id}_info") == 0:
        db.set(f"group_{chat_id}_{user_id}_info",{"id":user_id,"group":f"{chat_id}","msgs":0})
        return True
    else:
        d = db.get(f"group_{chat_id}_{user_id}_info")
        ns = int(d['msgs']) + int(count)
        d.update({"msgs": ns})
        db.delete(f"group_{chat_id}_{user_id}_info")
        db.set(f"group_{chat_id}_{user_id}_info",d)
        return True