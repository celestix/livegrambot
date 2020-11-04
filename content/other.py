import telebot
import sqlite3
import config
bot = telebot.TeleBot(config.TOKEN)
def other(message):
    try:
        db = sqlite3.connect('users.db', check_same_thread=False)
        sql = db.cursor()
        if message.from_user.id != config.main_id:
            sql.execute("SELECT user_id FROM blocked WHERE user_id = ?",(message.from_user.id,))
            db.commit()
            if sql.fetchone() is not None:
                bot.send_message(message.chat.id, config.banned)
            else:
                q = bot.forward_message(config.main_id, message.chat.id, message.message_id)
                sql.execute("INSERT OR IGNORE INTO USERS VALUES(?,?,?,?)",(message.from_user.id,message.from_user.first_name, q.message_id, message.text))
                db.commit()
                bot.send_message(message.chat.id, config.text_message)
                print(message.message_id)
        elif message.chat.id == config.main_id:
            if message.reply_to_message is None:
                bot.forward_message(config.main_id, message.chat.id, message.message_id)
                sql.execute("INSERT OR IGNORE INTO USERS VALUES(?,?,?,?)",(message.from_user.id,message.from_user.first_name, message.message_id, message.text))
                db.commit()
                bot.send_message(message.chat.id, config.text_message)
            elif message.reply_to_message is not None:
                print(message.reply_to_message.message_id)
                sql.execute("SELECT user_id FROM USERS WHERE messageid = ?",(message.reply_to_message.message_id,))
                db.commit()
                Lusers = sql.fetchall()
                for i in Lusers:
                    print(i[0])
                    if message.content_type == "photo":
                        capt = message.caption
                        bot.send_photo(i[0], message.photo[-1].file_id, caption=capt)
                    elif message.content_type == "video":
                        capt = message.caption
                        bot.send_video(i[0], message.video.file_id, caption=capt)
                    elif message.content_type == "sticker":
                        bot.send_sticker(i[0], message.sticker.file_id)
                    elif message.content_type == "audio":
                        capt = message.caption
                        bot.send_audio(i[0], message.audio.file_id, caption=capt)
                    elif message.content_type == "voice":
                        capt = message.caption
                        bot.send_voice(i[0], message.voice.file_id, caption=capt)
                    elif message.content_type == "document":
                        capt = message.caption
                        bot.send_document(i[0], message.document.file_id, caption=capt)
                    elif message.content_type == "location":
                        bot.send_location(i[0], message.location.longitude, message.location.latitude)
                    elif message.content_type == "animation":
                        capt = message.caption
                        bot.send_animation(i[0], message.animation.file_id, caption=capt)
                    elif message.content_type == "contact":
                        bot.send_contact(i[0], message.contact.file_id)
        sql.close()
        db.close()
    except telebot.apihelper.ApiException:
        bot.send_message(message.chat.id, config.blocked)