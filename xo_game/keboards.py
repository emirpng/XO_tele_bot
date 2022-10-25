from telebot import types

# кнопка запуска игры
start_game = types.InlineKeyboardMarkup(row_width=1)
button = types.InlineKeyboardButton(text="Начать игру.", callback_data="xo")
start_game.add(button)
