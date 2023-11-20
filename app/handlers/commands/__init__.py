from telebot.types import Message, BotCommand

from app import bot
from app.api.User import Users
from app.keyboards.first_start import first_start_keyboard
from app.keyboards.start import executor_start_keyboard, customer_start_keyboard
from app.services import order_storage_service

start_command = BotCommand("/start", "Запуск бота")


@bot.message_handler(commands=['start'])
def start(message: Message):
    user = Users().get(telegram_id=message.from_user.id)
    if user is None:
        reply_markup = first_start_keyboard
    else:
        order_storage_service.set_state_authorized(message.chat.id, message.from_user.id)
        reply_markup = executor_start_keyboard if user.role.type == 'executor' else customer_start_keyboard

    bot.send_message(chat_id=message.chat.id, text='Добро пожаловать!',
                     reply_markup=reply_markup)
