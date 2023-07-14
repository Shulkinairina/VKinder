from vkbottle import Bot
from routes import labelers

import config

bot = Bot(config.VK_TOKEN)

for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

bot.run_forever()
