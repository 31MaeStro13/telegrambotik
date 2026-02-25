# В НАЧАЛЕ файла aiagent.py добавьте:
import sys
import os

# Добавляем родительскую директорию в путь Python
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from aiagent.aiagent import agent

from aiogram import Router
from aiogram.types import Message


router_dialog = Router()

@router_dialog.message()
async def dialog_process_answer(message: Message):
    user_text = message.text

    response = agent.run(user_text).content.strip()

    await message.answer(text=response)
