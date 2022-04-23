from vkbottle import Bot
from configparser import ConfigParser

from commands import start

# Config Variable
config = ConfigParser()
config.read("config.ini")

# Bot Variable
bot = Bot(config["bot"]["bot_token"])

# Load Commands
start.bp.load(bot)

bot.run_forever()
