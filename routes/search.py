import database
from datetime import datetime
from io import BytesIO

from vkbottle import API, Keyboard, Callback, PhotoMessageUploader
from vkbottle.bot import BotLabeler, Message
from vkbottle.http import AiohttpClient

from modules import search, photos
import config

bl = BotLabeler()

api = API(config.VK_TOKEN)
uploader = PhotoMessageUploader(api, generate_attachment_strings=True)

http_client = AiohttpClient()


# Получаем данные со страницы пользователя и ищем подходящие анкеты
@bl.message(text="поиск")
async def search_user(message: Message):
    token = database.get_token(message.from_id)
    if token is None:
        await message.answer(
            "❌ Сначала введите команду !рег token, где <token> - ваш access_token. Вы можете получить его на сайте: https://vkhost.github.io/"
        )
        return
    await message.answer(
        "🔍 Ищем подходящие анкеты. Этот процесс может занять некоторое время."
    )

    # Инициализируем API
    api = API(token=token)

    # данные которые нам нужны: age city groups sex
    # получаем данные со страницы пользователя
    user = await api.users.get(fields="sex,city,bdate")

    sex = 2 if user[0].sex.value == 1 else 1 if user[0].sex.value == 2 else None
    city = user[0].city.id
    age = datetime.now().year - int(user[0].bdate.split(".")[2])

    # получаем список групп пользователя
    groups = await api.users.get_subscriptions(user_id=message.from_id)
    groups = groups.groups.items

    # ищем подходящие анкеты
    users = await search.get(api, age, city, groups, sex)

    # удаляем из списка анкеты из черного списка
    blacklist = database.get_blacklist(message.from_id)
    if blacklist is None:
        blacklist = []

    new_blacklist = []
    for user in blacklist:
        new_blacklist.append(int(user[0]))

    blacklist = new_blacklist

    users = [user for user in users if user[0].id not in blacklist]

    # удаляем из списка анкеты, которым пользователь уже поставил лайк
    likes = database.get_likes(message.from_id)

    if likes is None:
        likes = []

    new_likes = []
    for like in likes:
        new_likes.append(int(like[0]))

    likes = new_likes

    users = [user for user in users if user[0].id not in likes]

    # если подходящих анкет не нашлось
    if len(users) == 0:
        await message.answer("Подходящих анкет не нашлось. Попробуйте позже.")
        return

    # отправляем пользователю 10 самых подходящих анкет
    for user in users[:10]:
        keyboard = Keyboard(inline=True)
        keyboard.add(Callback("💖", payload={"command": "like", "id": user[0].id}))
        keyboard.add(Callback("💔", payload={"command": "dislike", "id": user[0].id}))

        # получаем топ-3 фотографии пользователя
        photos_user = await photos.get(api, user[0].id)
        if photos_user is None:
            continue
        attachments = []
        for photo in photos_user:
            photo = await http_client.request_content(photo)
            photo = BytesIO(photo)
            photo.seek(0)
            photo = await uploader.upload(photo.read())
            attachments.append(photo)

        attachments = ",".join(attachments)

        await message.answer(
            f"{user[0].first_name} {user[0].last_name}\n@id{user[0].id}\n\nОбщих групп: {user[2]}",
            attachment=attachments,
            keyboard=keyboard.get_json(),
        )
