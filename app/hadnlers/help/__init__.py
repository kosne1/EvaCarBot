from telebot.types import CallbackQuery, Message

from app import bot, env
from app.api.User import Users
from app.helpers import send_wait_message
from app.keyboards.start import executor_start_keyboard, customer_start_keyboard
from app.keyboards.start.text import send_help_message_button_info


@bot.callback_query_handler(func=lambda call: send_help_message_button_info.filter(call.data))
def write_help_message_handler(call: CallbackQuery):
    bot.send_message(chat_id=call.message.chat.id, text='Опишите проблему в текстовом формате')
    bot.register_next_step_handler(call.message, send_help_message_handler)


def send_help_message_handler(message: Message):
    new_message = send_wait_message(chat_id=message.chat.id)
    user = Users().get(telegram_id=message.from_user.id)
    # preparing message text for manager
    text = 'Новое сообщение от пользователя:\n\n' + message.text
    text += '\n\n' + 'Информация о пользователе:\n\n' + \
            f'<b>Имя пользователя</b>: @{user.username}\n' \
            f'<b>ФИО</b>: {user.full_name}\n' \
            f'<b>Роль</b>: {"исполнитель" if user.role.type == "executor" else "заказчик"}\n' \
            f'<b>Контакты</b>:'
    bot.send_message(chat_id=env.MANAGER_TELEGRAM_ID, text=text)
    bot.send_contact(chat_id=env.MANAGER_TELEGRAM_ID, phone_number=user.phone_number,
                     first_name=user.full_name)
    # preparing message text for executor
    reply_markup = executor_start_keyboard if user.role.type == 'executor' else customer_start_keyboard
    bot.edit_message_text(chat_id=new_message.chat.id, message_id=new_message.message_id,
                          text='Письмо успешно отправлено, ожидайте обратной связи!',
                          reply_markup=reply_markup)
