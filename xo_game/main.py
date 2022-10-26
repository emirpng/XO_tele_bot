import time
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

# функция, определяет кто делает первый ход в игре
def player_starter():
	return random.choice([x, o])

# отрисовка игрового поля
def show_field(field):
	txt = ''
	for i in range(len(field)):
		if not i % 3:
			txt += f'\n{"-" * 15}\n'
		txt += f'{field[i]:^8}'
	txt += f"\n{'-' * 15}"
	return txt

# проверка на победителя
def check_win(field):
	win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
														(0, 4, 8), (2, 4, 6))
	n = [
		field[x[0]] for x in win_coord if field[x[0]] == field[x[1]] == field[x[2]]
	]
	return n[0] if n else n

# обработка команды /start, приветственное сообщение, отрисовка кнопки начала игры.
@bot.message_handler(commands=["start"])
def start(message):
	print('"start" is running')
	bot.send_message(message.chat.id,
		f"Приветствую тебя, {message.from_user.first_name} {message.from_user.last_name}!!! Сыграем в крестики-нолики?!")
	bot.send_message(message.chat.id, f'Для начала игры нажмите кнопку {chr(128071)}', reply_markup=key.start_game)

# обработка всех остальных непонятных сообщений, и отрисовка кнопки с началом игры
@bot.message_handler(content_types=['text'])
def unknown_text(message):
	bot.send_message(message.chat.id, f'Я тебя не понимаю... \nЕсли хочешь играть жми кнопку {chr(128071)}', reply_markup=key.start_game)

# Функция, обработка нажатия кнопки, "Начать игру", при нажатии её,
# приходит запрос с текстов 'game', запускается функция начала игры,
# выбор кто первый ходит.
# с помощью функции, register_next_step_handler, регистрируем этот шаг, отправляем сообщение пользователю
# и ждем от него ответ, перенаправляем на функцию game_handler.
@bot.callback_query_handler(func=lambda call: call.data == 'game')
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
		bot.send_message(call.message.chat.id, 'Я не понимаю тея...')


# отбработка игры
def game_handler(message):
	print(f'"game handler" is running. Request text: {message.text}')
	global player, count, fld
	move = message.text
	if message.text == '/cancel': # вызов функции /cancel
		bot.register_next_step_handler(message.chat.id, cancel)
	elif not move.isdigit(): # проверка ввода числа
		print(f'"not move.isdigit" running. Request text: {message.text}')
		msg = bot.send_message(message.chat.id, 'Некорректный ввод, введите цифру от 1 до 9')
		bot.register_next_step_handler(msg, game_handler) # отправляем сообщение в чат, ждем ответ и снова вызываем эту же функцию
	else:
		print(f'"move.isdigit" running. Request text: {message.text}')
		move = int(move)
		if move not in fld: # проверка наличия числа в списке
			print(f'"move not in fld" is running. Request text: {message.text}')
			msg = bot.send_message(message.chat.id, "Введите другую не занятую цифру.")
			bot.register_next_step_handler(msg, game_handler) # отправляем сообщение в чат, ждем ответ и снова вызываем эту же функцию
		else:
			print(f'"move in fld" is running. Request text: {message.text}')
			fld.insert(fld.index(move), player) # на место выбранного числа вставляем текущий символ игрока
			fld.remove(move)	# удаляем указанный номер поля из списка
			if check_win(fld):
				print(f'"check_win" is running. Request text: {message.text}')
				bot.send_message(message.chat.id, show_field(fld))
				bot.send_message(message.chat.id, f"{player} - CHAMPION{chr(127942)}{chr(127881)}")
				bot.send_message(message.chat.id, f"{message.from_user.first_name} {message.from_user.last_name} сыграем еще?! {chr(128071)}", reply_markup=key.start_game)
				return
			player = o if player == x else x
			count -= 1
			if count == 0:
				bot.send_message(message.chat.id, f"Draw {chr(129309)}")
				bot.send_message(message.chat.id,
								 f"{message.from_user.first_name} {message.from_user.last_name} сыграем еще?! {chr(128071)}",
								 reply_markup=key.start_game)
				return
			msg = bot.send_message(message.chat.id, f'ход игрока {player} \n{show_field(fld)}')
			bot.register_next_step_handler(msg, game_handler) # отправляем сообщение в чат, ждем ответ и снова вызываем эту же функцию

# завершение работы
def cancel(message):
	print('cancel is running')
	bot.send_message(message.chat.id, 'До свидания!!')
	bot.stop_bot()
	return



if __name__ == '__main__':
	print('server start')
	bot.enable_save_next_step_handlers(delay=2)
	bot.load_next_step_handlers()

	while True:
		try:
			bot.polling(none_stop=True)
		except Exception as e:
			time.sleep(2)