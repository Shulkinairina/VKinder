from io import BytesIO

from vkbottle import API, GroupEventType, PhotoMessageUploader
from vkbottle.bot import BotLabeler, MessageEvent, Message
from vkbottle.http import AiohttpClient

import database
import config

bl = BotLabeler()

api = API(config.VK_TOKEN)
uploader = PhotoMessageUploader(api, generate_attachment_strings=True)
http_client = AiohttpClient()


# Сохрняем отметку лайка или дизлайка в базу данных
@bl.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent)
async def like_or_dislike(event: MessageEvent):
    if event.payload is None:
        return
    if event.payload["command"] not in ["like", "dislike"]:
        return
    if event.payload["id"] is None:
        return

    if event.payload["command"] == "like":
        database.add_likes(event.object.peer_id, event.payload["id"])
        await event.show_snackbar("💖 Вы поставили лайк!")

    elif event.payload["command"] == "dislike":
        database.add_blacklist(event.object.peer_id, event.payload["id"])
        await event.show_snackbar("💔 Вы поставили дизлайк!")


# Выводим список лайков пользователя
@bl.message(text="лайки")
async def show_likes(message: Message):
    # получаем список лайков пользователя
    likes = database.get_likes(message.from_id)
    if likes is None:
        likes = []

    new_likes = []
    for like in likes:
        new_likes.append(int(like[0]))

    likes = new_likes

    # если список пуст, выводим сообщение
    if len(likes) == 0:
        await message.answer("👎 У вас нет лайков")
        return

    # инициализируем API
    api = API(token=config.VK_USER_TOKEN)

    # получаем данные пользователей
    users = await api.users.get(user_ids=likes, fields="photo_max_orig")

    # отправляем фотографии пользователей
    for user in users:
        photo_url = user.photo_max_orig
        photo = await http_client.request_content(photo_url)
        photo = BytesIO(photo)
        photo.seek(0)
        photo = await uploader.upload(photo.read())

        await message.answer(
            f"👍 {user.first_name} {user.last_name}\n @id{user.id}", attachment=photo
        )


# Выводим список дизлайков пользователя
@bl.message(text="чс")
async def show_blacklist(message: Message):
    # получаем черный список пользователя
    blacklist = database.get_blacklist(message.from_id)
    if blacklist is None:
        blacklist = []

    new_blacklist = []
    for user in blacklist:
        new_blacklist.append(int(user[0]))

    blacklist = new_blacklist

    # если список пуст, выводим сообщение
    if len(blacklist) == 0:
        await message.answer("👍 Ваш черный список пуст")
        return

    # инициализируем API
    api = API(token=config.VK_USER_TOKEN)

    # получаем данные пользователей
    users = await api.users.get(user_ids=blacklist, fields="photo_max_orig")

    # отправляем фотографии пользователей
    for user in users:
        photo_url = user.photo_max_orig
        photo = await http_client.request_content(photo_url)
        photo = BytesIO(photo)
        photo.seek(0)
        photo = await uploader.upload(photo.read())

        await message.answer(
            f"👎 {user.first_name} {user.last_name}\n @id{user.id}", attachment=photo
        )
    print(blacklist)


@bl.message(text="дб")
async def debug(message: Message):
    viewed = database.get_viewed_profiles(message.from_id)
    print(viewed)