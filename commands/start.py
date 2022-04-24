from vkbottle import PhotoMessageUploader
from vkbottle.bot import Blueprint, Message

from random import choice, randint
from sqlite3 import connect

bp = Blueprint("Start command")

# Variables
path = "deck/images/"
db = connect("tupa_vk_2022.db")
cursor = db.cursor()


# Functions
async def generate_photos_name(deck: list = None):
    photos_name = set()
    while len(photos_name) < 5:
        if deck:
            photos_name.add(choice(deck))
        else:
            photos_name.add(randint(1, 98))
    return photos_name


async def upload_photos(photos_name: set):
    photo_upload = PhotoMessageUploader(bp.api)
    photos_id = []
    for i in photos_name:
        photos_id.append(await photo_upload.upload(f"{path}{i}.jpg"))
    return photos_id


# Commands
@bp.on.message(text=["Старт", "старт"])
async def start_command(message: Message):
    check_game = cursor.execute("SELECT user_id FROM games WHERE user_id == ?", (message.from_id,)).fetchone()
    if check_game:
        deck = cursor.execute("SELECT deck FROM games WHERE user_id == ?",
                              (message.from_id,)).fetchone()[0]
        if len(eval(deck)) <= 3:
            photos_name = set()
            while len(photos_name) < 3:
                photos_name.add(choice(list(eval(deck))))
            photo_list = await upload_photos(photos_name)
            cursor.execute("DELETE FROM games WHERE user_id == ?",
                           (message.from_id,))
            db.commit()
            await message.answer(
                attachment=f"{photo_list[0]},{photo_list[1]},{photo_list[2]}")
        else:
            random_photos_names = await generate_photos_name(list(eval(deck)))
            photo_list = await upload_photos(random_photos_names)
            cursor.execute("UPDATE games SET deck == ? WHERE user_id == ?",
                           (str(eval(f"{deck} - {random_photos_names}")), message.from_id))
            cursor.execute("UPDATE games SET discard == ? WHERE user_id == ?",
                           (str(random_photos_names), message.from_id))
            db.commit()
            await message.answer(
                attachment=f"{photo_list[0]},{photo_list[1]},{photo_list[2]},{photo_list[3]},{photo_list[4]}")
    else:
        random_photos_names = await generate_photos_name()
        photo_list = await upload_photos(random_photos_names)
        cursor.execute("INSERT INTO games VALUES(?, ?, ?)",
                       (message.from_id, str(set(range(1, 99)) - random_photos_names), str(random_photos_names)))
        db.commit()
        await message.answer(
            attachment=f"{photo_list[0]},{photo_list[1]},{photo_list[2]},{photo_list[3]},{photo_list[4]}")
