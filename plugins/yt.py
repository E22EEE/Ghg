import os, time
from pyrogram import Client as app, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
from pyrogram.enums import ChatMemberStatus 
from yt_dlp import YoutubeDL
from dragonxxdlib import *
from youtube_search import YoutubeSearch as Mr_Aws
import requests
import yt_dlp
from asSQL import Client as cl
from .is_admin import owner,admin,add_msg
data = cl("protect")
db = data['data']
def stm(seconds):
    return '{:02}:{:02}:{:02}'.format(seconds // 3600, seconds % 3600 // 60, seconds % 60)

disable = []
@app.on_message(filters.command("يوت", ["&",""]),group = 20)
def yttt(app,message):
    if message.text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    if db.get(f"lock_yt_{message.chat.id}"):
        message.reply(f"⇜ عزيزي {message.from_user.mention} البحث مقفول او معطلة .")
    else:
        if len(message.text.split(None, 1)) < 2:
           return
        query  = message.text.split(None, 1)[1]
        re = Mr_Aws(query, max_results=1).to_dict()
        vid = None
        title = None
        channel = None
        try:
            
            
            info =re[0]
            vid = info['id']
            title = info['title']
            channel = info['channel']
        except Exception as e:
            print(e)
            return message.reply("⇜ صار خطأ ")
        url = f'https://youtu.be/{vid}'
        ydl_ops = {"format": "bestaudio[ext=m4a]"}
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            if int(info_dict['duration']) > 2605:
              return message.reply("**⚠️ حد التحميل نص ساعة فقط**")
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        message.reply_audio(audio=audio_file,performer=channel,title=title,duration=info_dict['duration'],caption=f"@RaadSecurity_Bot ~ {stm(info_dict['duration'])}")
        os.remove(audio_file)
@app.on_message(filters.command("بحث", ["&",""]),group = 20)
def search(app, message):
    if message.text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    if db.get(f"lock_yt_{message.chat.id}"):
        message.reply(f"⇜ عزيزي {message.from_user.mention} البحث مقفول او معطلة .")
    else:
         if len(message.text.split(None, 1)) < 2:
           return 
         user_id = message.from_user.id
         query = message.text.split(None, 1)[1]
         re = Mr_Aws(query, max_results=4).to_dict()
         buttons = []
         for r in re:
           buttons.append(
           [
           InlineKeyboardButton(
              r["title"],
              callback_data=f"{user_id}GET{r['id']}"
             )
           ])
         message.reply(
            f"**⤶ هذي نتائج بحثك عن {query} :**",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
         )
     

@app.on_message(filters.regex("^تعطيل اليوتيوب$|^تعطيل التحميل$") & filters.group, group = 21)
def dis_yt(app,message):
    e = "**⇜ اليوتيوب معطل من قبل .**"
    d = "**⇜ من 「 {} 」 \n⇜ ابشر قفلت اليوتيوب \n༄**"
    
    if message.text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
        if db.get(f'lock_yt_{message.chat.id}') == True:
            message.reply(e)
        else:
            db.set(f'lock_yt_{message.chat.id}', True)
            message.reply(d.format(message.from_user.mention))
@app.on_message(filters.regex("^تفعيل اليوتيوب$|^تفعيل التحميل$") & filters.group, group =22)
def ena_yt(app,message):
    e = "**⇜ اليوتيوب مفعل من قبل .**"
    d = "**⇜ من 「 {} 」 \n⇜ ابشر فعلت اليوتيوب \n༄**"
    
    if message.text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
        if db.get(f'lock_yt_{message.chat.id}') == False:
            message.reply(e)
        else:
            db.set(f'lock_yt_{message.chat.id}', False)
            message.reply(d.format(message.from_user.mention))
@app.on_callback_query(filters.regex("GET") , group = 23)
def get_info(app, query: CallbackQuery):
    
    user_id = query.data.split("GET")[0]
    vid_id = query.data.split("GET")[1]
    if not query.from_user.id == int(user_id):
      return query.answer("⚠️ هذا الأمر لا يخصك ", show_alert=True)
    query.message.delete()
    yt = Mr_Aws(f'https://youtu.be/{vid_id}', max_results=1).to_dict()
    title = yt[0]['title']
    url = f'https://youtu.be/{vid_id}'
    reply_markup = InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton ("صوت 💿", callback_data=f'{user_id}AUDIO{vid_id}'),
          InlineKeyboardButton ("فيديو 🎥", callback_data=f'{user_id}VIDEO{vid_id}'),
        ]
      ]
    )
    app.send_message(
       query.message.chat.id,
       f"**⤶ العنوان - [{title}]({url})**",
       disable_web_page_preview=True,
       reply_markup=reply_markup
    )
    
