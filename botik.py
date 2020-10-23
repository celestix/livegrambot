# THIS BOT WAS MADE WITH EDUCODER IN TELEGRAM
#DONATE US
#FOR ANY QUESTIONS CONTACT @coder2020 in telegram



#Copyright educoder. Software has a license
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

bot = telebot.TeleBot("TOKEN")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, config.start)
@bot.message_handler(content_types=['text','photo','video'])
def text(message):
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
                bot.send_message(i[0], message.text)
bot.polling(none_stop=True)
