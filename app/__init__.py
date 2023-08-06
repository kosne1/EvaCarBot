from telebot import TeleBot

from app.configs import env

bot = TeleBot(token=env.BOT_TOKEN, parse_mode='html')
