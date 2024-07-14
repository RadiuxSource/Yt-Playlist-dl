import asyncio
import logging
import time
from importlib import import_module
from pymongo import MongoClient
from os import listdir, path
from dotenv import load_dotenv
from pyrogram import Client
from config import Config


loop = asyncio.get_event_loop()
load_dotenv()
boot = time.time()


logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)


zenova = Client(
    ":zenova:",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workdir="./sessions"
)

client = MongoClient(Config.MONGO_URI)
db = client["giveaway_db"]
giveaways = db["giveaways"]


async def zenova_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await zenova.start()
    getme = await zenova.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name


loop.run_until_complete(zenova_bot())
