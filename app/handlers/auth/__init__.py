import datetime

from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove, PollAnswer

from app import bot
from app.api.User import Users
from app.helpers import send_wait_message, get_car_list
from app.keyboards.first_start import first_start_keyboard
from app.keyboards.first_start.text import register_button_info, sign_in_button_info
from app.keyboards.phone_number import share_contact_keyboard
from app.keyboards.role import role_keyboard
from app.keyboards.role.text import choose_customer_role_button_info, choose_executor_role_button_info
from app.keyboards.start import customer_start_keyboard, executor_start_keyboard
from app.services import auth_storage_service


@bot.callback_query_handler(func=lambda call: register_button_info.filter(call.data))
def register(call: CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id)
    auth_storage_service.set_state_registring(chat_id=call.message.chat.id, user_id=call.from_user.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Пожалуйста выберите роль:', reply_markup=role_keyboard)

    @bot.callback_query_handler(func=lambda call: choose_customer_role_button_info.filter(call.data) or
                                                  choose_executor_role_button_info.filter(call.data) and
                                                  auth_storage_service.is_registring(call.message.chat.id,
                                                                                     call.from_user.id))
    def register_role(call: CallbackQuery):
        role = 'customer' if choose_customer_role_button_info.filter(call.data) else 'executor'
        auth_storage_service.set_role(chat_id=call.message.chat.id, user_id=call.from_user.id, role=role)
        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Введите ваше ФИО')

        def register_fullname(message: Message):
            auth_storage_service.set_fullname(chat_id=message.chat.id, user_id=message.from_user.id,
                                              full_name=message.text)
            bot.send_message(chat_id=message.chat.id, text='Необходимо поделиться номером телефона',
                             reply_markup=share_contact_keyboard)

            def register_contact(message: Message):
                log_file = open("info.log", "a")
                log_file.write(
                    f"\n[INFO {datetime.datetime.now()}]: {message.from_user.username} {message.contact.phone_number}, {type(message.contact.phone_number)}\n")
                log_file.close()
                auth_storage_service.set_phone_number(chat_id=message.chat.id, user_id=message.from_user.id,
                                                      phone_number=message.contact.phone_number)
                auth_storage_service.set_username(chat_id=message.chat.id, user_id=message.from_user.id,
                                                  username=message.from_user.username)

                user_dto = auth_storage_service.get_create_user_dto(chat_id=message.chat.id,
                                                                    telegram_id=message.from_user.id)
                if user_dto.role == 'executor':
                    bot.send_poll(question='Каким авто вы владеете?', chat_id=message.chat.id,
                                  is_anonymous=False,
                                  allows_multiple_answers=True,
                                  options=['Платформа', "Сдвижная платформа", "Манипулятор", "Автовоз"],
                                  reply_markup=ReplyKeyboardRemove())
                    return
                user = Users().create(user_dto)
                auth_storage_service.set_user_auth_id(chat_id=message.chat.id, user_id=message.from_user.id,
                                                      id=user.id)

                auth_storage_service.set_state_registered(chat_id=message.chat.id, user_id=message.from_user.id)

                bot.send_message(chat_id=message.chat.id, text='Регистрация успешно завершена!',
                                 reply_markup=ReplyKeyboardRemove())
                bot.send_message(chat_id=message.chat.id, text='Добро пожаловать!',
                                 reply_markup=customer_start_keyboard)

            bot.register_next_step_handler(message, register_contact)

        bot.register_next_step_handler(call.message, register_fullname)


@bot.poll_answer_handler(func=lambda call: True)
def handle_poll_answer(pollAnswer: PollAnswer):
    user_dto = auth_storage_service.get_create_user_dto(chat_id=pollAnswer.user.id,
                                                        telegram_id=pollAnswer.user.id,
                                                        car_list=get_car_list(pollAnswer.option_ids))
    user = Users().create(user_dto)
    auth_storage_service.set_user_auth_id(chat_id=pollAnswer.user.id, user_id=pollAnswer.user.id,
                                          id=user.id)
    auth_storage_service.set_state_registered(chat_id=pollAnswer.user.id, user_id=pollAnswer.user.id)

    bot.send_message(chat_id=pollAnswer.user.id, text='Регистрация успешно завершена!',
                     reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id=pollAnswer.user.id, text='Добро пожаловать!',
                     reply_markup=executor_start_keyboard)


@bot.callback_query_handler(func=lambda call: sign_in_button_info.filter(call.data))
def sign_in(call: CallbackQuery):
    send_wait_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user = Users().get(telegram_id=call.from_user.id)
    bot.answer_callback_query(callback_query_id=call.id)
    if user is None:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Необходимо пройти регистрацию',
                              reply_markup=first_start_keyboard)
    else:
        auth_storage_service.set_user_auth_id(chat_id=call.message.chat.id, user_id=call.from_user.id,
                                              id=user.id)
        reply_markup = customer_start_keyboard if user.role.type == 'customer' else executor_start_keyboard
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Авторизация успешно завершена!', reply_markup=reply_markup)
