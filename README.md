# VKinder
Бот для поиска пары ВКонтакте

## Установка
Клонируйте этот репозиторий. Создайте виртуальное окружение и активируйте его:
```sh
python -m venv venv
. ./venv/bin/activate       # Unix
.\venv\Scripts\activate     # Windows CMD
.\venv\Scripts\activate.ps1 # Windows PS
```
Установите необходимые зависимости:
```sh
pip install -r requirements.txt
```
## Запуск бота
```sh
python bot.py
```

## Доступные команды
- поиск - начать поиск анкет. Бот перебирает тысячи результатов, поэтому выполнение данной команды может занять время.
- лайки - список анкет, которые вы лайкнули.
- чс - список анкет, которые вы дизлайкнули.