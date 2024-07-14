import logging
from pyrogram import filters
from zenova import zenova

logger = logging.getLogger(__name__)

async def set_thumbnail(zenova, message):
    try:
        logger.info(f"Asked to set custom thumbnail for playlist")
        thumbnail_url = await zenova.ask(message.chat.id, "Enter the custom thumbnail URL or send a photo: ")
        if thumbnail_url.lower() == "/skip":
            logger.info(f"Using default thumbnail")
            return None
        else:
            logger.info(f"Custom thumbnail set to {thumbnail_url}")
            return thumbnail_url
    except Exception as e:
        logger.error(f"Error: {e}")
        await zenova.send_message(message.chat.id, f"Error: {e}")
        return None
