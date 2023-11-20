from app import bot
from app.handlers.commands import start_command
import app.handlers


if __name__ == '__main__':
    bot.set_my_commands([
        start_command
    ])

    bot.set_chat_menu_button()

    bot.polling(none_stop=True)
