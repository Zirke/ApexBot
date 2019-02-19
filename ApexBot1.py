#!python3.6
import asyncio
import json
import requests
import discord
from discord.ext import commands

TOKEN = 'MzI1MjY5OTMwNDUyNzEzNDgy.D0r9VA.EyQTiWXoQJQ-yzt11tu0OxTPGCI'

client = commands.Bot(command_prefix='.')


def inf_from_tracker(name):
    url = 'https://public-api.tracker.gg/apex/v1/standard/profile/5/' + name
    headers = {'TRN-Api-Key': '8b3b6e28-122f-4d9a-8c54-794fca417953'}
    r = requests.get(url, headers=headers)
    #print(r.text)
    return r.text


@client.event
async def on_ready():
    print('Bot online')


def query_api(name, stat):
    value = 0
    output = ''
    try:
        data = json.loads(inf_from_tracker(name))
    except ValueError:
        print("Invalid json")
    else:
        for i in range(0, len(data['data']['children'][0]['stats'])):
            if data['data']['children'][0]['stats'][i]['metadata']['key'] == stat:
                print(data['data']['children'][0]['stats'][i]['metadata']['key'])
                value = data['data']['children'][0]['stats'][i]['value']
        output = name.capitalize() + ' has got a total of : ' + str(int(value)) + ' ' + stat.capitalize() + '!'
    return output


@client.command()
async def kills(*args):
    stat = 'Kills'
    errormsg = None
    if len(args) is not 1:
        errormsg = 'Syntax error: Use synatx .kills name'
    else:
        for word in args:
            name = word
    await client.say(query_api(name, stat))

@client.command()
async def damage(*args):
    stat = 'Damage'
    errormsg = None
    if len(args) is not 1:
        errormsg = 'Syntax error: Use synatx .damage name'
    else:
        for word in args:
            name = word
    await client.say(query_api(name, stat))

@client.command()
async def wins(*args):
    stat = 'WinsWithFullSquad'
    errormsg = None
    if len(args) is not 1:
        errormsg = 'Syntax error: Use synatx .wins name'
    else:
        for word in args:
            name = word
    await client.say(query_api(name, stat))


def broadcastWins(name):
    value = 0
    try:
        data = json.loads(inf_from_tracker(name))
    except ValueError:
        print("invalid json")
    else:
        for i in range(0, len(data)):
            if 'value' in data[i]['winsWithFullSquad']:
                # if value < data[i]['kills']['value']:
                value += data[i]['winsWithFullSquad']['value']
    return int(value)


async def background_task_wins(name):
    wins = {}
    newWins = {}
    await client.wait_until_ready()
    channel = discord.Object(id='325296935667761152')
    wins[name] = broadcastWins(name)
    while not client.is_closed:
        newWins[name] = broadcastWins(name)
        if newWins[name] > wins[name]:
            output = name + ' has just won ' + str(newWins[name] - wins[name]) + ' game(s)!'
            wins[name] = newWins[name]
            await client.send_message(channel, output)
        await asyncio.sleep(5)


# for name in broadcastNames:
# client.loop.create_task(background_task_wins(name))

client.run(TOKEN)
