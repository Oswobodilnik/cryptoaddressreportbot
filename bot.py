import telebot # telebot

from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States
from data import save_report,get_user_rank
# States storage
from telebot.storage import StateMemoryStorage


# Starting from version 4.4.0+, we support storages.
# StateRedisStorage -> Redis-based storage.
# StatePickleStorage -> Pickle-based storage.
# For redis, you will need to install redis.
# Pass host, db, password, or anything else,
# if you need to change config for redis.
# Pickle requires path. Default path is in folder .state-saves.
# If you were using older version of pytba for pickle, 
# you need to migrate from old pickle to new by using
# StatePickleStorage().convert_old_to_new()



# Now, you can pass storage to bot.
state_storage = StateMemoryStorage() # you can init here another storage

bot = telebot.TeleBot("6255797844:AAG5b87erV7TstyJ7BLrI_jtdin-oOb8dqg",
state_storage=state_storage)


# States group.
class MyStates(StatesGroup):
    # Just name variables differently
    crypto_address = State() # creating instances of State class is enough from now
    message = State()




@bot.message_handler(commands=['start'])
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.id, MyStates.crypto_address, message.chat.id)
    bot.send_message(message.chat.id, 'Send crypto address.')
 

# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Your state was cancelled.")
    bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(state=MyStates.crypto_address)
def name_get(message):
    """
    State 1. Will process when user's state is MyStates.name.
    """
    bot.send_message(message.chat.id, 'Now write your message')
    bot.set_state(message.from_user.id, MyStates.message, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['crypto_address'] = message.text
 
 
@bot.message_handler(state=MyStates.message)
def ask_age(message):
    """
    State 2. Will process when user's state is MyStates.surname.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Your submitted data\n<b>"
               f"{data['crypto_address']}\n"
               f"{message.text}</b>")
        bot.send_message(message.chat.id, msg, parse_mode="html")
        bot.send_message(message.chat.id, "You submit that successfully")
        if message.from_user.username:
            save_report(data['crypto_address'],message.text,message.from_user.username,message.from_user.id)
        else:
            text = "No Username"
            save_report(data['crypto_address'],message.text,message.text,message.from_user.id)
    bot.delete_state(message.from_user.id, message.chat.id)




@bot.message_handler(commands=['donation'])
def start_ex(message):
    bot.send_message(message.chat.id, 'Your website link\n\naddress\naddress')


@bot.message_handler(commands=['rank'])
def start_ex(message):
    userid = message.from_user.id
    rank = get_user_rank(userid)
    bot.send_message(message.chat.id, f'Your rank is {rank}')



bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.infinity_polling(skip_pending=True)