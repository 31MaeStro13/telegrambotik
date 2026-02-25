from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, BaseFilter
from aiogram.types import Message
import asyncio
from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher()

admin_ids: list[int] = [1531218972]

class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids

class NumbersInMessage(BaseFilter):
    async def  __call__ (self, message: Message) -> bool | dict[str, list[int]]:
        numbers = []

        for word in message.text.split():
            normalized_word = word.replace('.', '').replace(',', '').strip()
            if normalized_word.isdigit():
                numbers.append(int(normalized_word))

        if numbers:
            return {'numbers': numbers}
        return False

@dp.message(F.text.lower().startswith('найди числа'),
            NumbersInMessage())
async def process_if_numbers(message: Message, numbers: list[int]):
    await message.answer(text=f'Нашел: {", ".join(str(num) for num in numbers)}')


@dp.message(F.text.lower().startswith('найди числа'))
async def process_if_not_numbers(message: Message):
    await message.answer(
            text='Не нашел что-то :(')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())