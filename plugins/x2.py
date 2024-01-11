from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions
import time
from asSQL import Client as cl
from .is_admin import admin,add_msg,owner
data = cl("protect")
db = data['data']
import speech_recognition as sr
import subprocess

def transcribe_audio(audio_file_path):
    r = sr.Recognizer()
    
    if audio_file_path.endswith(( ".mp3", ".wav")):
        supported_format = True
    else:
        supported_format = False
    
    if not supported_format:
        import os
        wav_file_path = audio_file_path.rsplit(".", 1)[0] + ".wav"
        process = subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-y", "-i", audio_file_path, wav_file_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        os.system("clear")
        audio_file_path = wav_file_path
    
    with sr.AudioFile(audio_file_path) as source:
        audio = r.record(source)
    try:
        transcribed_text = r.recognize_google(audio, language="ar-AR", show_all=True)
        
        transcribed_text = transcribed_text['alternative'][0]['transcript']
    
    except Exception as e:
        transcribed_text = False
    
    return transcribed_text
@app.on_message(filters.text & filters.group , group =72)
def v(app,message):
    
    if (message.text == "وش يقول؟" or message.text == "what?") and  message.reply_to_message.voice:
        app.download_media(message.reply_to_message.voice.file_id,file_name="a.ogg")
        what = transcribe_audio("downloads/a.ogg")
        if what:
            message.reply(f"يقول: {what}")
        else:
            message.reply("مافهمت وش يقول!!")
