import telebot
import sqlite3
from plugins.ban import blocked
import time
#db = sqlite3.connect('users.db', check_same_thread=False)
#sql = db.cursor()
from plugins.unban import unblocked
from content.text import text
from content.other import other
from plugins.start import start
from plugins.everyone_message import message_everyone

def create_db_new():
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute('''CREATE TABLE IF NOT EXISTS USERS(
        user_id INTEGER,
        first_name VARCHAR,
        messageid INT,
        message VARCHAR)''')
    sql.execute('''CREATE TABLE IF NOT EXISTS blocked(
        user_id INT)''')
    sql.execute('''CREATE TABLE IF NOT EXISTS user(
        user_id INT)''')
    sql.close()
    db.close()
create_db_new()
    
import config
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start2(message):
    start(message)
@bot.message_handler(commands=["ban"])
def bloc(message):
    blocked(message)
@bot.message_handler(commands=["unban"])
def some(message):
    unblocked(message)
@bot.message_handler(commands=["admin_message"])
def reklama(message):
    if message.chat.id == config.main_id:
        bot.send_message(message.chat.id, "your message to be sent: ")
        bot.register_next_step_handler(message, textrek)
    else:
        pass
def textrek(message):
    message_everyone(message)
@bot.message_handler(content_types=['text'])
def tex(message):
    text(message)
#photo #stikeri #video        
@bot.message_handler(content_types=['photo','sticker','video','audio','voice','location','animation','contact','document','dice','poll'])
def other2(message):
    other(message)
bot.polling(none_stop=True)