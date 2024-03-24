from aiogram.dispatcher.filters.state import StatesGroup, State


#Класс сотояний заказа
#Order status class
class OrderState(StatesGroup):
    name = State()
    descrition = State()
    price = State()

#Класс сотояний вопроса
#Class of question states
class QuastionState(StatesGroup):
    quastion = State()