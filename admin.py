import os
import asyncio
from main import EditBot
from main import BotState
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
import constants
from buttons import main_admin_kb
from buttons import main_cancel_kb
import database

DB_PATH = "ocean.db"
IMG_DIR = "images"
os.makedirs(IMG_DIR, exist_ok=True)

async def send_info(message: Message):
    await message.answer(f"Поддержка: @{constants.bot_admin}\nРеквизиты: {constants.bot_props}")
    path = os.path.join(IMG_DIR, "qr.jpg")
    if os.path.exists(path):
        photo = FSInputFile(path)
        await message.answer_photo(photo, caption="QR", reply_markup=main_admin_kb())
    else:
        await message.answer("QR пока не загружен.")


async def handle_admin(message: Message, state: FSMContext):
    new_admin = message.text
    
    database.update_admin(new_admin)
    constants.bot_admin = new_admin
    
    if constants.bot_admin == new_admin:
        await message.answer(f"Служба поддержки обновлена и сохранена. Новый admin: {constants.bot_admin}", reply_markup=main_admin_kb())
    else:
        await message.answer("Произошла ошибка при обновлении данных. Попробуйте снова.", reply_markup=main_admin_kb())
    await state.set_state(BotState.admin)

async def handle_props(message: Message, state: FSMContext):
     new_props = message.text
     database.update_props(new_props)
     constants.bot_props = new_props
     
     if constants.bot_props == new_props:
        await message.answer(f"Реквизит обновлен и сохранен. Новый реквизит: {constants.bot_props}", reply_markup=main_admin_kb())
     else:
        await message.answer("Произошла ошибка при обновлении данных. Попробуйте снова.", reply_markup=main_admin_kb())
     await state.set_state(BotState.admin)
         
async def handle_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
   
    new_path = os.path.join(IMG_DIR, f"qr.jpg")
    await message.bot.download_file(file.file_path, destination=new_path)

    await message.answer("Изображение обновлено и сохранено.", reply_markup=main_admin_kb())
    await state.set_state(BotState.admin)


async def admin_handler(message: Message, state: FSMContext) -> None:
         await send_info(message)
         await state.set_state(BotState.admin)
         
async def admin_ops(message: Message, state: FSMContext) -> None:
    try:            
        if(message.text == "Редактировать службу поддержки"):
         await state.set_state(EditBot.waiting_for_admin)   
         await message.answer("Введите значение:", reply_markup=main_cancel_kb())
         
        elif(message.text == "Редактировать реквизиты"):
         await state.set_state(EditBot.waiting_for_props)
         await message.answer("Введите значение:", reply_markup=main_cancel_kb())
         
        elif(message.text == "Загрузить другой QR"):
         await state.set_state(EditBot.waiting_for_photo)
         await message.answer("Отправьте фото:", reply_markup=main_cancel_kb())
         
    except TypeError:
        await message.answer("Ошибка :(")
        
        
