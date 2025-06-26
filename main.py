import telebot
import requests
import os
from yt_dlp import YoutubeDL

API_TOKEN = '8114186234:AAE2n-Y3H8NdUpnq2KshDaI7NXlpVOvk5NA'
CHANNEL_USERNAME = '@createdgalaxy'  # канал, на который нужно быть подписанным

bot = telebot.TeleBot(API_TOKEN)

# Проверка подписки
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_subscribed(message.from_user.id):
        bot.reply_to(message, "Привет! Отправь ссылку на видео из TikTok или Instagram 📥")
    else:
        bot.send_message(message.chat.id,
            f"Чтобы пользоваться ботом, подпишись на канал {CHANNEL_USERNAME} и нажми /start")

# Обработка ссылок
@bot.message_handler(func=lambda message: message.text.startswith("http"))
def download_video(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id,
            f"Подпишись на канал {CHANNEL_USERNAME}, чтобы пользоваться ботом.")
        return

    url = message.text.strip()
    bot.send_message(message.chat.id, "Скачиваю видео... ⏳")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'mp4',
            'quiet': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(filename)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при скачивании: {str(e)}")

bot.polling()