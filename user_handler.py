from config import dp, bot, ADMIN_ID_TG
from aiogram.dispatcher import FSMContext
from aiogram import types, filters
from user_keyboards import menu_key
from user_state import OrderState, QuastionState
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_save, get_data
from random import randint
from admin_state import AnswerState
from datetime import datetime

#Обработчик команды старт
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    id = message.from_user.id
    await bot.send_message(chat_id=id, text="""```
• This bot is made in order to simplify the interaction of the customer with the developer,
• Nо ads and various kinds of spam
• The bot is absolutely FREE


P.S. Developers🦧```""", parse_mode=types.ParseMode.MARKDOWN)
    await bot.send_message(chat_id=id, text="```Hi I'm your personal manager!```", parse_mode=types.ParseMode.MARKDOWN, reply_markup=menu_key)
    
    

#Обработчик команды меню
@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    id = message.from_user.id
    await bot.send_message(chat_id=id, text="```Hi I'm your personal manager!```", parse_mode=types.ParseMode.MARKDOWN, reply_markup=menu_key)


#Обработчик колбэков из инлайн кнопок
@dp.callback_query_handler(filters.Regexp(regexp=r'^menu_'))
async def hold_handler(callback: types.CallbackQuery):
    data = callback.data
    if data == 'menu_project':
        await callback.message.edit_text(text="""```
This project was born in order to gather a large community in the field of orders
The goal of this project is to ensure fast interaction of the client with the developer anywhere in the world
You will say that there is a freelance exchange!
But telegram bot is much faster and more convenient. Also an advantage is the absence of unnecessary elements, such as pictures, a lot of incomprehensible tabs with different sections, everything is very concise and clear!
There is a task, there is a solution!
You can place an order from any device and from anywhere in the world where there is Internet!
At the moment, we work only in one area and fulfill only programming orders, but in the future we want to find people from other areas, thereby attracting people from other areas!```""", reply_markup=menu_key, parse_mode=types.ParseMode.MARKDOWN)
    elif data == 'menu_order':
        await callback.message.answer(text="Write the name of the project")
        await OrderState.name.set()
    elif data == 'menu_support':
        await callback.message.answer(text="support")
    elif data == 'menu_question':
        await callback.message.answer(text="Ask a question")
        await QuastionState.quastion.set()


@dp.callback_query_handler(filters.Regexp(regexp=r'^answer_'))
async def answer_to_user(callback: types.CallbackQuery):
    await callback.message.answer(text="Введите ответ на вопрос!")
    quastion_id = callback.data.split('_')[1]
    AnswerState.user_id = quastion_id
    await AnswerState.answer.set()


@dp.message_handler(state=AnswerState.answer)
async def answer_state_set(messsage: types.Message, state: FSMContext):
    await state.update_data(answer=messsage.text)
    data = await state.get_data('DB/quastions.json')
    all_q = get_data('DB/quastions.json')
    q = all_q[AnswerState.user_id]
    await messsage.answer(text="Ответ отправлен!")
    await bot.send_message(chat_id=q['from'], text=f"The answer to your question: {q['quastion']}\n\nAnswer: {data['answer']}\n\nDevelopers🦧")
    await state.finish()


#Обработчик вопроса который задает юзер
#Handler for the question asked by the user
@dp.message_handler(state=QuastionState.quastion)
async def quastion(messsage: types.Message, state: FSMContext):
    await state.update_data(quastion=messsage.text)
    user = messsage.from_user
    _messsage = f"Новый вопрос!\nОт: {user.username}\nВопрос: {messsage.text}"
    all_q = get_data('DB/quastions.json')
    id = randint(10000, 999999)
    all_q[id] = {'from': user.id, 'time': str(datetime.now()), 'quastion': messsage.text}
    db_save('DB/quastions.json', all_q)
    answer_q = InlineKeyboardMarkup(row_width=1)
    button_with_id = InlineKeyboardButton(text="Ответить", callback_data=f'answer_{id}')
    answer_q.add(button_with_id)
    await bot.send_message(chat_id=ADMIN_ID_TG, text=_messsage, reply_markup=answer_q)
    await bot.send_message(chat_id=messsage.from_user.id, text='Thank you for your question!\nThe answer will come within a few minutes')
    await state.finish()


#Обработчик состояние имени заказа
@dp.message_handler(state=OrderState.name)
async def oreder_name(messsage: types.Message, state: FSMContext):
    await state.update_data(name=messsage.text)
    await bot.send_message(chat_id=messsage.from_user.id, text='Briefly describe the idea of ​​the project')
    await OrderState.next()


#Обработчик состояние описания заказа
@dp.message_handler(state=OrderState.descrition)
async def oreder_description(messsage: types.Message, state: FSMContext):
    await bot.send_message(chat_id=messsage.from_user.id, text='What amount do you expect?')
    await state.update_data(descrition=messsage.text)
    await OrderState.next()


#Обработчик состояние цены заказа
@dp.message_handler(state=OrderState.price)
async def oreder_price(messsage: types.Message, state: FSMContext):
    user = messsage.from_user
    await bot.send_message(chat_id=messsage.from_user.id, text='Thank you for the order!\nOur developer will contact you within 5-10 minutes)')
    await state.update_data(price=messsage.text)
    order = await state.get_data()
    all_orders = get_data()
    if user.username == None:
            await bot.send_message(chat_id=messsage.from_user.id, text="""```
It looks like you don't have a username specified
In this case, we recommend contacting the developer immediately```
Developer Contact - @raktor_0101""", parse_mode=types.ParseMode.MARKDOWN)
    messsage = f"Новый заказ!\nОт: https://t.me/{user.username}\nId: {user.id}\nТема: {order['name']}\nОписание: {order['descrition']}\nЦена: {order['price']}$"
    await bot.send_message(chat_id=ADMIN_ID_TG, text=messsage)
    await state.finish()
    all_orders['ORDERS'][randint(100000000, 999999999999)] = {"user": {'user_name': user.username,'id': user.id}, 
                                                              "order": {"title": order['name'], 
                                                              "description": order['descrition'], 
                                                              "price": order['price'], "status": ""}}
    db_save(data=all_orders)