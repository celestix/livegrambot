import telebot
import sqlite3
import config

bot = telebot.TeleBot(config.TOKEN)
def message_everyone(message):
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT user_id FROM user")
    Lusers = sql.fetchall()
    for i in Lusers:
        try:
            if message.content_type == "text":
                #text
                tex = message.text
                bot.send_message(i[0], tex)
            elif message.content_type == "photo":
                #photo
                capt = message.caption
                photo = message.photo[-1].file_id
                bot.send_photo(i[0], photo, caption=capt)
            elif message.content_type == "video":
                #video
                capt = message.caption
                photo = message.video.file_id
                bot.send_video(i[0], photo)
            elif message.content_type == "audio":
                #audio
                capt = message.caption
                photo = message.audio.file_id
                bot.send_audio(i[0], photo, caption=capt)
            elif message.content_type == "voice":
                #voice
                capt = message.caption
                photo = message.voice.file_id
                bot.send_voice(i[0], photo, caption=capt)
            elif message.content_type == "animation":
                #animation
                capt = message.caption
                photo = message.animation.file_id
                bot.send_animation(i[0], photo, caption=capt)
            elif message.content_type == "document":
                #document
                capt = message.caption
                photo = message.document.file_id
                bot.send_document(i[0], photo, caption=capt)
        except:
            print("error!!")
    sql.close()
    db.close()