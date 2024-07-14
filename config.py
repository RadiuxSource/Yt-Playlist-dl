import os

class Config:
    API_HASH = os.getenv("API_HASH", '15478961975051dfc360958e9ea07830')
    BOT_TOKEN = os.getenv("BOT_TOKEN", '7481260627:AAERIgH99ZziRP-E2GBC_0Sj2BkXgtShCFA')
    BOT_USERNAME = os.getenv("BOT_USERNAME", 'radiuxspam6bot')
    MONGO_URI = os.getenv("MONGO_URI", 'mongodb+srv://adityapatel:aditya310708@cluster0.esldbqp.mongodb.net/?retryWrites=true&w=majority')
    API_ID = int(os.getenv("API_ID", 24006476))
