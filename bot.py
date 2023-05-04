import json
import os
import random
import re

import twitchio
from dotenv import load_dotenv
from extrafunctions import ExtraFunctions

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
    HelloSenteces=["hello booty","hello bootybot","hello @b1g_b00ty","hello b1g_b00ty","hello bigbooty","hello big booty"]
    TmpReplaceWord=os.getenv("STARTWORD")

    def InitiateChannel(self, _Message):
        if _Message.channel.name not in self.Channels:
            self.Channels[_Message.channel.name]={
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
        self.SaveChannelJson(_Message)

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

    def AddNameToIgnore(self, Message, User = False):
        if ( not User):
            IgnoreName = re.search("^\!ignorename (.+)", Message.content.lower())
            if IgnoreName:
                if IgnoreName.group(1) not in self.Channels[Message.channel.name]["Ignore_Names"]:
                    self.Channels[Message.channel.name]["Ignore_Names"].append(IgnoreName.group(1))
                    self.SaveChannelJson(Message)
                    return IgnoreName.group(1)
                else:
                    return f"{IgnoreName.group(1)} already"
        else:
            if User not in self.Channels[Message.channel.name]["Ignore_Names"]:
                    self.Channels[Message.channel.name]["Ignore_Names"].append(User)
                    self.SaveChannelJson(Message)
                    return User

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

    def ReplaceWord(self, Message, Words):
        Words = Words
        RdmWord = random.randint(0,len(Words) -1)

        if (random.randint(1,3) == 1):
            RdmLetterStart = random.randint(0, len(Words[RdmWord]))
            RdmLetterEnd = random.randint(RdmLetterStart, len(Words[RdmWord]))
            Words[RdmWord] = Words[RdmWord][:RdmLetterStart] + self.Channels[Message.channel.name]["Word"] + Words[RdmWord][RdmLetterEnd:]
        else:
            Words[RdmWord] = self.Channels[Message.channel.name]["Word"]
        Words = " ".join(Words)
        return Words
    
    async def event_ready(self):
        print("Loading settings per channel")
        for File in os.listdir("settings"):
            if os.path.isfile(os.path.join("settings", File)) and File != ".keep":
                print(f" -{File}")
                Channel=File.replace(".json", "")
                with open(f"settings/{File}", "r") as OpenFile:
                    self.Channels[Channel]=json.load(OpenFile)
                print(self.Channels[Channel])
        print(f"{self.nick} Hopped in to chat")

    async def event_message(self, Message):

        # Initating Channel
        self.InitiateChannel(Message)

        # Getting channel status
        ChannelStatus=ExtraFunctions.CheckStreamIsLive(Message.channel.name.lower())

        # If requested don't react if channel is offline
        if not self.Channels[Message.channel.name]["Settings"]["Ignore_Offline"]:
            if not ChannelStatus:
                return
            else:
                if not ChannelStatus["publication"]["isLiveBroadcast"]:
                    return

        # Ignore messages sent by the bot itself
        if Message.echo:
            return

        # ungnoring the filled name because the steamer do want this one to echo
        elif Message.content.startswith("!unignorename"):
            # Only a mod is allowed to do this
            if Message.author.is_broadcaster:
                await Message.channel.send(f"{self.DelNameFromIgnore(Message)} has been removed from the ignore list!")

        if Message.author.name in self.Channels[Message.channel.name]["Ignore_Names"]:
            return

        # Giving a reaction to hello booty
        if Message.content.lower().startswith(tuple(self.HelloSenteces)):
            await Message.channel.send(f"Hello big butted {Message.author.name}!")

        # Giving a reaction to bootybot yes
        elif Message.content.lower().find("bootybot yes") != -1: # Using -1 as validation. find() gives -1 if the value isn't found
            await Message.channel.send(":D")

        # Giving a reaction to bootybot no
        elif Message.content.lower().find("bootybot no") != -1: # Using -1 as validation. find() gives -1 if the value isn't found
            await Message.channel.send("D:")

        # Just an easter egg for Ghunzor's channel
        elif Message.content.lower().find("boo! scary") != -1: # Using -1 as validation. find() gives -1 if the value isn't found
            if(Message.channel.name.lower() == "ghunzor"):
                await Message.channel.send("!scary")

        # Giving a reaction someone that is talking about bootybot
        elif Message.content.lower().find("bootybot") != -1: # Using -1 as validation. find() gives -1 if the value isn't found
            if not self.Channels[Message.channel.name]["Settings"]["Degen_Mode"]:
                await Message.channel.send(f"Hi {Message.author.name}, i am a friendly bot! I say everythin you say but with a slight twist.")
            else:
                await Message.channel.send(self.DegenResponse(Message))
    
        elif Message.content.lower().find("b1g_b00ty") != -1: # Using -1 as validation. find() gives -1 if the value isn't found
            if not self.Channels[Message.channel.name]["Settings"]["Degen_Mode"]:
                await Message.channel.send(f"Hi {Message.author.name}, i am a friendly bot! I say everythin you say but with a slight twist.")
            else:
                await Message.channel.send(self.DegenResponse(Message))
         
        # Ignoring the crybabies
        elif Message.content.startswith("!ignoremenowandforeverhere"):
            # Only a streamer is allowed to do this
            self.AddNameToIgnore(Message, Message.author.name)
            await Message.channel.send(f"!ban {Message.author.name} has been added to the ignore list!")

        # Moderating the word to replace in the message
        elif Message.content.startswith("!setword"):
            # Only a mod is allowed to do this
            if Message.author.is_mod:
                await Message.channel.send("Word has been changed to: "+self.ChangeChannelWord(Message))

        # Moderating the chance rate
        elif Message.content.startswith("!setchance"):
            # Only a streamer is allowed to do this
            if Message.author.is_broadcaster:
                Number=int(self.ChangeChance(Message))
                await Message.channel.send(f"The chance rate has been changed to 1:{Number}")

        # Ignoring the filled name because the steamer doesn't want this one to echo
        elif Message.content.startswith("!ignorename"):
            # Only a streamer is allowed to do this
            if Message.author.is_broadcaster:
                await Message.channel.send(f"{self.AddNameToIgnore(Message)} has been added to the ignore list!")

        # toggling offlinechatmode
        elif Message.content.startswith("!toggleofflinemode"):
            # Only a streamer is allowed to do this
            if Message.author.is_broadcaster:
                self.Channels[Message.channel.name]["Settings"]["Ignore_Offline"] = not self.Channels[Message.channel.name]["Settings"]["Ignore_Offline"]
                await Message.channel.send(f"""Chat offline mode is: {self.Channels[Message.channel.name]["Settings"]["Ignore_Offline"]}""")

        # toggling offlinechatmode
        elif Message.content.startswith("!toggledegenmode"):
            # Only a streamer is allowed to do this
            if Message.author.is_broadcaster:
                self.Channels[Message.channel.name]["Settings"]["Degen_Mode"] = not self.Channels[Message.channel.name]["Settings"]["Degen_Mode"]
                await Message.channel.send(f"""Degen mode is: {self.Channels[Message.channel.name]["Settings"]["Degen_Mode"]}""")

        # Ignoring all commands, preventing them to be added into the message list
        elif Message.content.startswith("!"):
            return
        # If everything has been done, lets add the message into the list
        else:
            self.AddMessageToStack(Message)

        # After the list has been filled with atleast if messaging is set to listed
        if self.Channels[Message.channel.name]["Settings"]["Messaging"].lower() == "listed":
            if len(self.Channels[Message.channel.name]["Messages"]) > 5 :
                if random.randint(1, int(self.Channels[Message.channel.name]["Settings"]["Chance_Rate"])) == 1: # chance rating
                    SelectedMsg = Message.content
                    WordsLeng = len(SelectedMsg.split())
                    #place while here to loop through each word
                    if (random.randint(1,2) == 1):
                        ConvWords = 0
                        while ((100 / WordsLeng * ConvWords < 40 )):
                            ConvWords = ConvWords + 1
                            Words = SelectedMsg.split()
                            SelectedMsg = self.ReplaceWord(Message, Words)
                            if (random.randint(1,5)):
                                break
                    #end while loop here
                    else:
                        Words = SelectedMsg.split()
                        SelectedMsg = self.ReplaceWord(Message, Words)
                    await Message.channel.send(SelectedMsg)
                    self.Channels[Message.channel.name]["Messages"].clear()

        # If messaging is set to direct we just apply the gods of RNG to capture a random message
        elif self.Channels[Message.channel.name]["Settings"]["Messaging"].lower() == "direct":
            if len(Message.content.split()) > 2:
                if random.randint(1, int(self.Channels[Message.channel.name]["Settings"]["Chance_Rate"])) == 1: # chance rating
                    SelectedMsg = Message.content
                    WordsLeng = len(SelectedMsg.split())
                    #place while here to loop through each word
                    if (random.randint(1,2) == 1):
                        ConvWords = 0
                        while ((100 / WordsLeng * ConvWords < 40 )):
                            ConvWords = ConvWords + 1
                            Words = SelectedMsg.split()
                            SelectedMsg = self.ReplaceWord(Message, Words)
                            if (random.randint(1,5)):
                                break
                    #end while loop here
                    else:
                        Words = SelectedMsg.split()
                        SelectedMsg = self.ReplaceWord(Message, Words)
                    await Message.channel.send(SelectedMsg)
