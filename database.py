import sqlite3 as sql

# База данных с четырьмя таблицами
# 1. Лайки пользователя
# Связка id пользователя в ВК и список id пользователей, которым он поставил лайк
# 2. Черный список
# Связка id пользователя в ВК и список id пользователей, которых он добавил в черный список
# 3. Список просмотренных
# Связка id пользователя в ВК и список id пользователей, анкеты которых он уже видел.
# 4. Данные о пользователе
# Пол, город и возраст пользователя. Пользователь всего один, поэтому таблица состоит из одной строки.

# Подключаемся к базе данных
conn = sql.connect("database.db")
cursor = conn.cursor()

# Создаем таблицы

cursor.execute(
    """CREATE TABLE IF NOT EXISTS likes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    likes TEXT
)"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS blacklist (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    blacklist TEXT
)"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS viewed (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    viewed_profiles TEXT
)"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS user_data (
    id INTEGER PRIMARY KEY,
    city INTEGER,
    sex INTEGER,
    year INTEGER
)"""
)

# Сохраняем изменения
conn.commit()

# Функция добавления лайков пользователя в базу данных
def add_likes(id: int, likes: list[int]):
    cursor.execute("INSERT INTO likes VALUES (?, ?, ?)", (None, id, str(likes)))
    conn.commit()


# Функция добавления черного списка пользователя в базу данных
def add_blacklist(id: int, blacklist: list[int]):
    cursor.execute("INSERT INTO blacklist VALUES (?, ?, ?)", (None, id, str(blacklist)))
    conn.commit()

# Функция добавления просмотренных анкет в базу данных
def add_viewed_profiles(id: int, viewed_profiles: list[int]):
    cursor.execute("INSERT INTO viewed VALUES (?, ?, ?)", (None, id, str(viewed_profiles)))
    conn.commit()


# Функция получения лайков пользователя
def get_likes(id: int):
    cursor.execute("SELECT likes FROM likes WHERE user_id = ?", (id,))
    likes = cursor.fetchall()
    if likes is None:
        return None
    return likes


# Функция получения черного списка пользователя
def get_blacklist(id: int):
    cursor.execute("SELECT blacklist FROM blacklist WHERE user_id = ?", (id,))
    blacklist = cursor.fetchall()
    if blacklist is None:
        return None
    return blacklist

# Функция получения просмотренных анкет пользователя
def get_viewed_profiles(id: int):
    cursor.execute("SELECT viewed_profiles FROM viewed WHERE user_id = ?", (id,))
    viewed_profiles = cursor.fetchall()
    if viewed_profiles is None:
        return None
    return viewed_profiles

# Функция сохранения данных о пользователе
def add_user_data(city, sex, year):
    cursor.execute("INSERT INTO user_data VALUES (1, ?, ?, ?)", (city, sex, year))
    conn.commit()

# Функция получения данных о пользователе
def get_user_data():
    cursor.execute("SELECT * FROM user_data WHERE id = 1")
    user_data = cursor.fetchone()
    if user_data is None:
        return None
    return user_data

# Функция обновления данных о пользователе
def update_user_data(city, sex, year):
    cursor.execute("UPDATE user_data SET city = ?, sex = ?, year = ? WHERE id = 1", (city, sex, year))
    conn.commit()
