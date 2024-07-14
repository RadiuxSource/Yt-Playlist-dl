# dl_playlist.py
import logging
import time
from pytube import Playlist, YouTube
from pyrogram import filters
from zenova import zenova
from .thumbnail import set_thumbnail
from .watermark import set_watermark
import moviepy.editor as mp

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='zenova.log',
                    filemode='w')

logger = logging.getLogger(__name__)

async def dl_playlist(zenova, message):
    try:
        playlist_url = message.text
        logger.info(f"Fetching playlist details for {playlist_url}")
        p = Playlist(playlist_url)
        logger.info(f"Playlist title: {p.title}")
        logger.info(f"Playlist description: {p.description}")
        logger.info(f"Playlist length: {len(p.videos)} videos")

        # Ask if the user wants to set a custom channel to dump the videos
        custom_channel = await zenova.ask(message.chat.id, "Do you want to set a custom channel to dump the videos? (yes/no)")
        channel_id = message.chat.id
        if custom_channel.lower() == "yes":
            channel_id = await zenova.ask(message.chat.id, "Enter the channel ID or username:")

        # Ask if the user wants to set a custom thumbnail for the videos
        thumbnail_url = await set_thumbnail(zenova, message)
        if thumbnail_url is None:
            thumbnail_url = None  # Use default thumbnail

        # Ask if the user wants to set a watermark for the videos
        watermark_text = await set_watermark(zenova, message)
        if watermark_text is None:
            watermark_text = ""  # No watermark

        # Ask for the desired video quality
        video_quality = await zenova.ask(message.chat.id, "Enter the desired video quality (144p, 240p, 360p, 480p, 720p, 1080p): ")
        video_quality = video_quality.lower()

        for video in p.videos:
            logger.info(f"Downloading video: {video.title}")
            await zenova.send_message(message.chat.id, f"Downloading video: {video.title}")
            yt = YouTube(video.watch_url)

            # Filter streams by video quality
            if video_quality == "144p":
                mp4_streams = yt.streams.filter(file_extension='mp4', resolution='144p').all()
            elif video_quality == "240p":
                mp4_streams = yt.streams.filter(file_extension='mp4', resolution='240p').all()
            elif video_quality == "360p":
                mp4_streams = yt.streams.filter(file_extension='mp4', resolution='360p').all()
            elif video_quality == "480p":
                mp4_streams = yt.streams.filter(file_extension='mp4', resolution='480p').all()
            elif video_quality == "720p":
                mp4_streams = yt.streams.filter(file_extension='mp4', resolution='720p').all()
            elif video_quality == "1080p":
                mp4_streams = yt.streams.filter(file_extension='mp4', resolution='1080p').all()
            else:
                mp4_streams = yt.streams.filter(file_extension='mp4').all()  # Default to highest quality

            d_video = mp4_streams[-1]

            # Download the video with real-time status updates
            bytes_downloaded = 0
            total_bytes = d_video.filesize
            start_time = time.time()
            video_file = f"{video.title}.mp4"
            with open(video_file, "wb") as f:
                for chunk in d_video.stream():
                    f.write(chunk)
                    bytes_downloaded += len(chunk)
                    percentage = (bytes_downloaded / total_bytes) * 100
                    speed = (bytes_downloaded / (time.time() - start_time)) / 1024
                    consumed_time = time.time() - start_time
                    await zenova.send_message(message.chat.id, f"Downloading video: {video.title} ({percentage:.2f}%) - {speed:.2f} KB/s - {consumed_time:.2f} seconds")

            logger.info(f"Video downloaded successfully: {video.title}")
            await zenova.send_message(message.chat.id, f"Video downloaded successfully: {video.title}")

            # Add watermark to the video
            video = mp.VideoFileClip(video_file)
            txt_clip = mp.TextClip(watermark_text, fontsize=70, color='white')
            txt_clip = txt_clip.set_position('bottom_right').set_duration(120)  # 2 minutes
            video = mp.CompositeVideoClip([video, txt_clip])
            video.write_videofile(video_file)

            # Upload the video to the chat with a custom caption and thumbnail
            caption = f"Video: {video.title}\nUploaded by ZENOVA"
            await zenova.send_video(channel_id, video_file, caption=caption, thumb=thumbnail_url)

        logger.info(f"Playlist downloaded successfully!")
        await zenova.send_message(message.chat.id, f"Playlist downloaded successfully!")

    except Exception as e:
        logger.error(f"Error: {e}")
        await zenova.send_message(message.chat.id, f"Error: {e}")
