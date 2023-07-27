import database
from datetime import datetime
from io import BytesIO
import asyncio

from vkbottle import API, Keyboard, Callback, PhotoMessageUploader
from vkbottle.bot import BotLabeler, Message
from vkbottle.http import AiohttpClient

from modules import search, photos
import config

bl = BotLabeler()

api = API(config.VK_TOKEN)
uploader = PhotoMessageUploader(api, generate_attachment_strings=True)

http_client = AiohttpClient()

offset = 0

# Получаем данные со страницы пользователя и ищем подходящие анкеты
@bl.message(text="поиск")
async def search_user(message: Message):
    global offset

    token = config.VK_USER_TOKEN

    await message.answer(
        "🔍 Ищем подходящие анкеты. Этот процесс может занять некоторое время."
    )

    # Инициализируем API
    api = API(token=token)

    # данные которые нам нужны: age city groups sex
    # получаем данные со страницы пользователя или из базы данных
    user = await api.users.get(fields="sex,city,bdate")

    if user[0].sex.value == 0 or user[0].city is None:
        try:
            sex, city, bdate = database.get_user_data()
        except:
            await message.answer("⚠️ В вашем профиле недостаточно информации. Введите команду 'рег' для заполнения профиля.")
            return
    else:
        bdate = int(user[0].bdate.split(".")[2])
        sex = 2 if user[0].sex.value == 1 else 1 if user[0].sex.value == 2 else None
        city = user[0].city.id
    age = datetime.now().year - bdate

    # получаем список групп пользователя
    groups = await api.users.get_subscriptions(user_id=message.from_id)
    groups = groups.groups.items

    # ищем подходящие анкеты
    # если в актуальном батче из 50 анкет не нашлось подходящих
    # то увеличиваем offset на 50 и ищем дальше.
    # если подходящих анкет не нашлось в 4 батчах, то завершаем поиск.
    i = 0
    while True:
        users = await search.get(api, age, city, groups, sex, offset)
        if len(users) == 0:
            await message.answer("⚠️ Вы просмотрели все подходящие профили.")
            return

        # удаляем из списка анкеты из черного списка, списка лайкнутых и просмтренных
        blacklist = database.get_blacklist(message.from_id)
        likes = database.get_likes(message.from_id)
        viewed = database.get_viewed_profiles(message.from_id)

        for filter in [blacklist, likes, viewed]:
            if filter is None:
                filter = []
            new_filter = []
            for _id in filter:
                print(_id)
                new_filter.append(int(_id[0]))
            users = [user for user in users if user[0].id not in new_filter]

        if len(users) == 0:
            i+=1
            if i == 4: 
                await message.answer("⚠️ Вы просмотрели все подходящие профили.")
                return
            offset=+50
        else:
            break

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
        await asyncio.sleep(1)
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

        database.add_viewed_profiles(message.from_id, user[0].id)
