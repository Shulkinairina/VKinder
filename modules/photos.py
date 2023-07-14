from vkbottle import API, VKAPIError

# получить топ-3 самых популярных фотографий в профиле


async def get(
    api: API,
    user_id: int,
):
    # получаем фотографии пользователя
    try:
        photos = await api.photos.get_all(owner_id=user_id, extended=1)
    except VKAPIError:
        return None

    # сортируем фотографии по популярности
    photos_activity = []
    for photo in photos.items:
        likes = photo.likes.count
        try:
            comments = await api.photos.get_comments(
                owner_id=user_id, photo_id=photo.id
            )
            comments = comments.count
        except VKAPIError:
            comments = 0
        photos_activity.append((photo, likes + comments))

    photos_activity.sort(key=lambda x: x[1], reverse=True)

    # получаем ссылки на топ-3 фотографии
    photos_activity = [photo[0].sizes[-1].url for photo in photos_activity]

    # возвращаем топ-3 фотографии
    return photos_activity[:3]
