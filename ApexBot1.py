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
    errorMsg = None
    lst=[]
    if len(args) is not 2:
        for word in args:
            name = word
        stat = 'kills'
    else:
        for word in args:
            lst.append(word)
        name = lst[0]
        if lst[1] == 'kills' or lst[1] == 'Kills':
            statMsg = 'Kills'
            stat = 'kills'
        elif lst[1] == 'wins' or lst[1] == 'Wins':
            statMsg = 'Wins'
            stat = 'winsWithFullSquad'
        elif lst[1] == 'damage' or lst[1] == 'Damage':
            statMsg = 'Damage'
            stat = 'damage'
        else:
            stat = 'kills'
            errorMsg = 'Syntax error: only kills, wins or damage is supported'

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
            if 'value' in data[i][stat]:
                #if value < data[i]['kills']['value']:
                value += data[i][stat]['value']
    if len(args) is not 2: 
        output = 'Could not understand, but '+name+' has '+str(value)+' kills! (Use syntax .update name kills/wins/damage)'
    elif errorMsg is not None:
        await client.say(errorMsg)
    else:
        output = name+' has got a total of: '+str(value)+' '+statMsg+'!'
    await client.say(output)
client.run(TOKEN)