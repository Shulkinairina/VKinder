from vkbottle import API, Bot, BaseStateGroup
from vkbottle.bot import Message

from routes import labelers
import database
import config

bot = Bot(config.VK_TOKEN)
api = API(token=config.VK_USER_TOKEN)

for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

# Состояния пользователя
class UserState(BaseStateGroup):
    SEX = "sex"
    CITY = "city"
    YEAR = "year"

sex, city, year = None, None, None

@bot.on.message(text = 'рег')
async def reg(message: Message):
    await message.answer('Укажите ваш пол, М или Ж.')
    await bot.state_dispenser.set(message.peer_id, UserState.SEX)

# Запросить пол пользователя
@bot.on.message(state=UserState.SEX)
async def reg_sex(message: Message):
    global sex
    if message.text.lower() == "м":
        sex = 2
    elif message.text.lower() == "ж":
        sex = 1
    else:
        await message.answer("⚠️ Некорректный пол! Нужно ввести \"м\" или \"ж\".")
        return
    await bot.state_dispenser.set(message.peer_id, UserState.CITY)

# Запросить город пользователя
@bot.on.message(state=UserState.CITY)
async def reg_city(message: Message):
    city_name = message.text
    cities = await api.database.get_cities(q=city_name)
    if len(cities.items) == 0:
        await message.answer("⚠️ Город не найден! Попробуйте ввести другой.")
        return
    global city
    city = cities.items[0].id
    await message.answer("Укажите ваш год рождения.")
    await bot.state_dispenser.set(message.peer_id, UserState.YEAR)

# Запросить год рождения пользователя
@bot.on.message(state=UserState.YEAR)
async def reg_year(message: Message):
    try:
        year = int(message.text)
    except:
        await message.answer("⚠️ Некорректный год рождения! Попробуйте еще раз.")
        return
    
    try:
        user = database.get_user_data()
    except:
        database.add_user_data(city, sex, year)
        return
    
    database.update_user_data(city, sex, year)
    
    await bot.state_dispenser.delete(message.peer_id)
    await message.answer("✅ Вы успешно зарегистрировались!")



bot.run_forever()
