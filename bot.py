import os
import twitchio
import random
import re

from dotenv import load_dotenv

# Loading the config variables from the .env file
load_dotenv()

class Bot(twitchio.Client):
    def __init__(self, Token, Initial_Channels):
        super().__init__(
            token=Token,
            initial_channels=Initial_Channels,
        )

    # Defining some variables
    Messages=[]
    TmpReplaceWord=os.getenv("STARTWORD")

    async def event_ready(self):
        print(f"{self.nick} Hopped in to chat")

    async def event_message(self, Message):
        # Ignore messages sent by the bot itself
        if Message.echo:
            return

        # Giving a reaction to hello booty
        if Message.content.lower().startswith("hello booty"):
            await Message.channel.send(f"Hello big butted {Message.author.name}!")

        # Giving a reaction to bootybot yes
        elif Message.content.lower().find("bootybot yes") != -1: # Using -1 as validation. find() gives -1 if the value isn't found
            await Message.channel.send(":D")

        # Giving a reaction to bootybot no
        elif Message.content.lower().find("bootybot no") != -1: # Using -1 as validation. find() gives -1 if the value isn't found
            await Message.channel.send("D:")

        # Giving a reaction someone that is talking about bootybot
        elif Message.content.lower().find("bootybot") != -1: # Using -1 as validation. find() gives -1 if the value isn't found
            await Message.channel.send(f"What do you want {Message.author.name}?")

        # Moderating the word to replace in the message
        elif Message.content.startswith("!setword"):
            # Only a mod is allowed to do this
            if Message.author.is_mod:
                SetWord = re.search("^\!setword ([\w\!\+\-\_\d]*)", Message.content)
                if SetWord:
                    self.TmpReplaceWord=SetWord.group(1)
                    await Message.channel.send(f"Word has been changed into: {self.TmpReplaceWord}")

        # Ignoring all commands, preventing them to be added into the message list
        elif Message.content.startswith("!"):
            return
        # If everything has been done, lets add the message into the list
        else:
            self.Messages.append(Message.content)

        # After the list has been filled with atleast
        if len(self.Messages) > 5 :
            if random.randint(0, 5) == 1:
                SelectedMsg = random.choice(self.Messages)
                Words = SelectedMsg.split()
                RdmWord = random.randint(0,len(Words) -1)
                Words[RdmWord] = self.TmpReplaceWord
                NewMsg = " ".join(Words)
                await Message.channel.send(NewMsg)
                self.Messages.clear()