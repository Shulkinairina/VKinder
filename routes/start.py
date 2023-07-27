from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()


@bl.message(payload={"command": "start"})
async def start(message: Message):
    await message.answer(
        'Привет! Я бот для знакомств. Введи команду "поиск", чтобы начать поиск анкет.'
    )
    return
