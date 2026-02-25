from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)
from aiogram import F
from config.config import Config, load_config

config: Config = load_config()

bot = Bot(config.bot.token)
dp = Dispatcher()

LEXICON: dict[str, str] = {
    'but_1': 'Кнопка 1',
    'but_2': 'Кнопка 2',
    'but_3': 'Кнопка 3',
    'but_4': 'Кнопка 4',
    'but_5': 'Кнопка 5',
    'but_6': 'Кнопка 6',
    'but_7': 'Кнопка 7'
}

kb_builder = InlineKeyboardBuilder()
# Наполняем клавиатуру кнопками-закладками в порядке возрастания
for button in sorted(args):
    kb_builder.row(InlineKeyboardButton(
        text=f'{LEXICON["del"]} {button} - {book[button][:100]}',
        callback_data=f'{button}del'
    ))
# Добавляем в конец клавиатуры кнопку "Отменить"
kb_builder.row(InlineKeyboardButton(
    text=LEXICON['cancel'],
    callback_data='cancel'
))

keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру с инлайн-кнопками
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text="Это инлайн-кнопки. Нажми на любую!", reply_markup=keyboard
    )
# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data `button_1_click`
@dp.callback_query(F.data == "button_1_click")
async def process_button_1_click(callback: CallbackQuery):
    if callback.message.text != "Была нажата КНОПКА 1":
        await callback.message.edit_text(
            text="Была нажата КНОПКА 1",
            reply_markup=callback.message.reply_markup,
        )
    await callback.answer()

# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data `button_2_click`
@dp.callback_query(F.data == "button_2_click")
async def process_button_2_click(callback: CallbackQuery):
    await callback.answer(text="Ура! Нажата кнопка 2", show_alert=True)

if __name__ == "__main__":
    dp.run_polling(bot)