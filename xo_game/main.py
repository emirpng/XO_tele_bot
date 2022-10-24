import telebot
from config import config

bot = telebot.TeleBot(config.BOT_TOKEN)


fld = list(range(1, 10))
x = chr(10060)
o = chr(11093)
count = 9
player = x
CHOICE = 0


def show_field(field):
    txt = ''
    for i in range(len(field)):
        if not i % 3:
            txt += f'\n{"-" * 25}\n'
        txt += f'{field[i]:^8}'
    txt += f"\n{'-' * 25}"
    return txt


def check_win(field):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    n = [field[x[0]] for x in win_coord if field[x[0]] == field[x[1]] == field[x[2]]]
    return n[0] if n else n

@bot.message_handler(commands=["start"])
def start(message):
    global fld, player, count
    fld = list(range(1, 10))
    count = 9
    player = x
    bot.send_message(message.chat.id, f"Приветствую тебя {message.from_user.id}!!! Сыграем в крестики-нолики?!")
    bot.send_message(message.chat.id, show_field(fld))
    bot.send_message(message.chat.id, f'Go first {chr(10060)}')
    return CHOICE

@bot.message_handler(content_types=['text'])
def choice(message):
    global player, count
    move = message.text
    chat_id = message.chat.id
    move = int(move)
    if move not in fld:
        bot.send_message(chat_id, "Incorrect input{chr(9940)}\nTry again")
    else:
        fld.insert(fld.index(move), player)
        fld.remove(move)
        bot.send_message(chat_id, show_field(fld))
        if check_win(fld):
            bot.send_message(chat_id, f"{player} - CHAMPION{chr(127942)}{chr(127881)}")
            return bot.stop_bot()
        player = o if player == x else x
        count -= 1
    if count == 0:
        bot.send_message(chat_id, f"Draw {chr(129309)}")
        return bot.stop_bot()

@bot.message_handler(commands=["cancel"])
def cancel(message):
    bot.send_message(message.chat.id, 'Bye!!')
    return bot.stop_bot()


if __name__ == '__main__':
    print('server start')
    bot.polling()


