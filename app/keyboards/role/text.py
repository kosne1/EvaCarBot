from app.schemas.ButtonInfoSchema import ButtonInfo

choose_customer_role_button_info = ButtonInfo(text="Заказчик", callback_data="choose_customer_role")
choose_executor_role_button_info = ButtonInfo(text="Исполнитель", callback_data="choose_executor_role")
