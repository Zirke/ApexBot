#!python3.6
import asyncio
import time
import requests
import discord
from discord.ext import commands

TOKEN = 'MzI1MjY5OTMwNDUyNzEzNDgy.D0r9VA.EyQTiWXoQJQ-yzt11tu0OxTPGCI'

client = commands.Bot(command_prefix='.')

namelist = {}


def deserialize_namelist():
    global namelist
    namelist = eval(open('namelist.py', 'r').read())


def write_namelist():
    with open('namelist.py', 'w') as f: f.write(repr(namelist))


def inf_from_tracker(name):
    url = 'https://public-api.tracker.gg/apex/v1/standard/profile/5/' + name
    headers = {'TRN-Api-Key': '8b3b6e28-122f-4d9a-8c54-794fca417953'}
    r = requests.get(url, headers=headers)
    # print(r.text)
    return r.json()


@client.event
async def on_ready():
    print('Bot online')
    deserialize_namelist()
    client.loop.create_task(background_task_wins())
    print('help')


def query_api(name, stat):
    value = 0
    try:
        data = inf_from_tracker(name)
    except ValueError:
        print("Invalid json")
    else:
        for j in range(0, len(data['data']['children'])):
            for i in range(0, len(data['data']['children'][j]['stats'])):
                if data['data']['children'][j]['stats'][i]['metadata']['key'] == stat:
                    print(data['data']['children'][j]['stats'][i]['metadata']['key'])
                    value += data['data']['children'][j]['stats'][i]['value']
    return value


@client.command()
async def kills(*args):
    stat = 'Kills'
    errormsg = None
    if len(args) is not 1:
        errormsg = 'Syntax error: Use synatx .kills name'
    else:
        for word in args:
            name = word
    output = name.capitalize() + ' has got a total of : ' + str(
        int(query_api(name, stat))) + ' ' + stat.capitalize() + '!'
    await client.say(output)


@client.command()
async def damage(*args):
    stat = 'Damage'
    errormsg = None
    if len(args) is not 1:
        errormsg = 'Syntax error: Use synatx .damage name'
    else:
        for word in args:
            name = word
    output = name.capitalize() + ' has got a total of : ' + str(
        int(query_api(name, stat))) + ' ' + stat.capitalize() + '!'
    await client.say(output)


@client.command()
async def wins(*args):
    stat = 'WinsWithFullSquad'
    errormsg = None
    if len(args) is not 1:
        errormsg = 'Syntax error: Use synatx .wins name'
    else:
        for word in args:
            name = word
    output = name.capitalize() + ' has got a total of : ' + str(
        int(query_api(name, stat))) + ' ' + stat.capitalize() + '!'
    await client.say(output)


@client.command()
async def add(*args):
    nametoadd = None
    if len(args) is not 1:
        await client.say('Syntax error, use syntax .add name')
    else:
        for word in args:
            name = word.capitalize()
            # print(name+'1st')

        if name in namelist:
            await client.say('Name already in list')
        else:
            nametoadd = name
        if nametoadd:
            namelist[nametoadd.capitalize()] = 0
            write_namelist()
            await client.say(nametoadd.capitalize() + ' added to namelist.')
            print('Added ' + nametoadd)


@client.command()
async def remove(*args):
    nametoremove = None
    if len(args) is not 1:
        await client.say('Syntax error, use syntax .add name')
    else:
        for word in args:
            name = word.capitalize()
    if name in namelist:
        nametoremove = name
    else:
        await client.say(name + ' not in namelist.')
    if nametoremove:
        nametoremove = nametoremove.capitalize()
        del namelist[nametoremove]
        write_namelist()
        await client.say(nametoremove + ' removed from namelist.')


def broadcastWins(name):
    value = 0
    try:
        data = inf_from_tracker(name)
    except ValueError:
        print("invalid json")
    else:
        for j in range(0, len(data['data']['children'])):
            for i in range(0, len(data['data']['children'][j]['stats'])):
                if data['data']['children'][j]['stats'][i]['metadata']['key'] == 'WinsWithFullSquad':
                    value += data['data']['children'][j]['stats'][i]['value']
    return int(value)


async def background_task_wins():
    newWins = {}
    await client.wait_until_ready()
    channel = discord.Object(id='325296935667761152')
    while not client.is_closed:
        for name in namelist.copy():
            newWins[name] = broadcastWins(name)
            if newWins[name] > namelist[name]:
                output = name + ' has just won ' + str(newWins[name] - namelist[name]) + ' game(s)!'
                namelist[name] = newWins[name]
                await client.send_message(channel, output)
            await asyncio.sleep(5)
        write_namelist()
        await asyncio.sleep(5)


client.run(TOKEN)
