import telebot
import sqlite3
import config
bot = telebot.TeleBot(config.TOKEN)
def unblocked(message):
    try:
        db = sqlite3.connect('users.db', check_same_thread=False)
        sql = db.cursor()
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
        sql.close()
        db.close()
    except Exception as ee:
        print("error in block" + str(ee))