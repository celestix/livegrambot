import telebot
import sqlite3
db = sqlite3.connect('users.db', check_same_thread=False)
sql = db.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS USERS(
    user_id INTEGER,
    first_name VARCHAR,
    messageid INT,
    message VARCHAR)''')
    
import config

bot = telebot.TeleBot("1297441208:AAHiknb7UcAXgHIFTcwpjw5Tj5iplqI3d0Q")

@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_message(message.chat.id, config.start)
    except Exception as e:
        print(str(e))
@bot.message_handler(content_types=['text'])
def text(message):
    try:
        if message.from_user.id != config.main_id:
            q = bot.forward_message(config.main_id, message.chat.id, message.message_id)
            sql.execute("INSERT OR IGNORE INTO USERS VALUES(?,?,?,?)",(message.from_user.id,message.from_user.first_name, q.message_id, message.text))
            db.commit()
            bot.send_message(message.chat.id, config.text_message)
            print(message.message_id)
        elif message.from_user.id == config.main_id:
            if message.reply_to_message is None:
                bot.forward_message(config.main_id, message.chat.id, message.message_id)
                sql.execute("INSERT INTO USERS VALUES(?,?,?,?)",(message.from_user.id,message.from_user.first_name, message.message_id, message.text))
                db.commit()
                bot.send_message(message.chat.id, config.text_message)
            elif message.reply_to_message is not None:
                print(message.reply_to_message.message_id)
                sql.execute("SELECT user_id FROM USERS WHERE messageid = ?",(message.reply_to_message.message_id,))
                db.commit()
                Lusers = sql.fetchall()
                for i in Lusers:
                    print(i[0])
                    bot.send_message(i[0], message.text)
    except Exception as e:
        print(str(e))        
                
#photo #stikeri #video        
@bot.message_handler(content_types=['photo','sticker','video','audio','voice','location','animation','contact','document'])
def other(message):
    try:
        if message.from_user.id != config.main_id:
            q = bot.forward_message(config.main_id, message.chat.id, message.message_id)
            sql.execute("INSERT OR IGNORE INTO USERS VALUES(?,?,?,?)",(message.from_user.id,message.from_user.first_name, q.message_id, message.text))
            db.commit()
            bot.send_message(message.chat.id, config.text_message)
            print(message.message_id)
        elif message.from_user.id == config.main_id:
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
                        bot.send_photo(i[0], message.photo[-1].file_id)
                    elif message.content_type == "video":
                        bot.send_video(i[0], message.video.file_id)
                    elif message.content_type == "sticker":
                        bot.send_sticker(i[0], message.sticker.file_id)
                    elif message.content_type == "audio":
                        bot.send_audio(i[0], message.audio.file_id)
                    elif message.content_type == "voice":
                        bot.send_voice(i[0], message.voice.file_id)
                    elif message.content_type == "document":
                        bot.send_document(i[0], message.document.file_id)
                    elif message.content_type == "location":
                        bot.send_location(i[0], message.location)
                    elif message.content_type == "animation":
                        bot.send_animation(i[0], message.animation.file_id)
                    elif message.content_type == "contact":
                        bot.send_contact(i[0], message.contact.file_id)
    except Exception as e:
        print(str(e))
bot.polling(none_stop=True)