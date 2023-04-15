import json
import os
import random

import twitchio
from dotenv import load_dotenv
from extrafunctions import ExtraFunctions
from botfunctions import BotFunctions

# Loading the config variables from the .env file
load_dotenv()

class Bot(twitchio.Client):
    def __init__(self, Token, Initial_Channels):
        super().__init__(
            token=Token,
            initial_channels=Initial_Channels,
        )

    async def event_ready(self):
        print("Loading settings per channel")
        for File in os.listdir("settings"):
            if os.path.isfile(os.path.join("settings", File)) and File != ".keep":
                print(f" -{File}")
                Channel=File.replace(".json", "")
                with open(f"settings/{File}", "r") as OpenFile:
                    BotFunctions.Channels[Channel]=json.load(OpenFile)
                print(BotFunctions.Channels[Channel])
        print(f"{self.nick} Hopped in to chat")

    async def event_message(self, Message):

        # Initating Channel
        BotFunctions.InitiateChannel(Message)

        # Getting channel status
        ChannelStatus=ExtraFunctions.CheckStreamIsLive(Message.channel.name.lower())

        # If requested don't react if channel is offline
        if not BotFunctions.Channels[Message.channel.name]["Settings"]["Ignore_Offline"]:
            if not ChannelStatus:
                return
            else:
                if not ExtraFunctions.CheckStreamIsLive(Message.channel.name.lower()).publication["isLiveBroadcast"]:
                    return

        # Ignore messages sent by the bot itself
        if Message.echo:
            return

        # ungnoring the filled name because the steamer do want this one to echo
        elif Message.content.startswith("!unignorename"):
            # Only a mod is allowed to do this
            if Message.author.is_broadcaster:
                await Message.channel.send(f"{BotFunctions.DelNameFromIgnore(Message)} has been removed from the ignore list!")

        if Message.author.name in BotFunctions.Channels[Message.channel.name]["Ignore_Names"]:
            return

        # Giving a reaction to hello booty
        if Message.content.lower().startswith(tuple(BotFunctions.HelloSenteces)):
            await Message.channel.send(f"Hello big butted {Message.author.name}!")

        # Giving a reaction to bootybot yes
        elif Message.content.lower().find("bootybot yes") != -1: # Using -1 as validation. find() gives -1 if the value isn't found
            await Message.channel.send(":D")

        # Giving a reaction to bootybot no
        elif Message.content.lower().find("bootybot no") != -1: # Using -1 as validation. find() gives -1 if the value isn't found
            await Message.channel.send("D:")

        # Giving a reaction someone that is talking about bootybot
        elif Message.content.lower().find("bootybot") != -1: # Using -1 as validation. find() gives -1 if the value isn't found
            if not BotFunctions.Channels[Message.channel.name]["Settings"]["Degen_Mode"]:
                await Message.channel.send(f"Hi {Message.author.name}, i am a friendly bot! I say everythin you say but with a slight twist.")
            else:
                await Message.channel.send(BotFunctions.DegenResponse(Message))
               
        elif Message.content.lower().find("b1g_b00ty") != -1: # Using -1 as validation. find() gives -1 if the value isn't found
            if not BotFunctions.Channels[Message.channel.name]["Settings"]["Degen_Mode"]:
                await Message.channel.send(f"Hi {Message.author.name}, i am a friendly bot! I say everythin you say but with a slight twist.")
            else:
                await Message.channel.send(BotFunctions.DegenResponse(Message))



        # Moderating the word to replace in the message
        elif Message.content.startswith("!setword"):
            # Only a mod is allowed to do this
            if Message.author.is_mod:
                await Message.channel.send("Word has been changed to: "+BotFunctions.ChangeChannelWord(Message))

        # Moderating the chance rate
        elif Message.content.startswith("!setchance"):
            # Only a streamer is allowed to do this
            if Message.author.is_broadcaster:
                Number=int(BotFunctions.ChangeChance(Message))
                await Message.channel.send(f"The chance rate has been changed to 1:{Number}")

        # Ignoring the filled name because the steamer doesn't want this one to echo
        elif Message.content.startswith("!ignorename"):
            # Only a streamer is allowed to do this
            if Message.author.is_broadcaster:
                await Message.channel.send(f"{BotFunctions.AddNameToIgnore(Message)} has been added to the ignore list!")

        # toggling offlinechatmode
        elif Message.content.startswith("!toggleofflinemode"):
            # Only a streamer is allowed to do this
            if Message.author.is_broadcaster:
                BotFunctions.Channels[Message.channel.name]["Settings"]["Ignore_Offline"] = not BotFunctions.Channels[Message.channel.name]["Settings"]["Ignore_Offline"]
                await Message.channel.send(f"""Chat offline mode is: {BotFunctions.Channels[Message.channel.name]["Settings"]["Ignore_Offline"]}""")

        # toggling offlinechatmode
        elif Message.content.startswith("!toggledegenmode"):
            # Only a streamer is allowed to do this
            if Message.author.is_broadcaster:
                BotFunctions.Channels[Message.channel.name]["Settings"]["Degen_Mode"] = not BotFunctions.Channels[Message.channel.name]["Settings"]["Degen_Mode"]
                await Message.channel.send(f"""Degen mode is: {BotFunctions.Channels[Message.channel.name]["Settings"]["Degen_Mode"]}""")

        # Ignoring all commands, preventing them to be added into the message list
        elif Message.content.startswith("!"):
            return
        # If everything has been done, lets add the message into the list
        else:
            BotFunctions.AddMessageToStack(Message)

        # After the list has been filled with atleast if messaging is set to listed
        if BotFunctions.Channels[Message.channel.name]["Settings"]["Messaging"].lower() == "listed":
            if len(BotFunctions.Channels[Message.channel.name]["Messages"]) > 5 :
                if random.randint(1, int(BotFunctions.Channels[Message.channel.name]["Settings"]["Chance_Rate"])) == 1: # chance rating
                    SelectedMsg = random.choice(BotFunctions.Channels[Message.channel.name]["Messages"])
                    Words = SelectedMsg.split()
                    RdmWord = random.randint(0,len(Words) -1)
                    Words[RdmWord] = BotFunctions.Channels[Message.channel.name]["Word"]
                    NewMsg = " ".join(Words)
                    await Message.channel.send(NewMsg)
                    BotFunctions.Channels[Message.channel.name]["Messages"].clear()

        # If messaging is set to direct we just apply the gods of RNG to capture a random message
        elif BotFunctions.Channels[Message.channel.name]["Settings"]["Messaging"].lower() == "direct":
                if len(Message.content.split()) > 2:
                    if random.randint(1, int(BotFunctions.Channels[Message.channel.name]["Settings"]["Chance_Rate"])) == 1: # chance rating
                        SelectedMsg = Message.content
                        Words = SelectedMsg.split()
                        RdmWord = random.randint(0,len(Words) -1)
                        Words[RdmWord] = BotFunctions.Channels[Message.channel.name]["Word"]
                        NewMsg = " ".join(Words)
                        await Message.channel.send(NewMsg)