import os

from dotenv import load_dotenv
from bot import Bot

# Loading the config variables from the .env file
load_dotenv()

# Constructing the Bot class 
bot = Bot(
    Token=os.getenv("OAUTH2_TOKEN"),
    Initial_Channels=["#GameCode64", "#b1g_b00ty_"]
)

while True:
    try:
        bot.run()
    except:
        pass
    else:
        break
