import telebot
import sqlite3
db = sqlite3.connect('users.db', check_same_thread=False)
sql = db.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS USERS(
    user_id INTEGER,
    first_name VARCHAR,
    messageid INT,
    message VARCHAR)''')
sql.execute('''CREATE TABLE IF NOT EXISTS blocked(
    user_id INT)''')
    
import config
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_message(message.chat.id, config.start)
    except Exception as e:
        print(str(e))
@bot.message_handler(commands=["ban"])
def blocked(message):
    try:
        if message.from_user.id == config.main_id:
            #fromm = str(message.from_user.id)
            #name = message.from_user.first_name
            sql.execute("SELECT user_id FROM USERS WHERE messageid = ?",(message.reply_to_message.message_id,))
            db.commit()
            Lusers = sql.fetchall()
            for i in Lusers:
                print(i[0])
                sql.execute("SELECT user_id FROM blocked WHERE user_id = ?",(i[0],))
                if sql.fetchone() is None:
                    bot.send_message(i[0],config.ban)
                    bot.send_message(message.chat.id, "you blocked " + str(i[0]))
                    sql.execute("INSERT INTO blocked VALUES (?)",(i[0],))
                    db.commit()
        else:
            bot.send_message(message.chat.id, "you are not admin!")
    except Exception as ee:
        print("error in block" + str(ee))
@bot.message_handler(commands=["unban"])
def unblocked(message):
    try:
        if message.from_user.id == config.main_id:
            sql.execute("SELECT user_id FROM USERS WHERE messageid = ?",(message.reply_to_message.message_id,))
            db.commit()
            Lusers = sql.fetchall()
            for i in Lusers:
                print(str(i[0]) + " mine")
                sql.execute("SELECT user_id FROM blocked WHERE user_id = ?",(i[0],))
                db.commit()
                print("unbanning")
                sql.execute("DELETE FROM blocked WHERE user_id = ?",(i[0],))
                db.commit()
                bot.send_message(i[0],"you were unblocked")
                bot.send_message(message.chat.id, "you unblocked " + str(i[0]))
        else:
            bot.send_message(message.chat.id, "you are not admin!")
    except Exception as ee:
        print("error in block" + str(ee))
@bot.message_handler(content_types=['text'])
def text(message):
    try:
        sql.execute("SELECT user_id FROM blocked WHERE user_id = ?",(message.from_user.id,))
        db.commit()
        if sql.fetchone() is not None:
            bot.send_message(message.chat.id, config.banned)
        else:
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
            sql.execute("SELECT user_id FROM blocked WHERE user_id = ?",(message.from_user.id,))
            db.commit()
            b = sql.fetchall()
            if sql.fetchone is not None:
                bot.send_message(message.chat.id, config.banned)
            else:
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
                        bot.send_location(i[0], message.location.longitude, message.location.latitude)
                    elif message.content_type == "animation":
                        bot.send_animation(i[0], message.animation.file_id)
                    elif message.content_type == "contact":
                        bot.send_contact(i[0], message.contact.file_id)
    except Exception as e:
        print(str(e))
bot.polling(none_stop=True)