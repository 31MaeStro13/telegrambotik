from typint import Any, Aqaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class SomeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:

        # ...
        # Здесь выполняется код на входе в middleware
        # ...


        result= await handler(event, data)

        # ...
        # Здесь выполняется код на выходе из middleware
        # ...

        return result