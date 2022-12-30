from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.button import main
from keyboards.inline.button import *
from loader import dp, bot
from states.answer import AnswerState
from states.question import QuestionState
from aiogram.dispatcher import FSMContext
from data.config import ADMINS

# /start komandasi uchun handler
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=main)
    
# ✍️ Savol yuborish tugmasi uchun handler
@dp.message_handler(text = "✍️ Savol yuborish")
async def write_question(message: types.Message):
    await message.answer("🖌Ismingizni va fimiliyangizni yuboring:")
    await QuestionState.name.set()

@dp.message_handler(state = QuestionState.name)
async def question(message: types.Message, state: FSMContext):
    await state.update_data({
        "name":message.text
    })
    await message.answer("✏️  Savolingizni yuboring:")
    await QuestionState.next()
    
@dp.message_handler(state = QuestionState.question)
async def something(message: types.Message, state: FSMContext):
    await state.update_data({
        "question":message.text
    })
    data = await state.get_data()
    text = "📤 <b>Malutmolarni adminga yuborayinmi?</b>\n\n"
    text += f"Ismingiz: {data['name']}\n"
    text += f"Savolingiz: {data['question']}"
    
    await message.answer(text=text, reply_markup=yes_no)
    await QuestionState.next()
    
    
@dp.callback_query_handler(state = QuestionState.check)
async def check(call: types.CallbackQuery, state: FSMContext):
    if call.data == "yes":
        data = await state.get_data()
        text = "🎉 Yangi savol keldi:\n\n"
        text += f"ID: {call.from_user.id}\n"
        text += f"Username: @{call.from_user.username}\n"
        text += f"Ismi: {data['name']}\n"
        text += f"Savol: {data['question']}"
        
        await bot.send_message(chat_id = ADMINS[0],text = text, reply_markup=await answer_button(user_id=f"{call.from_user.id}"))
        await call.message.answer("Adminga yuborildi. Iltimosni admin javobini kuting. ✅", reply_markup=main)
        await state.finish()
        await call.message.delete()  
    else:
        await call.message.answer(text = "❌ Bekor qilindi", reply_markup = main)
        await call.message.delete()
        await state.finish()
        
@dp.callback_query_handler(text_contains = "answer:")
async def answer(call: types.CallbackQuery, state: FSMContext):
    await AnswerState.id.set()
    id = call.data.replace("answer:", "")
    await state.update_data({
        "id":id
    })
    await call.message.answer("Javobni kiriting:")
    await call.message.delete()
    await AnswerState.next()
    
@dp.message_handler(state = AnswerState.answer)
async def answer_something(message: types.Message, state: FSMContext):
    await state.update_data({
        "answer":message.text
    })
    data = await state.get_data()
    await bot.send_message(chat_id = f"{data['id']}", text = f"🎉 Admindan javob keldi: \n\n{data['answer']}")
    await message.answer("Javob yuborildi!")
    await message.delete()
    await state.finish()
