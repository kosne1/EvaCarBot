from pydantic_settings import BaseSettings


class EnvConfig(BaseSettings):
    BOT_TOKEN: str
    API_URL: str
    API_TOKEN: str
    MANAGER_TELEGRAM_ID: str
    RUB_PER_KM: int
    ORDER_START_PRICE: int
