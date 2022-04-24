from vkbottle import Bot
from configparser import ConfigParser

from commands import start
from sqlite3 import connect

# DataBase Variable
db = connect("tupa_vk_2022.db")
cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS games(user_id, deck, discard)")
db.commit()

# Config Variable
config = ConfigParser()
config.read("config.ini")

# Bot Variable
bot = Bot(config["bot"]["bot_token"])

# Load Commands
start.bp.load(bot)

bot.run_forever()
