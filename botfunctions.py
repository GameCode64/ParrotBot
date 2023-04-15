import json
import os
import random
import re

import twitchio
from dotenv import load_dotenv
from extrafunctions import ExtraFunctions

# Loading the config variables from the .env file
load_dotenv()

class BotFunctions():
    
    # Defining some variables
    Channels={}
    HelloSenteces=["hello booty","hello bootybot","hello @b1g_b00ty","hello b1g_b00ty","hello bigbooty","hello big booty"]
    TmpReplaceWord=os.getenv("STARTWORD")

    def InitiateChannel(self, Message):
        if Message.channel.name not in self.Channels:
            self.Channels[Message.channel.name]={
                "Word": os.getenv("STARTWORD"),
                "Messages": [],
                "Ignore_Names": [],
                "Settings":{
                    "Chance_Rate": os.getenv("CHANCE_RATE"),
                    "Messaging": os.getenv("MESSAGE_TYPE"),
                    "Ignore_Offline": False,
                    "Degen_Mode": False
                }
            }
        self.SaveChannelJson(Message)

    def SaveChannelJson(self, Message):
        with open(f"settings/{Message.channel.name}.json", "w") as OutFile:
            OutFile.write(json.dumps(self.Channels[Message.channel.name]))

    # Adding the messages up to the stack
    def AddMessageToStack(self, Message):
        if Message.author.name.lower() in self.Channels[Message.channel.name]["Ignore_Names"]:
            return
        self.SaveChannelJson(Message)
        if len(Message.content.split()) > 3 and self.Channels[Message.channel.name]["Settings"]["Messaging"].lower() == "listed":
            self.Channels[Message.channel.name]["Messages"].append(Message.content)
            

    # Changing the word per channel as requested
    def ChangeChannelWord(self, Message):
        SetWord = re.search("^\!setword ([\w\!\+\-\_\d]+)", Message.content)
        if SetWord:
            self.Channels[Message.channel.name]["Word"]=SetWord.group(1)
            self.SaveChannelJson(Message)
            return self.Channels[Message.channel.name]["Word"]

    def AddNameToIgnore(self, Message):
        IgnoreName = re.search("^\!ignorename (.+)", Message.content.lower())
        if IgnoreName:
            if IgnoreName.group(1) not in self.Channels[Message.channel.name]["Ignore_Names"]:
                self.Channels[Message.channel.name]["Ignore_Names"].append(IgnoreName.group(1))
                self.SaveChannelJson(Message)
                return IgnoreName.group(1)
            else:
                return f"{IgnoreName.group(1)} already"

    def DelNameFromIgnore(self, Message):
        UnignoreName = re.search("^\!unignorename (.+)", Message.content.lower())
        if UnignoreName:
            if UnignoreName.group(1) in self.Channels[Message.channel.name]["Ignore_Names"]:
                self.Channels[Message.channel.name]["Ignore_Names"].remove(UnignoreName.group(1))
                self.SaveChannelJson(Message)
                return UnignoreName.group(1)
            else:
                return f"{UnignoreName.group(1)} already"

    def ChangeChance(self, Message):
        ChangeRate = re.search("^\!setchance (\d+)", Message.content)
        if ChangeRate:
            self.Channels[Message.channel.name]["Settings"]["Chance_Rate"]=ChangeRate.group(1)
            self.SaveChannelJson(Message)
            return self.Channels[Message.channel.name]["Settings"]["Chance_Rate"]

    def DegenResponse(self, Message):
         match random.randint(1,5):
                    case 1:
                       return (f"What do you want {Message.author.name}?")
                    case 2:
                        return (f"{Message.author.name} What is your problem?")
                    case 3:
                        return (f"Are you going to tell on me?")
                    case 4:
                        return (f"You summoned me {Message.author.name}?")
                    case 5:
                        return (f"Do you think i'm just a bot to talk to?")
