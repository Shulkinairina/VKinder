import asyncio
from vkbottle import API, VKAPIError, User

# Ищем пользователей ВКонтакте, приблизительно подходящих под
# заданные критерии, такие как: возраст, пол, город,
# семейное положение, общие группы.


async def get(
    api: API,
    age: int,
    city: int,
    groups: list[int],
    sex: int = 0,
    offset: int = 0
) -> list[tuple[User, list[int], int]]:
    # Ищем пользователей по полу, городу, возрасту и семейному положению
    users = []
    offset = 0
    while True:
        try:
            response = await api.users.search(
                count=50,
                age_from=age - 3,
                age_to=age + 3,
                status=6,  # в активном поиске
                sex=sex,
                has_photo=1,  # с фотографией
                city=city,
                offset=offset,
            )
        except VKAPIError as ex:
            print(ex)
            await asyncio.sleep(2)
            continue
        
        users += response.items
        break
        

    # Получаем список сообществ пользователей
    users_with_groups = []
    for user in users:
        while True:
            try:
                user_groups = await api.users.get_subscriptions(user_id=user.id)
                break
            except VKAPIError as e:
                if e.code == 6:  # ошибка из-за частых запросов
                    await asyncio.sleep(2)  # ждем 2 секунды
                else:
                    break
        users_with_groups.append((user, user_groups.groups.items))

    # Число общих групп добавляем в кортеж
    users_with_groups = [
        (user[0], user[1], len(set(user[1]) & set(groups)))
        for user in users_with_groups
    ]
    # Сортируем по числу общих групп
    users_with_groups.sort(key=lambda x: x[2], reverse=True)

    # Возвращаем список пользователей
    return users_with_groups