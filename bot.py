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
    Channels={}
    TmpReplaceWord=os.getenv("STARTWORD")

    def AddMessageToStack(self, Message):
            if Message.channel.name not in self.Channels:
                self.Channels[Message.channel.name]={
                    "Word": os.getenv("STARTWORD"),
                    "Messages": []
                }
            self.Channels[Message.channel.name]["Messages"].append(Message.content)

    def ChangeChannelWord(self, Message):
                if Message.channel.name not in self.Channels:
                    self.Channels[Message.channel.name]={
                        "Word": os.getenv("STARTWORD"),
                        "Messages": []
                    }
                SetWord = re.search("^\!setword ([\w\!\+\-\_\d]*)", Message.content)
                if SetWord:
                    self.Channels[Message.channel.name]["Word"]=SetWord.group(1)
                    return self.Channels[Message.channel.name]["Word"]
                    

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
                await Message.channel.send("Word has been changed into: "+self.ChangeChannelWord(Message))

        # Ignoring all commands, preventing them to be added into the message list
        elif Message.content.startswith("!"):
            return
        # If everything has been done, lets add the message into the list
        else:
            self.AddMessageToStack(Message)

        # After the list has been filled with atleast
        if len(self.Channels[Message.channel.name]["Messages"]) > 5 :
            if random.randint(0, 5) == 1:
                SelectedMsg = random.choice(self.Channels[Message.channel.name]["Messages"])
                Words = SelectedMsg.split()
                RdmWord = random.randint(0,len(Words) -1)
                Words[RdmWord] = self.Channels[Message.channel.name]["Word"]
                NewMsg = " ".join(Words)
                await Message.channel.send(NewMsg)
                self.Channels[Message.channel.name]["Messages"].clear()