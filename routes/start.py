from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()


@bl.message(payload={"command": "start"})
async def start(message: Message):
    await message.answer(
        'Привет! Я бот для знакомств. Для начала тебе нужно зарегистрироваться.\n\n\
                         Для этого введи команду "рег <token>", где token - твой access_token. Ты можешь получить его на сайте: https://vkhost.github.io/'
    )
    return
