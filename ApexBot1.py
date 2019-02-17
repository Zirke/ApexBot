#!python3.6
import re
from bs4 import BeautifulSoup
import json
import requests
import discord
from discord.ext import commands


TOKEN = 'MzI1MjY5OTMwNDUyNzEzNDgy.D0r9VA.EyQTiWXoQJQ-yzt11tu0OxTPGCI'

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot online')

@client.command()
async def update(*args):
    if not args:
        name = 'Dritix'
    else:
        for word in args:
            name = word        
    url = 'https://apex.tracker.gg/profile/pc/'+name
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")
    pattern = re.compile(r"var imp_careerStats = \[([^]]+)\]")
    script = str(soup.find("script", text=pattern))
    s = re.match(r"[^[]*\[([^]]*)\]", script).groups()[0]
    s = "[" + s + "]"
    value = 0
    try:
        data = json.loads(s)
    except ValueError:
        print ("invalid json")
    else:
        for i in range(0, len(data)):
            if 'value' in data[i]['kills']:
                #if value < data[i]['kills']['value']:
                value += data[i]['kills']['value']
    output = name+' has got a total of: '+str(value)+' kills!'
    await client.say(output)
client.run(TOKEN)