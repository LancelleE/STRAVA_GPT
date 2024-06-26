from dotenv import dotenv_values

config = dotenv_values(".env")

CLIENT_ID = config["CLIENT_ID"]
CLIENT_SECRET = config["CLIENT_SECRET"]
CLIENT_REFRESH_TOKEN = config["CLIENT_REFRESH_TOKEN"]
CLIENT_ACCESS_TOKEN = config["CLIENT_ACCESS_TOKEN"]
LATEST_RUN=config["LATEST_RUN"]