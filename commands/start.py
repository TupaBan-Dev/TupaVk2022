from vkbottle import PhotoMessageUploader
from vkbottle.bot import Blueprint, Message

from random import randint

bp = Blueprint("Start command")

# Variables
path = "images/card_deck/"


async def upload_photos():
    photo_upload = PhotoMessageUploader(bp.api)
    photos_name = set()
    while len(photos_name) < 5:
        photos_name.add(randint(1, 98))
    photos_id = []
    for i in photos_name:
        photos_id.append(await photo_upload.upload(f"{path}{i}.jpg"))
    return photos_id


@bp.on.message(text=["Старт", "старт"])
async def start(message: Message):
    photos_id = await upload_photos()
    await message.answer(attachment=f"{photos_id[0]},{photos_id[1]},{photos_id[2]},{photos_id[3]},{photos_id[4]}")