download = InlineKeyboardMarkup (
  [[
    InlineKeyboardButton("رعد ♪ ", url='T.me/RaadSecurity_Bot')
  ]]
)

upload = InlineKeyboardMarkup (
  [[
    InlineKeyboardButton("رعد ♪", url='T.me/RaadSecurity_Bot')
  ]]
)

error = InlineKeyboardMarkup (
  [[
    InlineKeyboardButton("⚠️", url='T.me/RaadSecurity_Bot')
  ]]
)

@app.on_callback_query(filters.regex("AUDIO") , group = 24)
def get_audii(app, query: CallbackQuery):
    
    user_id = query.data.split("AUDIO")[0]
    vid_id = query.data.split("AUDIO")[1]
    if not query.from_user.id == int(user_id):
      return query.answer("⚠️ هذا الأمر لا يخصك ", show_alert=True)
    url = f'https://youtu.be/{vid_id}'
    query.edit_message_text("**جاري التحميل ..**", reply_markup=download)
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    with yt_dlp.YoutubeDL(ydl_ops) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        if int(info_dict['duration']) > 3605:
          return query.edit_message_text("**⚠️ حد التحميل ساعة فقط**",reply_markup=error)
        audio_file = ydl.prepare_filename(info_dict)
        ydl.process_info(info_dict)
    query.edit_message_text("**جاري الإرسال ..**", reply_markup=upload)
    response= requests.get(info_dict['thumbnail'])
    with open(f"{vid_id}.png", "wb") as file:
      file.write(response.content)
    thumb = f"{vid_id}.png"
    user = app.get_users(int(user_id))
    query.message.reply_audio(
      audio_file,
      title=info_dict['title'],
      duration=int(info_dict['duration']),
      performer=info_dict['channel'],
      caption=f'• البحث من -› {user.mention}',
      thumb=thumb
    )
    doneload = InlineKeyboardMarkup (
      [[
      InlineKeyboardButton("رعد", url="RaadSecurity_Bot")
      ]]
    )
    query.edit_message_text(f"** العنوان [{info_dict['title']}]({url})**", reply_markup=doneload,disable_web_page_preview=True)
    os.remove(thumb)
    os.remove(audio_file)


@app.on_callback_query(filters.regex("VIDEO") , group = 26)
def get_video(app, query: CallbackQuery):
    
    user_id = query.data.split("VIDEO")[0]
    vid_id = query.data.split("VIDEO")[1]
    if not query.from_user.id == int(user_id):
      return query.answer("⚠️ هذا الأمر لا يخصك ", show_alert=True)
    url = f'https://youtu.be/{vid_id}'
    query.edit_message_text("**جاري التحميل ..**", reply_markup=download)
    with yt_dlp.YoutubeDL({}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        if int(info_dict['duration']) > 3605:
          return query.edit_message_text("**⚠️ حد التحميل ساعة فقط**",reply_markup=error)
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    with YoutubeDL(ydl_opts) as ytdl:
        ytdl_data = ytdl.extract_info(url, download=True)
        file_name = ytdl.prepare_filename(ytdl_data)
    query.edit_message_text("**جاري الإرسال ..**", reply_markup=upload)
    response= requests.get(info_dict['thumbnail'])
    with open(f"{vid_id}.png", "wb") as file:
      file.write(response.content)
    thumb = f"{vid_id}.png"
    user = app.get_users(int(user_id))
    query.message.reply_video(
      file_name,
      duration=int(info_dict['duration']),
      caption=f'• البحث من  -› {user.mention}',
      thumb=thumb
    )
    doneload = InlineKeyboardMarkup (
      [[
      InlineKeyboardButton("رعد", url='T.me/RaadSecurity_Bot')
      ]]
    )
    query.edit_message_text(f"**🔗 [{info_dict['title']}]({url})**", reply_markup=doneload,disable_web_page_preview=True)
    os.remove(thumb)
    os.remove(file_name)
