import json
import re
import requests

class ExtraFunctions:
    
    def CheckStreamIsLive(ChannelName):
        Response = requests.get(f"https://twitch.tv/{ChannelName}")
        ResponseFiltered = re.search("\<script type\=\"application\/ld\+json\"\>\[(.*)\]\<\/script><link rel=\"icon\" type=\"image\/png\"", Response.text)
        if (ResponseFiltered):
            return json.loads(ResponseFiltered.group(1).replace("@", ""))
        return None