from app import env


class API:
    def __init__(self):
        self.api_url = f"{env.API_URL}/api"
        self.api_token = env.API_TOKEN
