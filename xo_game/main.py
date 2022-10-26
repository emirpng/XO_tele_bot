import telebot
import random
import keyboards as key
from config import config as cfg

bot = telebot.TeleBot(cfg.BOT_TOKEN)
fld = list(range(1, 10))

x = chr(10060)
o = chr(11093)
player = x
count = 9


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
	
	print('"start" is running')
	
	bot.send_message(message.chat.id,
		f"Приветствую тебя, {message.from_user.first_name} {message.from_user.last_name}!!! Сыграем в крестики-нолики?!")
	bot.send_message(message.chat.id, f'Для начала игры нажмите кнопку {chr(128071)}', reply_markup=key.start_game)


@bot.callback_query_handler(func=lambda call: True)
def game(call):
	global fld, player, count
	
	print(f'"game" is running.')
	
	if call.data == 'game':
		fld = list(range(1, 10))
		count = 9
		player = player_starter()
		bot.send_message(call.message.chat.id, show_field(fld))
		msg = bot.send_message(call.message.chat.id, f"Начинает игрок {player}")
		bot.register_next_step_handler(msg, game_handler)
	else:
		bot.send_message(message.chat.id, 'Я не понимаю тея...')


def game_handler(message):
	
	print(f'"game handler" is running. Request text: {message.text}')
	
	global player, count, fld
	move = message.text
	if not move.isdigit():
		
		print(f'"not move.isdigit" running. Request text: {message.text}')
		
		msg = bot.send_message(message.chat.id, 'Некорректный ввод, введите цифру от 1 до 9')
		bot.register_next_step_handler(msg, game_handler)
	elif message.text == '/game':
		bot.register_next_step_handler(message.chat.id, cancel)
	else:
		
		print(f'"move.isdigit" running. Request text: {message.text}')
		
		move = int(move)
		if move not in fld:
			print(f'"move not in fld" is running. Request text: {message.text}')
			msg = bot.send_message(message.chat.id, "Введите другую не занятую цифру.")
			bot.register_next_step_handler(msg, game_handler)
		else:
			
			print(f'"move in fld" is running. Request text: {message.text}')
			
			fld.insert(fld.index(move), player)
			fld.remove(move)
			if check_win(fld):
				
				print(f'"check_win" is running. Request text: {message.text}')
				
				bot.send_message(message.chat.id, show_field(fld))
				bot.send_message(message.chat.id, f"{player} - CHAMPION{chr(127942)}{chr(127881)}")
				bot.send_message(message.chat.id, f"{message.from_user.first_name} {message.from_user.last_name} сыграем еще?! /game")
				return
			player = o if player == x else x
			count -= 1
			msg = bot.send_message(message.chat.id, f'ход игрока {player} \n{show_field(fld)}' )
			bot.register_next_step_handler(msg, game_handler) 

	if count == 0:
		bot.send_message(chat_id, f"Draw {chr(129309)}")
		return


@bot.message_handler(commands=["cancel"])
def cancel(message):
	
	print('cancel running')
	
	bot.send_message(message.chat.id, 'До свидания!!')
	return bot.stop_polling()


if __name__ == '__main__':
	print('server start')
	bot.enable_save_next_step_handlers(delay=2)
	bot.load_next_step_handlers()
	bot.infinity_polling()

