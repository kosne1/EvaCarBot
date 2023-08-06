from app import bot
from app.hadnlers.commands import start_command
import app.hadnlers


if __name__ == '__main__':
    bot.set_my_commands([
        start_command
    ])

    bot.set_chat_menu_button()

    bot.polling(none_stop=True)
