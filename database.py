import sqlite3 as sql

# База данных с тремя таблицами
# 1. Пользователи
# Связка id пользователя в ВК и его access_token
# 2. Лайки пользователя
# Связка id пользователя в ВК и список id пользователей, которым он поставил лайк
# 3. Черный список
# Связка id пользователя в ВК и список id пользователей, которых он добавил в черный список

# Подключаемся к базе данных
conn = sql.connect("database.db")
cursor = conn.cursor()

# Создаем таблицы
cursor.execute(
    """CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    token TEXT
)"""
)

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

# Сохраняем изменения
conn.commit()


# Функция добавления пользователя в базу данных
def add_user(id: int, token: str):
    cursor.execute("INSERT INTO users VALUES (?, ?)", (id, token))
    conn.commit()


# Функция добавления лайков пользователя в базу данных
def add_likes(id: int, likes: list[int]):
    cursor.execute("INSERT INTO likes VALUES (?, ?, ?)", (None, id, str(likes)))
    conn.commit()


# Функция добавления черного списка пользователя в базу данных
def add_blacklist(id: int, blacklist: list[int]):
    cursor.execute("INSERT INTO blacklist VALUES (?, ?, ?)", (None, id, str(blacklist)))
    conn.commit()


# Функция получения токена пользователя
def get_token(id: int):
    cursor.execute("SELECT token FROM users WHERE id = ?", (id,))
    token = cursor.fetchone()
    if token is None:
        return None
    return token[0]


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