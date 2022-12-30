from aiogram.dispatcher.filters.state import State, StatesGroup


class QuestionState(StatesGroup):
    name = State()
    question = State()
    check = State()
    