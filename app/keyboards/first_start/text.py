from app.schemas.ButtonInfoSchema import ButtonInfo

register_button_info = ButtonInfo(text="Регистрация", callback_data="register")
sign_in_button_info = ButtonInfo(text="Войти", callback_data='sign_in')
