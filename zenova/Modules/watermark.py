import logging
from pyrogram import filters
from zenova import zenova

logger = logging.getLogger(__name__)

async def set_watermark(zenova, message):
    try:
        logger.info(f"Asked to set watermark for playlist")
        watermark_text = await zenova.ask(message.chat.id, "Enter the watermark text: ")
        logger.info(f"Watermark text set to {watermark_text}")
        return watermark_text
    except Exception as e:
        logger.error(f"Error: {e}")
        await zenova.send_message(message.chat.id, f"Error: {e}")
        return None
