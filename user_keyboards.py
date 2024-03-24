from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


#клавиатура меню для пользователя
#menu keyboard for user
menu_key = InlineKeyboardMarkup(row_width=1)
info_about_bot = InlineKeyboardButton(text="About the project📖", callback_data="menu_project")
order_a_project = InlineKeyboardButton(text='Order a project📩', callback_data="menu_order")
question = InlineKeyboardButton(text="Ask a question❓", callback_data='menu_question')
menu_key.add(info_about_bot, order_a_project, question)


