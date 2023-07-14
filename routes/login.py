import database
from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()

# Принимаем токен пользователя и сохраняем его в базе данных


@bl.message(text="рег <token>")
async def register(message: Message, token: str):
    database.add_user(message.from_id, token)
    await message.answer("Вы успешно зарегистрировались! Напишите команду \"поиск\" чтобы начать.")
