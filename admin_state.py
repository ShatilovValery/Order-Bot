from aiogram.dispatcher.filters.state import StatesGroup, State


class AnswerState(StatesGroup):
    answer = State()
    user_id = State()