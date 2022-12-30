from aiogram.dispatcher.filters.state import StatesGroup, State

class AnswerState(StatesGroup):
    id = State()
    answer = State()
    check = State()