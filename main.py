import os
import time
from dotenv import load_dotenv
from bot import Bot

# Loading the config variables from the .env file
load_dotenv()

# Constructing the Bot class 
bot = Bot(
    Token=os.getenv("OAUTH2_TOKEN"),
    Initial_Channels=["#wordbenderbot", "#gamecode64"]
)

while True:
    try:
        bot.run()
    except ConnectionResetError as e:
         with open(f"error.log", "a+") as OutFile:
            OutFile.write(f"""\n[{time.strftime("%Y-%m-%d %H:%M:%S")}] - {str(e)}""")
            exit()
    except Exception as e:
        with open(f"error.log", "a+") as OutFile:
            OutFile.write(f"""\n[{time.strftime("%Y-%m-%d %H:%M:%S")}] - {str(e)}""")
            exit()
    else:
        break

