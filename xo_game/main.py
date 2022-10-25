import telebot
import random
from config import config
from telebot import types

bot = telebot.TeleBot(config.BOT_TOKEN)

fld = list(range(1, 10))

x = chr(10060)
o = chr(11093)
player = x
count = 9
CHOICE = 0


def player_starter():
	return random.choice([x, o])


def show_field(field):
	txt = ''
	for i in range(len(field)):
		if not i % 3:
			txt += f'\n{"-" * 15}\n'
		txt += f'{field[i]:^8}'
	txt += f"\n{'-' * 15}"
	return txt


def check_win(field):
	win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
														(0, 4, 8), (2, 4, 6))
	n = [
		field[x[0]] for x in win_coord if field[x[0]] == field[x[1]] == field[x[2]]
	]
	return n[0] if n else n


@bot.message_handler(commands=["start"])
def start(message):
	bot.send_message(
		message.chat.id,
		f"Приветствую тебя, {message.from_user.first_name} {message.from_user.last_name}!!! Сыграем в крестики-нолики?!"
	)
	
	bot.send_message(message.chat.id,text="Для начала игры нажми кнопку")
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	button = types.InlineKeyboardButton(text="Начать игру.", callback_data="xo")
	keyboard.add(button)
	bot.send_message(message.chat.id, 'Играем...', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == 'xo')
def game(callback_query: types.CallbackQuery):
	global fld, player, count
	fld = list(range(1, 10))
	count = 9
	player = player_starter()
	bot.answer_callback_query(callback_query.id)
	bot.send_message(callback_query.from_user.id, show_field(fld))
	return CHOICE


@bot.message_handler(content_types=['text'])
def game_msg_handler(message):
	global player, count
	try:
		move = message.text
		chat_id = message.chat.id
		move = int(move)
		if move not in fld:
			bot.send_message(chat_id, "Введите другую не занятую цифру.") 
		else:
			fld.insert(fld.index(move), player)
			fld.remove(move)
			bot.send_message(chat_id, show_field(fld))
			bot.send_message(chat_id, f'ход игрока {player}')
			if check_win(fld):
				bot.send_message(chat_id, f"{player} - CHAMPION{chr(127942)}{chr(127881)}")
				bot.send_message(
					message.chat.id,
					f"{message.from_user.first_name} {message.from_user.last_name} сыграем еще?! /begin"
				)
				return
			player = o if player == x else x
			count -= 1
	except:
		bot.send_message(chat_id, 'некорректный ввод, введите цифру от 1 до 9')

	if count == 0:
		bot.send_message(chat_id, f"Draw {chr(129309)}")
		return


'''
@bot.message_handler(commands=["cancel"])
def cancel(message):
    bot.send_message(message.chat.id, 'Bye!!')
    return
'''

if __name__ == '__main__':
	print('server start')
	bot.polling()

